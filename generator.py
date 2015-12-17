#!/usr/bin/env python

import subprocess, datetime
from itertools import repeat

emscripten_git_repo = 'https://github.com/kripken/emscripten/'
docker_hub_repo = "trzeci/emscripten"
minimum_version = "1.34.1"


def is_version_at_least(ver, target):
	ver = ver.split('.')
	target = target.split('.')
	while len(ver) < len(target):
		ver += ['0']
	for i in range(len(ver)):
		if int(ver[i]) < int(target[i]):
			return False
		elif int(ver[i]) > int(target[i]):
			return True
	return True


def get_tags():
	tags = subprocess.check_output(["git", 'ls-remote', '--tags', emscripten_git_repo])
	all_tags = []

	for t in tags.split('\n'):
		try:
			t = t[t.index('refs/tags/') + len('refs/tags/'):].strip()
			if is_version_at_least(t, minimum_version):
				all_tags += [t]
		except:
			pass
	return all_tags

def version_compare(x, y):
	a = 1 if is_version_at_least(x, y) else 0
	b = 1 if is_version_at_least(y, x) else 0
	return a - b

def log(text):
	with open("log.txt", "a") as myfile:
		myfile.write("\n[{time}] {text}".format(time=datetime.datetime.now(), text=text))
	print(text)

def get_builds(tags, b64=False):
	builds = []

	for bits in ["32bit"] + (["64bit"] if b64 else []):
		for tag in tags:
			sdk = "sdk-tag-" + tag + "-" + bits
			builds.append({
					"tag": tag,
					"dir": "tag-" + tag,
					"sdk": sdk,
					"docker_tag": sdk,
					"docker_name" : docker_hub_repo + ":" + sdk,
				})
	return builds

def get_server_tags():
	from urllib import urlopen
	import json

	api = "https://registry.hub.docker.com/v1/repositories/{repo}/tags".format(repo=docker_hub_repo)
	response = urlopen(api)
	data = json.loads(str(response.read()))
	result = {}
	for node in data:
		result[str(node["name"])] = {
			"layer" : str(node["layer"])
		}
	return result

def generate_dockerfile(path, build):
	f = open("Dockerfile.in", "r")
	data = f.read();
	f.close()
	properties = {
		"EMSCRIPTEN_SDK_TAG" : build["sdk"], 
		"EMSCRIPTEN_SDK_DIR" : build["dir"]
	}
	for p in properties:
		data = data.replace("{" + p + "}", properties[p])
	f = open(path, "w")
	f.write(data)
	f.close()

def rename(builds):
	for pb in builds:
		if pb.startswith("sdk"):
			log("Already OK: " + pb)
			continue
		tag = "sdk-tag-" + pb + "-32bit"
		if tag in builds:
			log("Already Exists: " + pb)
			continue

		log("RETAG: " + pb  + " => " + tag)
		# get image
		subprocess.call(["docker", "pull", docker_hub_repo + ":" + pb])
		# re-tag
		subprocess.call(["docker", "tag", docker_hub_repo + ":" + pb, docker_hub_repo + ":" + tag])
		# push
		subprocess.call(["docker", "push", docker_hub_repo + ":" + tag])
		# clean
		subprocess.call(["docker", "rmi", "-f", docker_hub_repo + ":" + pb])
		subprocess.call(["docker", "rmi", "-f", docker_hub_repo + ":" + tag])


def generate(builds, serverTags):
	for build in builds:
		# Check that tag exists in remote repository 
		if build["docker_tag"] in serverTags:
			log("[INFO] Not need to create " + build["docker_tag"])
			continue

		log("[INFO] Start building {tag}".format(tag=build["docker_tag"]))

		generate_dockerfile("Dockerfile", build)

		# generate docker image 
		ret = subprocess.call(["docker", "build", "-t",  build["docker_name"], "."])

		if ret != 0:
			log("[ERROR] Building {tag} failed".format(tag=build["docker_tag"]))
			continue

		# test image by compiling sample.cpp
		t_start = datetime.datetime.now()
		ret = subprocess.call(["docker run -v $(pwd):/src " + build["docker_name"]+ " emcc test.cpp -o test.js && nodejs test.js"], shell=True)

		if ret != 0:
			log("[ERROR] Testing {tag} failed".format(tag=build["docker_tag"]))
			continue
		else:
			log("[INFO] Compiling [{tag}] in: {time}".format(tag=build["docker_tag"], time=str(datetime.datetime.now() - t_start)))

		# push to docker repository
		for i in repeat(None, 3):
			ret = subprocess.call(["docker", "push", build["docker_name"]])
			if ret != 0:
				log("[WARNING] Pushing {tag} failed. Repeat.".format(tag=build["docker_tag"]))
		
		if ret != 0:
			log("[ERROR] Pushing {tag} failed.".format(tag=build["docker_tag"]))
			continue

		subprocess.call(["docker", "rmi", "-f", build["docker_name"]])
		log("[INFO] Finished building {tag}".format(tag=build["docker_tag"]))


tags = get_tags()
sorted(tags, cmp=version_compare)

builds = get_builds(tags)
pushed_builds = get_server_tags()


generate(builds, pushed_builds)


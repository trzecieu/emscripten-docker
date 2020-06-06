
import json
import re
import subprocess
import os

from urllib.request import Request
from urllib.request import urlopen
from itertools import repeat

def mock_log_handler(line):
    print(line)

class DockerHelper:
    @staticmethod
    def decompose_image_id(image_id):
        print(image_id)
        project, tag = image_id.split(":")
        version = re.match(r'.+(\d+\.\d+\.\d+).+', tag).groups()[0]
        return (project, tag, version)

    @staticmethod
    def push_image(image, dry=False):
        print(f"Pushing: {image}")
        if dry: return 0

        for i in repeat(None, 3):
            if not subprocess.call(["docker", "push", image]):
                return 0
        return -1

    @staticmethod
    def rmi(image):
        subprocess.call(["docker", "rmi", "-f", image])

    @staticmethod
    def tag(old, *new):
        for n in new:
            subprocess.call(["docker", "tag", old, n])
        return

    @staticmethod
    def compile_image(source_folder, tag, args, log_file, no_cache = False, log_handler = None):
        args = args or {}
        log_handler = log_handler or mock_log_handler
        with open(log_file, "w") as f:
            cmd = ["docker", "build"]
            cmd += ["--network", "host"]
            cmd += ["--no-cache"] if no_cache else []
            cmd += ["-t", tag]
            cmd += [f"--build-arg={k}={v}" for k, v in args.items()]
            cmd += [source_folder]
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
            while 42 < 1337:
                l = p.stdout.readline()
                if not l: break
                l = l.decode()
                f.write(l)
                f.flush()
                log_handler(l)
            p.communicate()
            return p.returncode
        return -1

class DockerRegistry:
    @staticmethod
    def pushed_tags(registry, repo):
        response = urlopen(f"https://{registry}/v1/repositories/{repo}/tags")
        raw = response.read().decode()
        data = json.loads(raw)
        return list(map(lambda x: str(x["name"]), data))

    def __init__(self):
        pass

    def login(self):
        # usefull to access some Docker Hub functionality
        r = Request("https://hub.docker.com/v2/users/login/",
            json.dumps({
                "username" : os.environ["DOCKER_HUB_USERNAME"],
                "password" : os.environ["DOCKER_HUB_PASSWORD"]
            }).encode(),
            {'Content-Type': 'application/json'}
        )
        data = urlopen(r).read()
        data = data.decode()
        try:
            self.access_token = json.loads(data)["token"]
            print("Logged in!")
        except Exception as e:
            print("Wrong docker login data.", e)

    def update_description(self, repository, short_description, full_description):
        r = Request(f"https://hub.docker.com/v2/repositories/{repository}/",
            json.dumps({
                "full_description" : full_description,
                "description" : short_description,
            }).encode(),
            headers=self.add_authorization_header({
                'Content-Type': 'application/json'
            })
        )
        r.get_method = lambda: "PATCH"
        data = urlopen(r).read()

    def get_auth_header(self, repository, headers=None):
        headers = headers if headers else {}
        r = Request(f"https://auth.docker.io/token?service=registry.docker.io&scope=repository:{repository}:pull")
        data = urlopen(r).read()
        headers["Authorization"] = "Bearer " + json.loads(data)["token"]
        return headers

    def get_manifest(self, repository, reference):
        r = Request(
            f"https://index.docker.io/v2/{repository}/manifests/{reference}",
            headers=self.get_auth_header(repository, {
                "Accept" : "application/vnd.docker.distribution.manifest.v2+json"
            })
        )
        data = None
        try:
            data = json.loads(urlopen(r).read())
        except Exception as e:
            pass
        return data

    def get_digest(self, repository, reference):
        manifest = self.get_manifest(repository, reference)
        return manifest["config"]["digest"] if manifest else None

    def add_authorization_header(self, headers):
        headers["Authorization"] = "JWT " + self.access_token
        return headers

    def authorized(self):
        return self.access_token is not None

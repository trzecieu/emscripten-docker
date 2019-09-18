#!/usr/bin/env python3
import argparse
import subprocess
import datetime
import time
import os
import pwd
import re
import copy

from functools import cmp_to_key
from pprint import PrettyPrinter

import toml

from builder.dashboard import Dashboard
from builder.docker import DockerRegistry, DockerHelper
from subprocess import PIPE, Popen

pprint = PrettyPrinter(1).pprint

EMSCRIPTEN_REPO = "https://github.com/emscripten-core/emscripten/"
DOCKER_REGISTRY = "registry.hub.docker.com"

# TODO: remove
DOCKER_REPO = "trzeci/emscripten"

QUEUE_FILE = "queue.txt"
LOG_COMPILATION = "build.log"
ROOT = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), ".."))

config = toml.load(open("config.toml", "r"))

def format_values(sth, mapping):
    def handle_object(obj):
        for k, v in obj.items():
            obj[k] = format_values(v, mapping)
        return obj

    def handle_list(arr):
        for i, v in enumerate(arr):
            arr[i] = format_values(v, mapping)
        return arr

    if type(sth) is dict:
        return handle_object(sth)
    if type(sth) is list:
        return handle_list(sth)
    if type(sth) is str:
        return sth.format_map(mapping)
    return sth

def index_image_name(name):
    for i, v in enumerate(config["images"]):
        if v["name"] == name:
            return i
    return -1

def get_variants():
    return list(map(lambda x: x["name"], filter(lambda x: x["enabled"], config["images"])))

class FakeDict(dict):
    def __getitem__(self, key):
        if not self.__contains__(key):
            return "{" + key + "}"
        return super().__getitem__(key)

def get_build_description(variant, registries, emsdk_cs="master"):
    index = index_image_name(variant.name)
    if index < 0: return None

    template = copy.deepcopy(config["images"][index])
    tags = []
    for registry in registries:
        for tag in template["tags"]:
            tags.append(tag.format_map(FakeDict(registry)))

    template["tags"] = tags
    template = format_values(template, {
        "emsdk_cs": emsdk_cs,
        "namespace": variant.namespace,
        "project": variant.project,
        "version": variant.version,
    })
    # pprint(template)
    return template

def log(text, console=False):
    if console:
        dashboard.log(text)

    with open(LOG_COMPILATION, "a") as f:
        f.write("\n[{time}] {text}".format(time=datetime.datetime.now(), text=text))

def sort_variants(x, y):
    return index_image_name(x.name) - index_image_name(y.name)

def version_compare(x, y):
    a = 1 if is_version_at_least(x, y) else 0
    b = 1 if is_version_at_least(y, x) else 0
    return a - b

def cmp_name_versions(x, y):
    return version_compare(x.name, y.name)

def is_version_at_least(ver, target):
    ver = map(lambda x: int(x) if x.isdigit() else 0, ver.split('.'))
    target = map(lambda x: int(x) if x.isdigit() else 0, target.split('.'))

    ver = list(ver)
    target = list(target)

    while len(ver) < len(target):
        ver += [0]
    for i, v in enumerate(ver):
        if v < target[i]:
            return False
        elif v > target[i]:
            return True
    return True

#  Emscripten Helpers ----------------------------------------------------------

class EMBuild:
    def __init__(self, emscripten_sdk, update):
        self.emscripten_sdk = emscripten_sdk
        self.update = update

    @property
    def docker_name(self, docker_project):
        return docker_project + ":" + self.emscripten_sdk

    @property
    def docker_tag(self):
        return self.emscripten_sdk

class EMVariant:
    def __init__(self, name, version):
        """
        @param name: Either full name i.e. trzeci/emscripten or reduced name in case of official images
        @param version: version of Emscripten SDK
        """
        self.name = name
        self.version = version
        (self.namespace, self.project) = name.split("/")

    def __hash__(self):
        return hash((self.name, self.version))

    def __repr__(self):
        return "EMVariant({}/{}:{})".format(self.namespace, self.project, self.version)

    def __str__(self):
        return f"{self.namespace}/{self.project}:{self.version}"

    def __eq__(self, other):
        return self.name == other.name and self.version == other.version


class EMHelper:
    @staticmethod
    def get_sdk_name_tag(tag):
        return "sdk-tag-{tag}-64bit".format(tag=tag)

    @staticmethod
    def get_sdk_name_branch(branch):
        return "sdk-{branch}-64bit".format(branch=branch)

    @staticmethod
    def get_emscripten_tags(min_version):
        tags = subprocess.check_output(["git", 'ls-remote', '--tags', EMSCRIPTEN_REPO]).decode("utf-8").strip().split("\n")
        all_tags = []
        for t in tags:
            try:
                t = t[t.index('refs/tags/') + len('refs/tags/'):].strip()
                if is_version_at_least(t, min_version):
                    all_tags += [t]
            except:
                pass
        result = list(map(lambda x: str(x), all_tags))
        result = sorted(result, key=cmp_to_key(version_compare), reverse=True)
        result = list(filter(lambda x: x not in config["sdk_ignored"], result))
        return result

    @staticmethod
    def expand_tags_to_variants(tags):
        result = set()
        for t in tags:
            for r in get_variants():
                result.add(EMVariant(r, t))
        return result

class EmscriptenTester:
    @staticmethod
    def test_image(id, tests_cases):
        log("TESTING: " + id)
        test_failed = False
        # explode by defined and undefined user
        for user in [["-u", "emscripten"], []]:
            log("[INFO] ## Setting user switch: '%s'" % user)
            # explode by existence of entrypoint
            for entrypoint in [["--entrypoint="], []]:
                log("[INFO] ## Setting entrypoint switch: '%s'" % entrypoint)
                for test in tests_cases:
                    volume = os.path.join(ROOT, "builder", "test_source")
                    cmd = [ "docker", "run", "--rm" ]
                    # test build with and without entrypoint (to make sure that raw image also works)
                    cmd += entrypoint
                    cmd += user
                    cmd += [ "-v", "{}:/src".format(volume) ]
                    cmd += [ "-w", "/src" ]
                    cmd += [ "-u", "emscripten" ]
                    cmd += [ id ]
                    cmd += [ "bash", "-c" ]
                    cmd += [ test ]

                    p = Popen(cmd,
                        stdout=PIPE,
                        stderr=PIPE,
                    )
                    out, err = p.communicate()

                    log("[INFO]: {}".format(subprocess.list2cmdline(cmd)))

                    if p.returncode:
                        if err: log(err.decode())
                        if out: log(out.decode())

                        log(f"[ERROR] Testing {id} failed")
                        test_failed = True

        if test_failed:
            log("TEST: {} - FAIL".format(id), True)
        else:
            log("TEST: {} - SUCCESS".format(id), True)

        return test_failed




class CompilationSet:
    def __init__(self, name, variants=None):
        self.name = name
        self.variants = variants[:] if variants else []

    def __repr__(self):
        return "CompilationSet({}:{})".format(self.name, self.variants)


# --------------VV------------- NOT REFACTORED YET --------------VV-------------

def get_builds(tags, update=False, branches=None, releases=False):
    result = []
    if releases:
        for tag in tags:
            sdk = EMHelper.get_sdk_name_tag(tag)
            result.append(EMBuild(sdk, update))
    for branch in branches:
        sdk = EMHelper.get_sdk_name_branch(branch)
        result.append(EMBuild(sdk, True))
    return result

def handle_build_log(line):
    r = re.match(r'## (.+)', line)
    if r:
        dashboard.set_status(r.groups()[0])
        return

    r = re.match(r'\[\s*(\d+)\%]', line)
    if r:
        dashboard.set_progress(int(r.groups()[0]))
        return

    r = re.match(r'Step (\d+/\d+)', line)
    if r:
        dashboard.set_step(r.groups()[0])
        return

    r = re.match(r'\] Built target (.+)', line)
    if r:
        dashboard.trace(r.groups()[0])
        return

    r = re.match(r'Unpacking (.+) ', line)
    if r:
        dashboard.trace(r.groups()[0])
        return

def build_image(description, no_cache = False):
    # compile: source folder, as tag, argument list, extra options (might be composable)
    if DockerHelper.compile_image(
        description["source"],
        description["build_tag"],
        description["args"],
        log_file=LOG_COMPILATION,
        no_cache=no_cache,
        log_handler=handle_build_log
    ):
        log("Failed to compile")
        return -1

    if EmscriptenTester.test_image(description["build_tag"], description["tests"]):
        log("Failed to test")
        return -1
    # test

    # for t in :
    DockerHelper.tag(description["build_tag"], *description["tags"])

    return 0

def defer_push(image_name):
    queue = open(QUEUE_FILE, 'r').read().splitlines(True) if os.path.isfile(QUEUE_FILE) else []
    queue.insert(0, image_name + "\n")
    with open(QUEUE_FILE, 'w+') as f:
        f.writelines(queue)
        log(f"[INFO] Deferred pushing: {image_name} ")


def get_sdk_to_compile(em_builds, docker_tags):
    result = []
    for b in em_builds:
        if b.docker_tag not in docker_tags:
            b.update = True

        if b.update:
            result.append(b.docker_tag)
    return result


# ------------------------------------------------------------------------------

def get_variants_to_compile(sdks, incoming=False, master=False, branches=False, releases=False):
    # like 1.33.1 or branch name: 'incoming', 'master' - any valid tag that's pushed to emscripten
    versions_to_compile = set()

    # every possible variant that's needed to be compiled
    # Set of EMVariant
    variants_to_compile = set()

    if incoming or branches:
        versions_to_compile.add("incoming")
    if master or branches:
        versions_to_compile.add("master")

    # compile every release that isn't pushed to docker registry
    if releases:
        # List of pushed tags to Docker, in format: ['sdk-master-32bit', 'sdk-tag-1.38.8-64bit', ...]
        docker_tags = DockerHelper.pushed_tags(DOCKER_REGISTRY, DOCKER_REPO)
        # ["1.23.4", ...]
        emscripten_tags = EMHelper.get_emscripten_tags(config["sdk_min"])
        for v in emscripten_tags:
            # TODO: here needs to be updated, once new tagging schema is in place
            if EMHelper.get_sdk_name_tag(v) not in docker_tags:
                versions_to_compile.add(v)

    # if tag was given explicitly, then use it
    for sth in sdks:
        # sdk can be either: full docker image id, or a tag.
        if sth.find(":") >= 0:
            # in this case an explicit version was given.
            name, version = sth.split(":")
            variants_to_compile.add(EMVariant(name, version))
        elif re.match(r'^\d+\.\d+\.\d+$', sth): # it's a version number: 1.12.4
            versions_to_compile.add(sth)
        elif sth in ["master", "incoming"]: # it's a branch name
            versions_to_compile.add(sth)
        else:
            print("Ignoring: '{}' - don't know how to build it.".format(sth))

    # populate variants to compile
    combined_variants = variants_to_compile.union(EMHelper.expand_tags_to_variants(versions_to_compile))
    return list(combined_variants)

def create_compilation_sets(variants):
    """takes a set of possible compilation variants and create a list of atomic sets"""
    """each atomic set contains one or more variants, in order to mark those compilation successful, every variant has to succeeded"""
    sets = dict()

    # simplified logic groups only by version/tag
    # sdk-master-32bit', 'sdk-tag-1.38.8-64bit
    for variant in variants:
        if variant.version not in sets:
            sets[variant.version] = CompilationSet(variant.version)
        sets[variant.version].variants.append(variant)

    result = list(sets.values())
    result = sorted(result, key=cmp_to_key(cmp_name_versions), reverse=False)

    for r in result:
        r.variants = list(sorted(r.variants, key=cmp_to_key(sort_variants), reverse=False))

    return list(result)

def compile(args):
    """Build images, and push tags to the queue"""

    assert(not args.branches)   # not supported ATM
    assert(not args.incoming)   # not supported ATM
    assert(not args.master)     # not supported ATM

    variants = get_variants_to_compile(args.sdks, args.incoming, args.master, args.branches, args.releases)
    sets = create_compilation_sets(variants)


    total_images = 0
    for s in sets:
        dashboard.log("* {}".format(s.name))
        total_images += len(s.variants)
        for v in s.variants:
            dashboard.log("  * {}".format(v))

    success = True
    for s in sets:
        set_compiled = True
        build_descriptions = []
        for i, v in enumerate(s.variants):
            dashboard.set_task(v.name, i + 1, len(s.variants))
            registries = [
                config["registries"]["docker"]
            ]
            if args.push_gh: registries.append(config["registries"]["github"])
            description = get_build_description(v, registries, emsdk_cs=args.emsdk_cs)

            if not build_image(description, no_cache=args.no_cache):
                build_descriptions.append(description)
                log(f"{v} - SUCCESS", True)
            else:
                log(f"{v} - FAIL", True)
                set_compiled = False
                break

        if set_compiled:
            # reversed, because defer push always puts new element in front of queue.
            for description in build_descriptions[::-1]:
                for tag in description["tags"]:
                    defer_push(tag)
        else:
            success = False
            if args.fast_fail:
                break

    if not success:
        log("At least one compilation set has failed to compile", True)
        exit(1)

def list_installed_packages(image):
    fetch_script = ""
    if not subprocess.call(["docker", "run", "--rm", image, "cat", "/etc/debian_version"], stdout=PIPE, stderr=PIPE):
        fetch_script="./scripts/list_packages_debian.sh"
    else:
        print("Unknown base system, can't handle packages")

    if fetch_script:
        output = subprocess.check_output([
            "docker", "run", "--rm",
            "-v", "{}:{}".format(os.path.join(ROOT), "/src"),
            "-w", "/src",
            image,
            fetch_script
        ]).decode().strip()
        output = "\n".join([
            f"|`{pair[0]}`|**{pair[1]}**|" for pair in map(lambda x: x.split(":"), output.split("\n"))
        ])
        return f"|package|version|\n|---|---|\n{output}"
    return ""

def set_latest(args):
    registry = DockerRegistry()
    registry.login()
    for repo in get_variants():
        docker_tags = DockerHelper.pushed_tags(DOCKER_REGISTRY, repo)
        docker_tags = list(set(filter(lambda x: re.match(r'sdk-tag-(\d+\.\d+\.\d+)-64bit', x), docker_tags)))
        docker_tags = list(map(lambda x: re.match(r'.+(\d+\.\d+\.\d+).+', x).groups()[0], docker_tags))
        docker_tags = sorted(docker_tags, key=cmp_to_key(version_compare), reverse=True)
        if len(docker_tags) < 0: continue

        tag = f"sdk-tag-{docker_tags[0]}-64bit"
        digest_latest = registry.get_digest(repo, "latest")
        digest_recent = registry.get_digest(repo, tag)

        if digest_latest != digest_recent or args.force:
            subprocess.call([f"docker pull {repo}:{tag}"], shell=True)
            subprocess.call([f"docker tag {repo}:{tag} {repo}:latest"], shell=True)
            subprocess.call([f"docker push {repo}:latest"], shell=True)
            log(f"[{repo}]: Set latest to: {tag}", True)
        else:
            log(f"[{repo}]: Tag 'latest' already points at: {tag}", True)

        # Update description
        description_short = config["images"][index_image_name(repo)]["short"]
        long_from_file = config["images"][index_image_name(repo)]["long_from_file"]

        description_long = ""
        with open(long_from_file, "r") as f: description_long = f.read()
        description_long += "\n<!-- footer -->"

        properties = {
            "installed_packages": list_installed_packages(f"{repo}:{tag}"),
            "footer": f"-----\nGenerated by {pwd.getpwuid(os.getuid())[0]}: " + datetime.datetime.now().isoformat(),
        }

        for k, v in properties.items():
            description_long = description_long.replace(f"<!-- {k} -->", v)

        registry.update_description(repo, description_short, description_long)


def push(args):
    """Push created tags, what are waiting in queue document """
    while True:
        pushed = False
        if os.path.exists(QUEUE_FILE):
            with open(QUEUE_FILE, 'r') as fin:
                data = fin.read().splitlines(True)
            if len(data):
                tag_to_send = data[0].strip()
                with open(QUEUE_FILE, 'w') as fout:
                    fout.writelines(data[1:])
                if tag_to_send:
                    if DockerHelper.push_image(tag_to_send):
                        log(f"[ERROR] Pushing {tag_to_send} failed.")
                    else:
                        log(f"[INFO] Pushed tag: {tag_to_send}")
                        if args.clean:
                            DockerHelper.rmi(tag_to_send)
                            log(f"[INFO] Removed tag: {tag_to_send}")
                    pushed = True
        if not pushed and args.no_block:
            log("[INFO] Nothing to do here, queue is empty")
            break
        time.sleep(2)


dashboard = Dashboard()
def main():
    parser = argparse.ArgumentParser(description='Emscripten Image generator')
    subparsers = parser.add_subparsers(title="command", help="Main work command")

    parser_build = subparsers.add_parser("compile", help="Compile Docker images.")
    parser_build.set_defaults(function=compile)
    parser_build.add_argument("sdks", type=str, nargs='*', help="List of images to compile, either just version (1.38.32) or explicit path: (trzeci/emscripten:1.38.31)")
    parser_build.add_argument("--branches", action="store_true", help="Update master and incoming images")

    parser_build.add_argument("--master", action="store_true", help="Update master images")     # FIXME: unsupported
    parser_build.add_argument("--incoming", action="store_true", help="Update incoming images") # FIXME: unsupported

    parser_build.add_argument("--releases", action="store_true", help="Update released SDKs")
    parser_build.add_argument("--fast-fail", action="store_true", help="Stops queue after first failure")
    parser_build.add_argument("--emsdk-cs", default="master", help="Explicitly use given branch/changeset of juj/emsdk")
    parser_build.add_argument("--push-gh", action="store_true", help="Push also to GH registry")
    parser_build.add_argument("--no-cache", action="store_true", help="Sets --no-cache for docker build command")

    parser_push = subparsers.add_parser("push", help="Runs a service what will push created images")
    parser_push.add_argument("--clean", action="store_true", help="Remove pushed images")
    parser_push.add_argument("--no-block", action="store_true", help="Don't wait if queue is empty")
    parser_push.set_defaults(function=push)

    parser_set_latest = subparsers.add_parser("set_latest", help="Automatically sets the 'latest' tag")
    parser_set_latest.add_argument("--force", action="store_true", help="Ignore comparing digests")
    parser_set_latest.set_defaults(function=set_latest)

    args = parser.parse_args()
    args.function(args)

if __name__ == "__main__":
    main()

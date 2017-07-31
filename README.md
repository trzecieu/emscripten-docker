[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten.svg)](https://store.docker.com/community/images/trzeci/emscripten/)

### Emscripten Docker images generator

Generator for Docker image dedicated to run emscripten.

This has to be run manually on dedicated machine, because a compilation process of building Emscipten takes ~1h. What is more than a limit of execution for auto builds on the Docker Hub.

DockerHub: https://hub.docker.com/r/trzeci/emscripten/

- [x] Creates all releases from tag
- [x] Support for 64 and 32 releases
- [x] auto publish images
- [x] Validate generated images
- [x] Add a job that handles: "incoming" and "master" branches
- [ ] Dedicate some device that runs onece per day and update branch builds.


### Usage

```
./build --help
usage: build [-h] [--no-32] [--no-64] [--update] [--branches] [--releases]
             [--pusher]
             [tags [tags ...]]

Emscripten Image generator

positional arguments:
  tags        Explicitly provide list of tags in format X.Y.Z, i.e.: 1.34.5

optional arguments:
  -h, --help  show this help message and exit
  --no-32     Explicitly disable 32 images
  --no-64     Explicitly disable 64 images
  --update    Update docker images that are arleady created and pushed
  --branches  Update master and incomming images
  --releases  Update released SDKs
  --pusher    Pushes tags created by regular command
```

For the instance, to build all tags that aren't build yet:
```
$terminal_1: ./build --releases --branches
```
```
$terminal_2: ./build --pusher
```

### License
MIT


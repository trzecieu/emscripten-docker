# Docker: emscripten
[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten.svg)](https://store.docker.com/community/images/trzeci/emscripten/) [![Size](https://images.microbadger.com/badges/image/trzeci/emscripten.svg)](https://microbadger.com/images/trzeci/emscripten/)


A complete container that is required to compile C++ code with [Emscripten](http://emscripten.org). The goal was to provide a container that includes the most popular development packages and it's also easy to extend.
Since tag 1.37.16 this container bases on https://hub.docker.com/r/trzeci/emscripten-slim/

## Structure
Each tag was build from [Dockerfile](https://github.com/trzecieu/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile)
* Base system: **trzeci/emscripten-slim**
* Installed packages:
  * `ant` : **1.9.9-1+deb9u1**
  * `build-essential` : **12.3**
  * `ca-certificates` : **20161130+nmu1+deb9u1**
  * `curl` : **7.52.1-5+deb9u9**
  * `gcc` : **4:6.3.0-4**
  * `git` : **1:2.11.0-3+deb9u4**
  * `iproute2` : **4.9.0-1+deb9u1**
  * `iputils-ping` : **3:20161105-1**
  * `libidn11` : **1.33-1**
  * `make` : **4.1-9.1**
  * `openjdk-8-jre-headless` : **8u181-b13-2~deb9u1**
  * `openssh-client` : **1:7.4p1-10+deb9u4**
  * `python` : **2.7.13-2**
  * `python-pip` : **9.0.1-2**
  * `unzip` : **6.0-21**
  * `wget` : **1.18-5+deb9u2**
  * `zip` : **3.0-11+b1**
* Extra packages:
  * `cmake`: **3.14.3**

## Tag schema
### latest
The default version (aka `latest`) points at [the latest tagged release](https://github.com/kripken/emscripten/releases) by Emscripten. 

### Version release
`sdk-tag-{VERSION}-{BITS}`
* **VERSION**: One of the official [Emscripten tag](https://github.com/kripken/emscripten/tags) released since 1.34.1
* **BITS**: `["32bit", "64bit"]`
Example: `sdk-tag-1.34.4-64bit`

### Branch release
`sdk-{BRANCH}-{BITS}`
* **BRANCH**: `["incoming", "master"]`
* **BITS**: `["32bit", "64bit"]`
Example: `sdk-master-32bit`


## Usage
Start volume should be mounted in `/src`. 
For start point every Emscripten command is available. For the instance: `emcc`, `em++`, `emmake`, `emar` etc.

To compile a single file:
`docker run --rm -v $(pwd):/src trzeci/emscripten emcc helloworld.cpp -o helloworld.js --closure 1`

Hello World:
```bash
printf '#include <iostream>\nint main() { std::cout<<"HELLO FROM DOCKER C++"<<std::endl; return 0; }' > helloworld.cpp

docker run \
  --rm \
  -v $(pwd):/src \
  -u emscripten \
  trzeci/emscripten \
  emcc helloworld.cpp -o helloworld.js --closure 1

node helloworld.js
```

Teardown of compilation command:

|part|description|
|---|---|
|`docker run`| A standard command to run a command in a container|
|`--rm`|remove a container after execution|
|`-v $(pwd):/src`|Mounting current folder from the host system, into `/src` of the image|
|`-u emscripten`|(1.37.23+) Run a container as a non-root user `emscripten`, hence all files produced by this are accessible to non-root users|
|`trzeci/emscripten`|Get the latest tag of this container|
|`emcc helloworld.cpp -o helloworld.js --closure 1`|Execute emcc command with following arguments inside container|


## How to compile?
0. Pull the latest https://github.com/trzecieu/emscripten-docker
0. [Optional] To be extra accurate, you can check which version of [EMSDK](https://github.com/juj/emsdk) was used in a particular image. For older images you can check [a file](https://github.com/trzecieu/emscripten-docker/blob/master/emscripten_to_emsdk_map.md) otherwise for images 1.38.9+ execute a command `docker run --rm -it trzeci/emscripten:sdk-tag-1.38.9-64bit bash -c "git -C /emsdk_portable rev-parse HEAD"`
0. Compile [Dockerfile](https://github.com/trzecieu/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile)

Helper command: `./build compile trzeci/emscripten:sdk-tag-1.37.17-64bit` (where `sdk-tag-1.37.17-64bit` is an arbitrary tag)

## Support 
* **GitHub / Issue tracker**: https://github.com/trzecieu/emscripten-docker
* **Docker: emscripten**: https://hub.docker.com/r/trzeci/emscripten/
* **Docker: emscripten-slim**: https://hub.docker.com/r/trzeci/emscripten-slim/

## History
* **1.38.30** [#40](https://github.com/trzecieu/emscripten-docker/issues/40) Fixed image compilation problem caused by JRE backport package
* **1.38.22** [#35](https://github.com/trzecieu/emscripten-docker/issues/35) upgrade to `cmake` 3.12.2
* **1.38.17** Version ignored due problems with [Emscripten]
* **1.38.9** `/emsdk_portable` will be preserved as a git repos (with valid version of changeset)
* **1.38.7** Version removed due problems with [emsdk](https://github.com/juj/emsdk/pull/156)
* **1.37.29** upgrade to `cmake` 3.7.2
* **1.37.23** Added `curl`, `zip`, `unzip`, upgrade to openjdk-jre-8
* **1.37.21** Fixed missing `ctest` command
* **1.37.21** image includes `ssh` and cache of libc libcxx is fixed. 
* **1.37.19** image doesn't use entrypoint from the base image.
* **1.37.18** it contains `perl` and `git` package
* **1.37.16** images are compiled from singe [Dockerfile](https://github.com/trzecieu/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile).
* **1.37.10** images are bundled with `java`
* **1.36.7** images are bundled with `make` and `nodejs`
* **1.36.7** images are bundled with `cmake` 3.6.3, images are build from generated [Dockerfiles](https://github.com/trzecieu/emscripten-docker/tree/f738f061c8068ec24124c37286eafec01d54a6ef/configs)
* **1.35.0** images base on Debian
* **1.34.X** images base on Ubuntu:15.10

### License
MIT

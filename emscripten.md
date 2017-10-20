# Docker: emscripten
[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten.svg)](https://store.docker.com/community/images/trzeci/emscripten/) [![Size](https://images.microbadger.com/badges/image/trzeci/emscripten.svg)](https://microbadger.com/images/trzeci/emscripten/)


A complete container what is required to compile C++ code with [Emscripten](http://emscripten.org). The goal was to provide the best foundation for custom Docker images.
Since tag 1.37.16 this container bases on https://hub.docker.com/r/trzeci/emscripten-slim/

## Structure
Each tag was build from [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile)
* Base system: **trzeci/emscripten-slim:**
* Installed packages: 
  * `python`: **2.7**
  * `nodejs`: **4.1.1_64bit** (from EMSDK)
* Extra packages: 
  * `cmake`: **3.6.3**
  * `make`: **4.0**
  * `java`: **OpenJDK 1.7.0_131**
  * `git`: **2.1.4**
  * `ant`: **1.9.4**
  * `perl`: **5**
  * `ssh`
  * `curl`
  * `wget`
  * `zip`
  * `unzip`
  * `ca-certificates`
  * `build-essential`

## Tag schema
### latest
Currently latest tag is not available. Not decided yet it should point either on the latest master, or latest official release. 

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


## How to use the image?
Start volume should be mounted in `/src`. 
For start point every Emscripten command is available. For the instance: emcc, em++, emmake, emar etc.

To compile a single file:
`docker run --rm -v $(pwd):/src trzeci/emscripten:sdk-tag-1.37.19-64bit emcc helloworld.cpp -o helloworld.js --closure 1`

Hello World:
```bash
printf '#include <iostream>\nint main() { std::cout<<"HELLO FROM DOCKER C++"<<std::endl; return 0; }' > helloworld.cpp
docker run --rm -v $(pwd):/src trzeci/emscripten:sdk-tag-1.37.19-64bit emcc helloworld.cpp -o helloworld.js --closure 1
node helloworld.js
```

## How to compile?
0. Pull the latest https://github.com/asRIA/emscripten-docker
0. Compile [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile)

Helper command: `./build compile trzeci/emscripten:sdk-tag-1.37.17-64bit` (where `sdk-tag-1.37.17-64bit` is an arbitrary tag)

## Support 
* **GitHub / Issue tracker**: https://github.com/asRIA/emscripten-docker
* **Docker: emscripten**: https://hub.docker.com/r/trzeci/emscripten/
* **Docker: emscripten-slim**: https://hub.docker.com/r/trzeci/emscripten-slim/

## History
* **1.37.23** Added `curl`, `zip`, `unzip`
* **1.37.21** Fixed missing `ctest` command
* since **1.37.21** image includes `ssh` and cache of libc libcxx is fixed. 
* since **1.37.19** image doesn't use entrypoint from the base image.
* since **1.37.18** it contains `perl` and `git` package
* since **1.37.16** images are compiled from singe [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile).
* since **1.37.10** images are bundled with `java`
* since **1.36.7** images are bundled with `make` and `nodejs`
* since **1.36.7** images are bundled with `cmake` 3.6.3, images are build from generated [Dockerfiles](https://github.com/asRIA/emscripten-docker/tree/f738f061c8068ec24124c37286eafec01d54a6ef/configs)
* since **1.35.0** images base on Debian
* since **1.34.X** images base on Ubuntu:15.10

### License
MIT

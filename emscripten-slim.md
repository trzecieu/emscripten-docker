# Docker: emscripten-slim
[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten-slim.svg)](https://store.docker.com/community/images/trzeci/emscripten-slim/) [![Size](https://images.microbadger.com/badges/image/trzeci/emscripten-slim.svg)](https://microbadger.com/images/trzeci/emscripten-slim/)

The minimal version what is require to compile C++ code with [Emscripten](http://emscripten.org) to ASM.js or WebAssembly. The goal was to provide the best foundation for custom Docker images. 
This version has been utilized as a base version for https://hub.docker.com/r/trzeci/emscripten/ since 1.37.16 tags.

## Structure
Each tag was build from [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten-slim/Dockerfile)
* Base system: **debian:jessie**
* Installed packages: 
  * `python`: **2.7**
  * `nodejs`: **4.1.1_64bit** (from EMSDK)

`debian:jessie` has been chosen as a base system due it's popularity. Image has been optimized in order to have the lowest possible size.

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


## Usage
Start volume should be mounted in `/src`. 
For start point every Emscripten command is available. For the instance: emcc, em++, emmake, emar etc.

To compile single file it could be called like:
`docker run --rm -v $(pwd):/src trzeci/emscripten-slim:sdk-tag-1.37.19-64bit emcc helloworld.cpp -o helloworld.js`

Hello World:
```bash
printf '#include <iostream>\nint main() { std::cout<<"HELLO FROM DOCKER C++"<<std::endl; return 0; }' > helloworld.cpp
docker run --rm -v $(pwd):/src trzeci/emscripten-slim:sdk-tag-1.37.19-64bit emcc helloworld.cpp -o helloworld.js
node helloworld.js
```

## How to extend this image?
Good example of extending this image you can find here: https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile
Basically it requires to create own Dockerfile what stats with: 
```Dockerfile
FROM trzeci/emscripten-slim:sdk-tag-1.37.19-64bit
# Where sdk-tag-1.37.19-64bit is an arbitrary version what you would like to extend

RUN ...

```
Doing so, don't forget about https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/ 

## How to compile?
0. Pull the latest https://github.com/asRIA/emscripten-docker
0. Compile [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten-slim/Dockerfile)

Helper command: `./build compile trzeci/emscripten-slim:sdk-tag-1.37.19-64bit` (where `sdk-tag-1.37.19-64bit` is an arbitrary tag)

## Support 
* **GitHub / Issue tracker**: https://github.com/asRIA/emscripten-docker
* **Docker: emscripten**: https://hub.docker.com/r/trzeci/emscripten/
* **Docker: emscripten-slim**: https://hub.docker.com/r/trzeci/emscripten-slim/

## History
* since **1.37.19** Entrypoint (`/entrypoint`) is removed, what simplifies setup and adds a compatibility to CircleCI. [#12](https://github.com/asRIA/emscripten-docker/pull/12)
* since **1.37.16** the image is compiled from singe [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten-slim/Dockerfile).


### License
MIT

# Docker: emscripten-slim
[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten-slim.svg)](https://store.docker.com/community/images/trzeci/emscripten-slim/) [![Size](https://images.microbadger.com/badges/image/trzeci/emscripten-slim.svg)](https://microbadger.com/images/trzeci/emscripten-slim/)

The minimal version what is required to compile C++ code with [Emscripten](http://emscripten.org) to ASM.js or WebAssembly (WASM). The goal was to provide the best and the most lightweight foundation for custom Docker images. 
This version has been utilized as a base version for https://hub.docker.com/r/trzeci/emscripten/ since 1.37.16 tag.

## Structure
Each tag was build from one [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten-slim/Dockerfile)
* Base system: **debian:jessie**
* Installed packages: 
  * `python`: **2.7**
  * `nodejs`: **4.1.1_64bit** (from EMSDK)

`debian:jessie` has been chosen as a base system due its popularity. Image has been optimized in order to have the lowest possible size.

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
`docker run --rm -v $(pwd):/src trzeci/emscripten-slim emcc helloworld.cpp -o helloworld.js`

Hello World:
```bash
printf '#include <iostream>\nint main() { std::cout<<"HELLO FROM DOCKER C++"<<std::endl; return 0; }' > helloworld.cpp

docker run \
  --rm \
  -v $(pwd):/src \
  -u emscripten \
  trzeci/emscripten-slim \
  emcc helloworld.cpp -o helloworld.js

node helloworld.js
```

Teardown of compilation command: 
part|description
|---|---|
|`docker run`| A standard command to run a command in a container|
|`--rm`|remove a container after execution|
|`-v $(pwd):/src`|Mounting current folder from the host system, into `/src` of the image|
|`-u emscripten`|(1.37.23+)Run a container as a non-root user `emscripten`, hence all files produced by this are accessible to non-root users|
|`trzeci/emscripten-slim`|Get the latest tag of this container|
|`emcc helloworld.cpp -o helloworld.js`|Execute emcc command with following arguments inside container|


## How to extend this image?
Good example of extending this image you can find here: https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile
Basically it requires to create own Dockerfile what stats with: 
```Dockerfile
FROM trzeci/emscripten-slim:sdk-tag-1.37.19-64bit
# Where sdk-tag-1.37.19-64bit is an arbitrary version what you would like to extend

RUN ...

```
Doing so, don't forget about [Dockerfile best practices](https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/)

## How to compile?
0. Pull the latest https://github.com/asRIA/emscripten-docker
0. Compile [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten-slim/Dockerfile)

Helper command: `./build compile trzeci/emscripten-slim:sdk-tag-1.37.19-64bit` (where `sdk-tag-1.37.19-64bit` is an arbitrary tag)

## Support 
* **GitHub / Issue tracker**: https://github.com/asRIA/emscripten-docker
* **Docker: emscripten**: https://hub.docker.com/r/trzeci/emscripten/
* **Docker: emscripten-slim**: https://hub.docker.com/r/trzeci/emscripten-slim/

## History
* **1.37.23** Moved all mutable files to `$EM_DATA`, created an user emscripten:emscripten (1000:1000)
* **1.37.21** Fixed missing `npm` command and changed permission to `$EM_CACHE` to 775
* **1.37.19** Entrypoint (`/entrypoint`) is removed, what simplifies setup and adds a compatibility to CircleCI. [#12](https://github.com/asRIA/emscripten-docker/pull/12)
* **1.37.16** the image is compiled from singe [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten-slim/Dockerfile).

### License
MIT

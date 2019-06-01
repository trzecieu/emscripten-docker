# Docker: emscripten
Based on: **[trzeci/emscripten-slim](https://hub.docker.com/r/trzeci/emscripten-slim)**

[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten.svg?style=flat-square)](https://store.docker.com/community/images/trzeci/emscripten/) [![Size](https://images.microbadger.com/badges/image/trzeci/emscripten.svg)](https://microbadger.com/images/trzeci/emscripten/)

A complete container that is required to compile C++ code with [Emscripten](http://emscripten.org). The goal was to provide a container that includes the most popular development packages and it's also easy to extend.
Each tag was build from [Dockerfile](https://github.com/trzecieu/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile)

## Packages

### Manually installed:

|pacakage|version|
|---|---|
|`cmake`|**3.14.3**|

### System packages:

<!-- installed_packages -->

## Tag schema
### latest
The default version (aka `latest`) points at [the latest tagged release](https://github.com/emscripten-core/emscripten/releases) by Emscripten.

### Version release
`sdk-tag-{VERSION}-{BITS}`
* **VERSION**: One of the official [Emscripten tag](https://github.com/emscripten-core/emscripten/tags) released since 1.34.1
* **BITS**: `["32bit", "64bit"]`
Example: `sdk-tag-1.34.4-64bit`

### Branch release
`sdk-{BRANCH}-{BITS}`
* **BRANCH**: `["incoming", "master"]`
* **BITS**: `["32bit", "64bit"]`
Example: `sdk-master-64bit`

Please note: **32bit** is not longer released by this image

## Usage
Start volume should be mounted in `/src`.
For start point every Emscripten command is available. For the instance: `emcc`, `em++`, `emmake`, `emar` etc.

To compile a single file:
`docker run --rm -v $(pwd):/src trzeci/emscripten emcc helloworld.cpp -o helloworld.js --closure 1`

Hello World:
```bash
cat << EOF > helloworld.cpp
#include <iostream>
int main() {
  std::cout << "HELLO FROM DOCKER C++" << std::endl;
  return 0;
}
EOF

docker run \
  --rm \
  -v $(pwd):/src \
  -u $(id -u):$(id -g) \
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
|`-u $(id -u):$(id -g)`|(1.37.23+) Run a container as a non-root user with the same UID and GID as local user. Hence all files produced by this are accessible to non-root users|
|`trzeci/emscripten`|Get the latest tag of this container|
|`emcc helloworld.cpp -o helloworld.js --closure 1`|Execute emcc command with following arguments inside container|


## How to compile?
0. Pull the latest https://github.com/trzecieu/emscripten-docker
0. [Optional] To be extra accurate, you can check which version of [EMSDK](https://github.com/juj/emsdk) was used in a particular image. For older images you can check [a file](https://github.com/trzecieu/emscripten-docker/blob/master/emscripten_to_emsdk_map.md) otherwise for images 1.38.9+ execute a command `docker run --rm -it trzeci/emscripten:sdk-tag-1.38.9-64bit bash -c "git -C /emsdk_portable rev-parse HEAD"`
0. Compile [Dockerfile](https://github.com/trzecieu/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile)

Helper command: `./build compile trzeci/emscripten:sdk-tag-1.37.17-64bit` (where `sdk-tag-1.37.17-64bit` is an arbitrary tag)

## Support
* **GitHub / Issue tracker**: https://github.com/trzecieu/emscripten-docker
* **Docker Hub: emscripten**: https://hub.docker.com/r/trzeci/emscripten/
* **Docker Hub: emscripten-slim**: https://hub.docker.com/r/trzeci/emscripten-slim/

## History
<sub>(Please note that following history refers only to the history of this Docker Image and how it was build / what includes. For release notes of emscripten, please follow https://emscripten.org)</sub>

* **1.38.33**: [#44](https://github.com/trzecieu/emscripten-docker/issues/44) Significant refactoring of base image emscripten-slim. Which includes:
  * Improvements:
    * `/emsdk_portable` is fully moveable folder that can be used as a `COPY --from` source of multi stage build
    * `/emsdk_portable/dockerfiles` contains Dockerfile sources used to compile a particular image - so that it should be fairly easy to replicate and inspect content of images
    * `emsdk` should be fully functional tool now, so that can be used for upgrading bundled emscripten SDK or to install extra tools
    * Even further size optimization by stripping out symbols from node.js and emscripten-clang tools

  * Breaking Changes:
    * Image has to be executed with boundled entrypoint (`/emsdk_portable/emscripten`)
    * Image no longer creates system symbolic links
    * Image no longer preserves folder structure between versions (like Clang tools were always placed in `/emsdk_portable/llvm`)
    * `nodejs` is no longer symlinked (`node` should be used instead)
    * If image is accessed bypassing entrypoint, then `$EMSCRIPTEN` environment variable isn't set.

Please follow GitHub issue for more information.
* **1.38.30**: [#40](https://github.com/trzecieu/emscripten-docker/issues/40) Fixed image compilation problem caused by JRE backport package
* **1.38.22**: [#35](https://github.com/trzecieu/emscripten-docker/issues/35) upgrade to `cmake` 3.12.2
* **1.38.17**: Version ignored due problems with [Emscripten]
* **1.38.9**: `/emsdk_portable` will be preserved as a git repos (with valid version of changeset)
* **1.38.7**: Version removed due problems with [emsdk](https://github.com/juj/emsdk/pull/156)
* **1.37.29**: upgrade to `cmake` 3.7.2
* **1.37.23**: Added `curl`, `zip`, `unzip`, upgrade to openjdk-jre-8
* **1.37.21**: Fixed missing `ctest` command
* **1.37.21**: image includes `ssh` and cache of libc libcxx is fixed.
* **1.37.19**: image doesn't use entrypoint from the base image.
* **1.37.18**: it contains `perl` and `git` package
* **1.37.16**: images are compiled from singe [Dockerfile](https://github.com/trzecieu/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile).
* **1.37.10**: images are bundled with `java`
* **1.36.7**: images are bundled with `make` and `nodejs`
* **1.36.7**: images are bundled with `cmake` 3.6.3, images are build from generated [Dockerfiles](https://github.com/trzecieu/emscripten-docker/tree/f738f061c8068ec24124c37286eafec01d54a6ef/configs)
* **1.35.0**: images base on Debian
* **1.34.X**: images base on Ubuntu:15.10

## License
[![MIT](https://img.shields.io/github/license/trzecieu/emscripten-docker.svg?style=flat-square)](https://github.com/trzecieu/emscripten-docker/blob/master/LICENSE)

-----
<!-- footer -->

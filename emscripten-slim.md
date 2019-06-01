# Docker: emscripten-slim
Based on: **debian:stretch-slim**

[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten-slim.svg?style=flat-square)](https://store.docker.com/community/images/trzeci/emscripten-slim/) [![Size](https://images.microbadger.com/badges/image/trzeci/emscripten-slim.svg)](https://microbadger.com/images/trzeci/emscripten-slim/)

The minimal version that is required to compile C++ code with [Emscripten](http://emscripten.org) to ASM.js or WebAssembly (WASM). The goal was to provide the best and the most lightweight foundation for custom Docker images.
Each tag was build from [Dockerfile](https://github.com/trzecieu/emscripten-docker/blob/master/docker/trzeci/emscripten-slim/Dockerfile)

## Packages

### Manually installed:

|pacakage|version|
|---|---|
|`nodejs`|**8.9.1_64bit** (from EMSDK)|

### System installed:

<!-- installed_packages -->

## Tag schema
|tag|description|
|--|--|
|`latest`|The default version (aka `latest`) points at [the latest tag release](https://github.com/emscripten-core/emscripten/releases) by Emscripten.|
|`sdk-tag-{VERSION}-64bit`| Tag release:<br>- **VERSION**: One of the official [Emscripten tag](https://github.com/emscripten-core/emscripten/tags) released since 1.34.1|
|`sdk-{BRANCH}-64bit`|Branch release:<br>- **BRANCH**: `["incoming", "master"]`|


## Usage
Start volume might be mounted in `/src`, but I prefer to mirror my local path (then it's easier to look for compilation errors)
For start point every Emscripten command is available. For the instance: `emcc`, `em++`, `emmake`, `emar` etc.

To compile a single file:
```bash
docker run --rm -v `pwd`:`pwd` trzeci/emscripten-slim emcc helloworld.cpp -o helloworld.js
```

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
  -v $(pwd):$(pwd) \
  -u $(id -u):$(id -g) \
  trzeci/emscripten-slim \
  emcc helloworld.cpp -o helloworld.js

node helloworld.js
```

Teardown of compilation command:

|part|description|
|---|---|
|`docker run`| A standard command to run a command in a container|
|`--rm`|remove a container after execution|
|`-v $(pwd):$(pwd)`|Mounting current folder from the host system, into mirrored path on the image|
|`-u $(id -u):$(id -g)`|(1.37.23+) Run a container as a non-root user with the same UID and GID as local user. Hence all files produced by this are accessible to non-root users|
|`trzeci/emscripten-slim`|Get the latest tag of this container|
|`emcc helloworld.cpp -o helloworld.js`|Execute emcc command with following arguments inside container|

## Extending this image
If you would like to extend this image you have two choices:
### Extend: Keep base image
An example how to derive from base image and keep linux base container you can find here - [emscripten](./docker/trzeci/emscripten/Dockerfile).

 Then all what you need is:
```Dockerfile
FROM trzeci/emscripten-slim:latest
RUN ...
```
### Change base image
An example how to derive from base image and switch linux base container you can find here - [emscripten-ubuntu](./docker/trzeci/emscripten-ubuntu/Dockerfile).

In case if you'd like to create a different image that contains pre-compiled emscripten you can use multistage Docker file.
For example let's create fedora base image:
```dockerfile
FROM trzeci/emscripten-slim:sdk-tag-1.38.25-64bit as emscripten_base
# ----
FROM fedora
COPY --from=emscripten_base /emsdk_portable /emsdk_portable

# install required tools to run Emscripten SDK
RUN dnf install -y python python-pip ca-certificates

ENTRYPOINT ["/emsdk_portable/entrypoint"]
```
That's all! All you need is to copy content from `/emsdk_portable` to the same folder in your image.
Then it's important to use `/emsdk_portable/entrypoint` as it contains some nice fixes for non-root file access rights.
Alternatively you can also call:
```bash
. /emsdk_portable/emsdk_set_env.sh
```
in your entrypoint - it will work just fine!

#### Entrypoint
Important step is to activate Emscripten SDK - so that tools are available for usage.
Most traditional way is to use entrypoint and this image provides one:
```dockerfile
ENTRYPOINT ["/emsdk_portable/entrypoint"]
```

#### Entypoint-less
In case when you can't override entrypoint, or you have to have Emscripten Ready as a docker stage step, you might use an alternative method - let's say static activation.
For that instead of adding `ENTRYPOINT`, you need to add:
```dockerfile
# Setup Emscripten Environment variables
ENV EMSDK /emsdk_portable
ENV EMSCRIPTEN=${EMSDK}/emscripten/sdk

ENV EM_DATA ${EMSDK}/.data
ENV EM_CONFIG ${EMSDK}/.emscripten
ENV EM_CACHE ${EM_DATA}/cache
ENV EM_PORTS ${EM_DATA}/ports

# Expose tools to system PATH
ENV PATH="${EMSDK}:${EMSDK}/emscripten/sdk:${EMSDK}/llvm/clang/bin:${EMSDK}/node/current/bin:${EMSDK}/binaryen/bin:${PATH}"
```

Basically you can use whatever base system of choice and copy content of `/emsdk_portable` from either `emscripten` or `emscripten-slim` and start use it.

## How to compile?
0. Pull the latest https://github.com/trzecieu/emscripten-docker
0. [Optional] To be extra accurate, you can check which version of [EMSDK](https://github.com/juj/emsdk) was used in a particular image. For older images you can check [a file](https://github.com/trzecieu/emscripten-docker/blob/master/emscripten_to_emsdk_map.md) otherwise for images 1.38.9+ execute a command `docker run --rm -it trzeci/emscripten:sdk-tag-1.38.9-64bit bash -c "git -C /emsdk_portable rev-parse HEAD"`
0. Compile [Dockerfile](https://github.com/trzecieu/emscripten-docker/blob/master/docker/trzeci/emscripten-slim/Dockerfile)
<!-- TODO: Add instruction about  -->
Helper command: `./build compile trzeci/emscripten-slim:sdk-tag-1.37.19-64bit` (where `sdk-tag-1.37.19-64bit` is an arbitrary tag)

## Support
* **GitHub / Issue tracker**: https://github.com/trzecieu/emscripten-docker
* **Docker: emscripten**: https://hub.docker.com/r/trzeci/emscripten/
* **Docker: emscripten-slim**: https://hub.docker.com/r/trzeci/emscripten-slim/

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
* **1.38.26** [#36](https://github.com/trzecieu/emscripten-docker/issues/36) - Reduce image size from 330MB to 189MB
* **1.38.20** [#34](https://github.com/trzecieu/emscripten-docker/issues/34) - Fix error when `emcc` tries to read internal documentation
* **1.38.17** Version ignored due problems with [Emscripten]
* **1.38.13** Base image changed to **debian:stretch**
* **1.38.9** `/emsdk_portable` will be preserved as a git repos (with valid version of changeset)
* **1.38.7** Version removed due problems with [emsdk]
* **1.37.34** [#27](https://github.com/trzecieu/emscripten-docker/issues/27) - Keep `ca-certificates` to allow Python accessing https
* **1.37.33** [#25](https://github.com/trzecieu/emscripten-docker/pull/25) - Preserve libclang.so and libLTO.so
* **1.37.28** [#22](https://github.com/trzecieu/emscripten-docker/issues/22) - Switched to Node 8.9.1
* **1.37.23** Moved all mutable files to `$EM_DATA`, created an user emscripten:emscripten (1000:1000)
* **1.37.21** Fixed missing `npm` command and changed permission to `$EM_CACHE` to 775
* **1.37.19** Entrypoint (`/entrypoint`) is removed, what simplifies setup and adds a compatibility to CircleCI. [#12](https://github.com/trzecieu/emscripten-docker/pull/12)
* **1.37.16** the image is compiled from singe [Dockerfile](https://github.com/trzecieu/emscripten-docker/blob/master/docker/trzeci/emscripten-slim/Dockerfile).

## License
[![MIT](https://img.shields.io/github/license/trzecieu/emscripten-docker.svg?style=flat-square)](https://github.com/trzecieu/emscripten-docker/blob/master/LICENSE)

-----
<!-- footer -->
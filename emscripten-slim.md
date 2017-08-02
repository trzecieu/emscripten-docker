# Docker: emscripten-slim
[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten-slim.svg)](https://store.docker.com/community/images/trzeci/emscripten-slim/) [![Size](https://images.microbadger.com/badges/image/trzeci/emscripten-slim.svg)](https://microbadger.com/images/trzeci/emscripten-slim/)

The minimal version what is require to compile C++ code with [Emscripten](http://emscripten.org). The goal was to provide the best foundation for custom Docker images. 
This version has been utilized as a base version for https://hub.docker.com/r/trzeci/emscripten/ for tags 1.37.16 and newer.

## Structure
Each tag was build from [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/Dockerfile)
* Base system: **debian:jessie**
* Installed packages: 
  * `python`: 2.7
  * `nodejs`: 4.1.1_64bit (from EMSDK)

`debian:jessie` has been chosen in order to have the latest ImageMagick. It is not a part of this image but this image could be easy extend to pull it. Image has been optimised in order to have the lowest possible size.

## Tag schema
#### latest
Currently latest tag is not available. Not decided yet it should point either on the latest master, or latest official release. 

#### Version release
`sdk-tag-{VERSION}-{BITS}`
* **VERSION**: One of the official [Emscripten tag](https://github.com/kripken/emscripten/tags) released since 1.34.1
* **BITS**: `["32bit", "64bit"]`
Example: `sdk-tag-1.34.4-64bit`

#### Branch release
`sdk-{BRANCH}-{BITS}`
* **BRANCH**: `["incoming", "master"]`
* **BITS**: `["32bit", "64bit"]`
Example: `sdk-master-32bit`


## How to use the image?
Start volume should be mounted in `/src`. 
For start point every Emscripten command is available. For the instance: emcc, em++, emmake, emar etc.

To compile single file it could be called like:
`docker run --rm -v $(pwd):/src trzeci/emscripten:sdk-tag-1.35.4-64bit emcc helloworld.cpp -o helloworld.js`

Hello World:
```bash
printf '#include <iostream>\nint main() { std::cout<<"HELLO FROM DOCKER C++"<<std::endl; return 0; }' > helloworld.cpp
docker run --rm -v $(pwd):/src trzeci/emscripten:sdk-tag-1.35.4-64bit emcc helloworld.cpp -o helloworld.js
node helloworld.js
```

## How to extend this image?
Good example of extending this image you can find here: https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten/Dockerfile
Basically it requires to create own Dockerfile what stats with: 
```Dockerfile
ARG EMSCRIPTEN_SDK=sdk-tag-1.37.16-64bit
FROM trzeci/emscripten-slim:${EMSCRIPTEN_SDK}

RUN ...
# ...

CMD ["/bin/bash"]; 
ENTRYPOINT ["/entrypoint"]
```
Doing so, don't forget about https://docs.docker.com/engine/userguide/eng-image/dockerfile_best-practices/ 

## How to compile?
0. Pull the latest https://github.com/asRIA/emscripten-docker
0. Compile [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten-slim/Dockerfile)

Helper command: `./build compile trzeci/emscripten-slim:sdk-tag-1.37.17-64bit` (where `sdk-tag-1.37.17-64bit` is an arbitry tag)

## Support 
* **GitHub / Issue tracker**: https://github.com/asRIA/emscripten-docker
* **Docker: emscripten**: https://hub.docker.com/r/trzeci/emscripten/
* **Docker: emscripten-slim**: https://hub.docker.com/r/trzeci/emscripten-slim/

## History
* from **1.37.16** all further images are compiled from singe [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/docker/trzeci/emscripten-slim/Dockerfile).

### License
MIT

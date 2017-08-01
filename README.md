[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten.svg)](https://store.docker.com/community/images/trzeci/emscripten/)
[![Size](https://images.microbadger.com/badges/image/trzeci/emscripten.svg)](https://microbadger.com/images/trzeci/emscripten/)

## Info
**GitHub / Issue tracker**: https://github.com/asRIA/emscripten-docker
**Docker**: https://hub.docker.com/r/trzeci/emscripten/

## Structure
Each tag was build from [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/Dockerfile)
* Base system: **Debian Jessie**
* Installed packages: 
  * `cmake`: 3.6.3
  * `make`: 4.0
  * `python`: 2.7
  * `nodejs`: 4.1 (from EMSDK)
  * `java`: OpenJDK 1.7.0_131
* Version of Emscripten:  **32bit** and **64bit**
* Starting from **1.36.7** images are bundled with cmake 3.6.3

`debian:jessie` has been chosen in order to have the latest ImageMagick. It is not a part of this image but this image could be easy extend to pull it. Image has been optimised in order to have the lowest possible size.

## Tag schema
#### latest
Currently latest tag is not available. Not decided yet it should point either on the latest master, or latest official release. 

#### Version release
`sdk-tag-{VERSION}-{BITS}`
where
**VERSION**: One of the official version released since 1.34.1
**BITS**: `["32bit", "64bit"]`
Example: `sdk-tag-1.34.4-64bit`

#### Branch release
`sdk-{BRANCH}-{BITS}`
where
**BRANCH**: `["incoming", "master"]`
**BITS**: `["32bit", "64bit"]`
Example: `sdk-master-32bit`

## How to use the image?
Start volume should be mounted in `/src`. 
For start point every Emscripten command is available. For the instance: emcc, em++, emmake, emar etc.

To compile single file it could be called like:
`docker run -v $(pwd):/src trzeci/emscripten:sdk-tag-1.35.4-64bit emcc helloworld.cpp -o helloworld.js`

This container nicely works with cmake projects

## How to compile?
0. Pull the latest https://github.com/asRIA/emscripten-docker
0. Compile Dockerfile

Here you can just type: `docker build . -t MY_TAG` and it should work just fine. 
You can use also `./build` script to automate the process.

## History
* from **1.37.19** all further images are compiled from singe [Dockerfile](https://github.com/asRIA/emscripten-docker/blob/master/Dockerfile). An entrypoint was added.
* from **1.37.10** images are bundled with `java`
* from **1.36.7** images are bundled with `make` and `nodejs`
* from **1.36.7** images are bundled with `cmake` 3.6.3, images are build from generated [Dockerfiles](https://github.com/asRIA/emscripten-docker/tree/f738f061c8068ec24124c37286eafec01d54a6ef/configs)
* from **1.35.0** images based on Debian
* from **1.34.X** images based on Ubuntu:15.10

### License
MIT


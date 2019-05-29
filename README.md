# Emscripten Docker
[![Build Status](https://jenkins.trzeci.eu/buildStatus/icon?job=public%2Femscripten-docker.release&style=flat-square)](https://jenkins.trzeci.eu/job/public/job/emscripten-docker.release/)


This repository contains source files for Docker Hub projects:

## trzeci/emscripten-slim
[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten-slim.svg)](https://store.docker.com/community/images/trzeci/emscripten-slim/)
[![Size](https://images.microbadger.com/badges/image/trzeci/emscripten-slim.svg)](https://microbadger.com/images/trzeci/emscripten-slim/)
[![Sanity](https://badges.herokuapp.com/travis/trzecieu/emscripten-docker?env=IMAGE=trzeci/emscripten-slim&label=hello)](https://travis-ci.org/trzecieu/emscripten-docker)

* **Docker Hub**: https://hub.docker.com/r/trzeci/emscripten-slim/
* **ReadMe**: https://github.com/trzecieu/emscripten-docker/blob/master/emscripten-slim.md

## trzeci/emscripten
[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten.svg)](https://store.docker.com/community/images/trzeci/emscripten/)
[![Size](https://images.microbadger.com/badges/image/trzeci/emscripten.svg)](https://microbadger.com/images/trzeci/emscripten/)
[![Sanity](https://badges.herokuapp.com/travis/trzecieu/emscripten-docker?env=IMAGE=trzeci/emscripten&label=hello)](https://travis-ci.org/trzecieu/emscripten-docker)

* **Docker Hub**: https://hub.docker.com/r/trzeci/emscripten/
* **ReadMe**: https://github.com/trzecieu/emscripten-docker/blob/master/emscripten.md

## Extending this image
In case if you'd like to create a different image that contains precompiled emscripten you can use multistage Docker file.
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
Alternatively you can also call `. /emsdk_portable/emsdk_set_env.sh` in your entrypoint - it will work just fine!

## Usage of build script
```
/build --help
usage: build [-h] {compile,test,push} ...

Emscripten Image generator

optional arguments:
  -h, --help           show this help message and exit

command:
  {compile,test,push}  Main work command
    compile            Compile Docker images
    test               Test given tag(s) with Emscripten and WebAssembly
                       compatibility
    push               Runs a service what will push created images
```

## Who uses this image?

* https://github.com/medialize/sass.js
* https://github.com/jasoncharnes/run.rb
* https://github.com/GoogleChromeLabs/webm-wasm
* https://github.com/google/neuroglancer
* https://github.com/finos/perspective
* https://blog.qt.io/blog/2019/03/05/using-docker-test-qt-webassembly/
* And many more that I'm proud of each!


## License
[![MIT](https://img.shields.io/github/license/trzecieu/emscripten-docker.svg?style=flat-square)](https://github.com/trzecieu/emscripten-docker/blob/master/LICENSE)


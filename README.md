# Emscripten Docker
[![Build Status](https://jenkins.trzeci.eu/buildStatus/icon?job=public%2Femscripten-docker.release&style=flat-square)](https://jenkins.trzeci.eu/job/public/job/emscripten-docker.release/)

This repository contains source files for Docker Hub projects.

__If you're looking for readme related to dockerimages, please see following table where to look for a specific readme.__

## trzeci/emscripten-slim
[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten-slim.svg)](https://store.docker.com/community/images/trzeci/emscripten-slim/)
[![Size](https://images.microbadger.com/badges/image/trzeci/emscripten-slim.svg)](https://microbadger.com/images/trzeci/emscripten-slim/)
[![Sanity](https://badges.herokuapp.com/travis/trzecieu/emscripten-docker?env=IMAGE=trzeci/emscripten-slim&label=hello)](https://travis-ci.org/trzecieu/emscripten-docker)

| | |
|-|-|
|Docker Hub|[trzeci/emscripten-slim](https://hub.docker.com/r/trzeci/emscripten-slim/)|
|Readme|[emscripten-slim.md](emscripten-slim.md)|


## trzeci/emscripten
[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten.svg)](https://store.docker.com/community/images/trzeci/emscripten/)
[![Size](https://images.microbadger.com/badges/image/trzeci/emscripten.svg)](https://microbadger.com/images/trzeci/emscripten/)
[![Sanity](https://badges.herokuapp.com/travis/trzecieu/emscripten-docker?env=IMAGE=trzeci/emscripten&label=hello)](https://travis-ci.org/trzecieu/emscripten-docker)

| | |
|-|-|
|Docker Hub|[trzeci/emscripten](https://hub.docker.com/r/trzeci/emscripten/)|
|Readme|[emscripten.md](emscripten.md)|


## Usage of build script
```
./build --help
usage: build [-h] {compile,test,push,set_latest} ...

Emscripten Image generator

optional arguments:
  -h, --help            show this help message and exit

command:
  {compile,test,push,set_latest}
                        Main work command
    compile             Compile Docker images.
    test                Test given tag(s) with Emscripten and WebAssembly
                        compatibility
    push                Runs a service what will push created images
    set_latest          Automatically sets the 'latest' tag
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


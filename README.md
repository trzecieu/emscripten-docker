# Emscripten Docker
This repository contains source files for Docker Hub projects:

## trzeci/emscripten-slim
[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten-slim.svg)](https://store.docker.com/community/images/trzeci/emscripten-slim/) [![Size](https://images.microbadger.com/badges/image/trzeci/emscripten-slim.svg)](https://microbadger.com/images/trzeci/emscripten-slim/)

* **Docker Hub**: https://hub.docker.com/r/trzeci/emscripten-slim/
* **ReadMe**: https://github.com/asRIA/emscripten-docker/blob/master/emscripten-slim.md

## trzeci/emscripten
[![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten.svg)](https://store.docker.com/community/images/trzeci/emscripten/) [![Size](https://images.microbadger.com/badges/image/trzeci/emscripten.svg)](https://microbadger.com/images/trzeci/emscripten/)

* **Docker Hub**: https://hub.docker.com/r/trzeci/emscripten/
* **ReadMe**: https://github.com/asRIA/emscripten-docker/blob/master/emscripten.md

## Usage
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

## License
[MIT](https://github.com/asRIA/emscripten-docker/blob/master/LICENSE)


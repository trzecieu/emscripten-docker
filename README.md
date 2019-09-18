# Emscripten Docker (Unofficial Image)
[![Build Status](https://jenkins.trzeci.eu/buildStatus/icon?job=public%2Femscripten-docker.release&style=flat-square)](https://jenkins.trzeci.eu/job/public/job/emscripten-docker.release/)

This repository contains source files for Docker Hub projects.

__If you're looking for readme related to specific DockerImages, please see following table where to look for a specific readme.__

## Docker Files and Images

| DockerHub | Dockerfile | Readme | Badges |
| --- | --- | --- | --- |
| [trzeci/emscripten-slim](https://hub.docker.com/r/trzeci/emscripten-slim/) | [Dockerfile](./docker/trzeci/emscripten-slim/Dockerfile) | [emscripten-slim.md](./docs/emscripten-slim.md) | [![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten-slim.svg)](https://store.docker.com/community/images/trzeci/emscripten-slim/)<br/>[![Size](https://images.microbadger.com/badges/image/trzeci/emscripten-slim.svg)](https://microbadger.com/images/trzeci/emscripten-slim/)<br/>[![Sanity](https://badges.herokuapp.com/travis/trzecieu/emscripten-docker?env=IMAGE=trzeci/emscripten-slim&label=hello)](https://travis-ci.org/trzecieu/emscripten-docker) |
| [trzeci/emscripten](https://hub.docker.com/r/trzeci/emscripten/) | [Dockerfile](./docker/trzeci/emscripten/Dockerfile) | [emscripten.md](./docs/emscripten.md) | [![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten.svg)](https://store.docker.com/community/images/trzeci/emscripten/)<br/>[![Size](https://images.microbadger.com/badges/image/trzeci/emscripten.svg)](https://microbadger.com/images/trzeci/emscripten/)<br/>[![Sanity](https://badges.herokuapp.com/travis/trzecieu/emscripten-docker?env=IMAGE=trzeci/emscripten&label=hello)](https://travis-ci.org/trzecieu/emscripten-docker) |
| [trzeci/emscripten-ubuntu](https://hub.docker.com/r/trzeci/emscripten-ubuntu/) | [Dockerfile](./docker/trzeci/emscripten-ubuntu/Dockerfile) | [emscripten-ubuntu.md](./docs/emscripten-ubuntu.md) | [![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten-ubuntu.svg)](https://store.docker.com/community/images/trzeci/emscripten-ubuntu/)<br/>[![Size](https://images.microbadger.com/badges/image/trzeci/emscripten-ubuntu.svg)](https://microbadger.com/images/trzeci/emscripten-ubuntu/)<br/>[![Sanity](https://badges.herokuapp.com/travis/trzecieu/emscripten-docker?env=IMAGE=trzeci/emscripten-ubuntu&label=hello)](https://travis-ci.org/trzecieu/emscripten-docker) |
| [trzeci/emscripten-upstream](https://hub.docker.com/r/trzeci/emscripten-upstream/) | [Dockerfile](./docker/trzeci/emscripten-upstream/Dockerfile) | [emscripten-upstream.md](./docs/emscripten-upstream.md) | [![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten-upstream.svg)](https://store.docker.com/community/images/trzeci/emscripten-upstream/)<br/>[![Size](https://images.microbadger.com/badges/image/trzeci/emscripten-upstream.svg)](https://microbadger.com/images/trzeci/emscripten-upstream/)<br/>[![Sanity](https://badges.herokuapp.com/travis/trzecieu/emscripten-docker?env=IMAGE=trzeci/emscripten-upstream&label=hello)](https://travis-ci.org/trzecieu/emscripten-docker) |
| [trzeci/emscripten-fastcomp](https://hub.docker.com/r/trzeci/emscripten-fastcomp/) | [Dockerfile](./docker/trzeci/emscripten-fastcomp/Dockerfile) | [emscripten-fastcomp.md](./docs/emscripten-fastcomp.md) | [![Docker Pulls](https://img.shields.io/docker/pulls/trzeci/emscripten-fastcomp.svg)](https://store.docker.com/community/images/trzeci/emscripten-fastcomp/)<br/>[![Size](https://images.microbadger.com/badges/image/trzeci/emscripten-fastcomp.svg)](https://microbadger.com/images/trzeci/emscripten-fastcomp/)<br/>[![Sanity](https://badges.herokuapp.com/travis/trzecieu/emscripten-docker?env=IMAGE=trzeci/emscripten-fastcomp&label=hello)](https://travis-ci.org/trzecieu/emscripten-docker) |



## Usage of build script
```
➜ python3 -m builder --help
usage: __main__.py [-h] {compile,push,set_latest} ...

Emscripten Image generator

optional arguments:
  -h, --help            show this help message and exit

command:
  {compile,push,set_latest}
                        Main work command
    compile             Compile Docker images.
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


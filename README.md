### Emscripten Docker images generator

Generator for Docker image dedicated to run emscripten.

This has to be run manually on dedicated machine, because compilation procees of emscipten takes ~1h what is more than limit of execution auto builds on Docker Hub

DockerHub: https://hub.docker.com/r/trzeci/emscripten/

- [x] Creates all releases from tag
- [x] Support for 64 and 32 releases
- [x] auto publish images
- [x] Validate generated images
- [x] Add a job that handles: "incoming" and "master" branches
- [ ] Dedicate some device that runs onece per day and update branch builds.

### License MIT

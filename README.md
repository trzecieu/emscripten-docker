### Emscripten Docker images generator

Generator for Docker image dedicated to run emscripten.

This has to be run manually on dedicated machine, because a compilation process of building Emscipten takes ~1h. What is more than a limit of execution for auto builds on the Docker Hub.

DockerHub: https://hub.docker.com/r/trzeci/emscripten/

- [x] Creates all releases from tag
- [x] Support for 64 and 32 releases
- [x] auto publish images
- [x] Validate generated images
- [x] Add a job that handles: "incoming" and "master" branches
- [ ] Dedicate some device that runs onece per day and update branch builds.


### Usage

The application runs in two modes: 
- generator: compiles fully functional docker image and stores it into local docker inventory
- consumer: watches `queue.txt` what generator has produced, and pushes to the docker hub

Hence, suggested setup requires two consoles:

#### generator

`python ./generator.py branches releases 32 64`
where:
- `branches` : will generate images from incomming and master
- `releases` : will generate every released tag
- `64`/`32` : will build both 32 and 64 bit

#### consumer

`python ./generator.py consumer`
The application will automatically push what generator has created


### License
MIT

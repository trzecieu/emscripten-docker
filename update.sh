#!/bin/bash

echo "Clean unused docker images"
docker rm $(docker ps -a -q) 2> /dev/null
docker rmi $(docker images -q) 2> /dev/null

echo "Update emscripten-docker script"
git clean -fdx
git pull

set +x
echo "Compile and push"
./build compile --incoming --branches --fast-fail
./build push --no-block

echo "DONE"



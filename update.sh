#!/bin/bash

BASEDIR=$(dirname "$0")

echo "Clean unused docker images"
docker rm $(docker ps -a -q) 2> /dev/null
docker rmi $(docker images -q) 2> /dev/null

pushd $BASEDIR
    echo "Update emscripten-docker script"
    git clean -fdx
    git pull

    set +x
    echo "Compile and push"
    ./build compile --branches --fast-fail
    ./build push --no-block
    ./build set_latest

    ./build compile --incoming --fast-fail
    ./build push --no-block
popd

echo "DONE"



#!/bin/bash

image=$1
tag=$2

echo "Make ${image}:${tag} as the latest"
docker pull ${image}:${tag}
docker tag ${image}:${tag} ${image}:latest
docker push ${image}:latest
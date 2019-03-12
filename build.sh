#!/bin/bash

increment_version ()
{
  echo $1 | awk -F. -v OFS=. 'NF==1{print ++$NF}; NF>1{if(length($NF+1)>length($NF))$(NF-1)++; $NF=sprintf("%0*d", length($NF), ($NF+1)%(10^length($NF))); print}'
} 

# check docker is running at all
{
  # will throw an error if the docker daemon is not running and jump
  # to the next code chunk     
  docker ps -q
} || {
  exit -1
}

TAG=$(cat release)
TAG=$(increment_version $TAG)

echo Building Docker image ver. $TAG
cp myproject/cfg/config-confidential.yml myproject/cfg/config.yml
docker-compose build --no-cache

IMAGE='collabuniba/mini-ipip'
docker tag $IMAGE:latest $IMAGE:$TAG

echo Pushing Docker image $IMAGE:$TAG
docker push $IMAGE:$TAG

echo $TAG > release
git commit release -m "Update release number"

git checkout myproject/cfg/config.yml
git push uniba master

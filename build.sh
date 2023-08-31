#!/bin/bash
if [ "$1" == "" ] ; then
  echo "usage: sh build.sh <version>"
  echo "Example:"
  echo "./build.sh latest"
  exit 0
fi

version=$1
image=cpsc393_student_image

docker build --build-arg USER=${USER} \
  --network=host \
  -t ${image}:${version} .

if [ $? -ne 0 ] ; then
    echo "Trouble with docker build"
    exit 1
fi



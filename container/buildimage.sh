#!/bin/bash
# Toomey Sept 2020

# It 'might' work with docker, not on 8 though
COMMAND="podman"

# Check parameters
if test "$#" -ne 2; then
  echo "Usage: buildimage imagename imagekey (Ex: ./buildimage rapio7 rapio7_centos7)"
  exit
fi

# Check podman..haven't tried docker on 8 
if ! command -v $COMMAND &> /dev/null
then
    echo "$COMMAND command not found, wrong os or needs to be installed"
    exit
fi

# Make sure in directory of this script no matter where called from
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

# Get builder stuff (and any other requirements) into local folder on the image.
# Needs to be a copy for security/subfolder requirement of podman/docker
# and avoid having to link host here
rm -rf working
mkdir -p working
cp -r ../mrmsbuilder working/mrmsbuilder
cp -r ../third working/third
cp ../build.py working/build.py 
cp -r configs working/configs

podman build --tag $1 -f $2

#!/bin/bash
# Toomey December 2020
# Podman creating rapio/third in centos8 stream
# Currently I'm patching the centos:8 I'm betting they
# have an image for it later.

#podman build --tag rapio_centos8 -f rapio_centos8.dock
./buildimage.sh rapio8s rapio_centos8s.dock

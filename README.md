# MRMS Builder

MRMS Builder is a collection of python scripts and utilities for building RAPIO and MRMS on linux systems and in containers.  There's more in here than most people will ever use.  We use several packages with non-default compiler flags and settings so this builder handles that.  We also static chain the entire build since currently we handle having multiple builds on our systems and don't want them to step on each other.

## Requirements
Python

## WDSSII/MRMS
Run ./build mrms.cfg to build the MRMS system.  Obviously to do this you need to have access to the code repository for NSSL, since the WDSSII/MRMS code is propritary.

## RAPIO
Run ./build rapio.cfg to just attempt to build RAPIO.  

## Containers
We have various scripts and docker/podman files in the container subfolder which can be used to generate containers of our code/deployment.

## Operating systems
We have made containers using the Amazon linux 2, Centos7 and Centos8.  Mostly because that's what we're 'stuck' to using at NSSL right now for research and deployment.

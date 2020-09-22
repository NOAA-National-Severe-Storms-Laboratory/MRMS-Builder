#!/bin/bash
# Toomey Sept 2020

# This adds packages for the GUI as well
# I also remove sourcecode/strip binaries, etc. to shrink the image.
# making a 'full' sourcecode one is 10 GB, lol.

./buildimage.sh mrms_c7_full mrms_c7_full.dock

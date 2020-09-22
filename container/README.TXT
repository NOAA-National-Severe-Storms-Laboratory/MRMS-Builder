# Toomey Sept 2020
# Building containers.  I can't really help you master containers, 
# there are good youtube videos documentation out there.
#
# I'm currently building using podman on centos8, but 
# using podman or docker should be similiar
# Each build.sh script is various build levels, and I might chain the images
# later to save even more space.
#
# I suggest you build the mrms_c7_full docker.  It removes sourcecode and ends
# up with a wg build plus algs that is about 2.6 GB.
# ./build_mrms_c7_full.sh
#
# As a user such as mrms, you must map userids/groups in /etc/subuid and /etc/subgid.  For example add mrms like so:
# mrms:100000:65536
# Then run 'podman system migrate' as the user 
#
# Transfering an image example and running it somewhere else:
podman save mrms_c7_full > mrms.tar
gzip mrms.tar  # Turn into tar.gz save transfer time
gunzip mrms.tar.gz # ungip final destination
podman image load < mrms.tar # Bring it in
podman run -h 'mypod.winstorm.nssl' -it mrms_c7_full /bin/bash
w2merger
#
# Level 1:
# build_rapio7, rapio8, amz2 -- 'core' third libraries build, no WDSS2/copyright/etc.
#
# Level 2:
# build_mrms_c7_algs.sh -- Build image with algorithms such as for vmrms centos7
# build_mrms_c8_algs.sh -- " centos8 
#
# Level 3:
# build_mrms_c7_full.sh -- Build the GUI (wg)
# -- There isn't a build GUI for centos8 due to libraries, etc.  GTK3 and the gl libraries.
#
# NOTE: To run, you must currently pass a hostname with winstorm.nssl as it is one of the authentication checks.
podman run -h 'mycontainer.winstorm.nssl' -it THEIMAGENAME 
# Quick cheat-sheet
# show all static images you can spawn
podman images
# show all containers (these are 1 to N instances of the images)
podman container list --all 
# remove all containers (needed before removing an image)
podman container rm --all 
# remove images (and containers related to it)
podman rmi --force THEIMAGENAME 
# save container as new image after exit (keeping changes)
podman commit THECONTAINERNAME 


# Toomey December 2020

# Trying to update the centos:8 to a stream image before anything else
dnf install centos-release-stream -y
dnf distro-sync -y

# Install packages from 'older' centos8
./rapio_centos8.sh

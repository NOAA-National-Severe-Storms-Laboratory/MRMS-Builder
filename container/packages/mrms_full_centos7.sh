# Toomey Sept 2020
# Centos:7 image requirements for building
# If using docker/etc, having a single install script drops the storage for layers quite a bit

# -------------------------------------------------------------
# Base core/setup libraries
./mrms_algs_centos7.sh

# -------------------------------------------------------------
# WDSS2 WG extras
yum install epel-release -y
yum install gtkglext-devel -y

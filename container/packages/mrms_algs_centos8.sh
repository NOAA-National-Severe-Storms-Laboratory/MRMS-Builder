# Toomey Sept 2020
# Centos:8 image requirements for building
# If using docker/etc, having a single install script drops the storage for layers quite a bit

# -------------------------------------------------------------
# Base core/setup libraries
./rapio_centos8.sh

# -------------------------------------------------------------
# WDSS2/MRMS build extras

# gdal libjpeg-turbo-devel
dnf install libjpeg-turbo-devel -y
# MRMS/HMET fortran stuf
dnf install gcc-gfortran -y
# 'file' checks in mrms python script for non-rapio
dnf install file -y

# CENTOS 8 and UP ONLY (WDSS2)
# Remote Procedure Call has moved from glibc-devel. This header is
# /usr/include/rpc/rpc.h and is used by w2ext/nexrad.  Need
# new rpm with this:
dnf install libtirpc-devel -y

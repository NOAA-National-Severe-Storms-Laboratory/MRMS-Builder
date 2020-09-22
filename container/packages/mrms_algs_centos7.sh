# Toomey Sept 2020
# Centos:7 image requirements for building
# If using docker/etc, having a single install script drops the storage for layers quite a bit

# -------------------------------------------------------------
# Base core/setup libraries
./rapio_centos7.sh

# -------------------------------------------------------------
# WDSS2/MRMS build extras

# gdal libjpeg-turbo-devel
yum install libjpeg-turbo-devel -y
# MRMS/HMET fortran stuf
yum install gcc-gfortran -y
# 'file' checks in mrms python script for non-rapio
yum install file -y

# CENTOS 7 ONLY (WDSS2)
# Remote Procedure Call is in from glibc-devel. This header is
# /usr/include/rpc/rpc.h and is used by w2ext/nexrad.  Need
# new rpm with this:
yum install glibc-devel -y

# Toomey Sept 2020
# -------------------------------------------------------------
# Algs/HMET package extras

# gdal libjpeg-turbo-devel 
dnf install libjpeg-turbo-devel -y
# MRMS/HMET fortran stuf
dnf install gcc-gfortran -y
# 'file' checks in mrms python script for non-rapio
dnf install file -y

# CENTOS 8 ONLY (WDSS2)
# Remote Procedure Call is in from glibc-devel. This header is
# /usr/include/rpc/rpc.h and is used by w2ext/nexrad.  Need
# new rpm with this:
dnf install libtirpc-devel -y

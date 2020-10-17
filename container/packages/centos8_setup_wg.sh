# Toomey Sept 2020
# Script I run on a stock centos:8 container image
# to prepare for wg.  Biggest thing is the xpra repository,
# it appears to be kept current as of now.
# Should work on a base centos8 install as well

# -------------------------------------------------------------
# Raw stuff missing on centos:8 image

# Utility stuff/useful for admin 
# color ls on container/install please
dnf install vim coreutils-common -y

# Repo access
dnf install svn git -y

# Python for my script builder.  Bleh 2/3...let's do 2
#RUN dnf install python38 -y
dnf install python2 -y

# -------------------------------------------------------------
# Basic compiler stuff, RAPIO core (subset of WDSSII/MRMS)
#Compiler stuff
#gcc-toolset-9-gcc-c++ is on here too, we'll go with stock
# libtool 'should' snag autoconf, automake, m4
dnf install gcc-c++ gdb make libtool -y

#Compression/Decompression libraries
dnf install unzip xz-devel bzip2-devel -y

# Development libraries
# expat-devel (udunits requirement)
dnf install expat-devel libpng-devel openssl-devel -y

# Stuff RAPIO doesn't really need, but the Third package does 
# If we break it up base, rapio, algs, gui it should be here
# (gdal)
dnf install libjpeg-turbo-devel -y

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

# -------------------------------------------------------------
# WDSS2 WG extras

# Use the xpra org repository.  We might even try using
# xpra in containers at some point for running wg
# it avoids some of the x display security stuff

# Web probably better but I'll hard cat it for now
# We're pulling over web from that repo anyway so it needs to be there
#curl https://xpra.org/repos/CentOS/xpra.repo -o /etc/yum.repos.d/xpra.repo
cat >/etc/yum.repos.d/xpra.repo <<'EOL'
[xpra]
name=Xpra $releasever - $basearch
enabled=1
metadata_expire=1d
gpgcheck=1
gpgkey=https://xpra.org/gpg.asc
baseurl=https://xpra.org/dists/CentOS/$releasever/$basearch/
EOL

dnf install gtkglext-devel -y



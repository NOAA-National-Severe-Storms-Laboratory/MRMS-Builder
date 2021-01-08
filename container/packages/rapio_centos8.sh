# Toomey Sept 2020
# Centos:8 image requirements for building
# If using docker/etc, having a single install script drops the storage for layers quite a bit

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

# (image) The image plugin for RAPIO uses imagick
dnf install GraphicsMagick-c++-devel -y

# Stuff RAPIO doesn't really need, but the Third package does 
# If we break it up base, rapio, algs, gui it should be here
# (gdal)
dnf install libjpeg-turbo-devel -y

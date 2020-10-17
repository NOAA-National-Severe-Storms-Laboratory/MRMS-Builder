# Toomey Sept 2020
# Centos:7 image requirements for building
# If using docker/etc, having a single install script drops the storage for layers quite a bit

# -------------------------------------------------------------
# Raw stuff missing on centos:7 image

# Utility stuff/useful for admin 
# color ls on container/install please
yum install vim coreutils-common -y

# Repo access
yum install svn git -y

# Python for my script builder. 
yum install python -y

# -------------------------------------------------------------
# Basic compiler stuff, RAPIO core (subset of WDSSII/MRMS)
#Compiler stuff
#gcc-toolset-9-gcc-c++ is on here too, we'll go with stock
# libtool 'should' snag autoconf, automake, m4
yum install gcc-c++ gdb make libtool -y

#Compression/Decompression libraries
yum install unzip xz-devel bzip2-devel -y

# Development libraries
# expat-devel (udunits requirement)
yum install expat-devel libpng-devel openssl-devel -y

# Stuff RAPIO doesn't really need, but the Third package does 
# If we break it up base, rapio, algs, gui it should be here
# (gdal)
yum install libjpeg-turbo-devel -y

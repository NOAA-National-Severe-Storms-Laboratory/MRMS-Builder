#
#  Robert Toomey
#  April 2017
#
#  This will become a new simplier m4 for building using the python scripts.
#  It should be reduced drastically.  We hardlink to our custom third party.
#  This will work in most situations.
#

dnl
dnl
dnl

AC_DEFUN([W2_WITH_GDAL],
    [AC_ARG_WITH([gdal],
                 [AC_HELP_STRING([--with-gdal],[build converters that use gdal (default=yes)])],
                 [case "${withval}" in
                   no) gdal=false;;
                   yes) gdal=true;;
                   *) AC_MSG_ERROR([bad value ${withval} for --with-gdal]);;
                  esac],[gdal=true])
     AM_CONDITIONAL(COND_GDAL, test x$gdal = xtrue)
    ]
)

dnl
dnl
dnl

AC_DEFUN([W2ALGS_WITH_TDWR],
    [AC_ARG_WITH(tdwr,
        [AC_HELP_STRING([--with-tdwr],[support TDWR data conversion (default=yes)])],
        [if test x"${withval}" = xno; then
            tdwr=false
        elif test x"${withval}" = xyes; then
            tdwr=true
        else
            AC_MSG_ERROR(bad value ${withval} for --with-tdwr)
        fi],
        [tdwr=true]
    )
    AM_CONDITIONAL(TDWR, test x"${tdwr}" = xtrue)
    ]
)

AC_DEFUN([W2ALGS_WITH_DEALIAS],
    [AC_ARG_WITH(dealias,
        [AC_HELP_STRING([--with-dealias],[support DALIASING velocity data (default=yes)])],
        [if test x"${withval}" = xno; then
            dealias=false
        elif test x"${withval}" = xyes; then
            dealias=true
        else
            AC_MSG_ERROR(bad value ${withval} for --with-dealias)
        fi],
        [dealias=true]
    )
    AM_CONDITIONAL(DEALIAS, test x"${dealias}" = xtrue)
    ]
)

AC_DEFUN([W2_WITH_RSSD],
    [AC_ARG_WITH(
        [rssd],
        [AC_HELP_STRING([--with-rssd],[Which library to use for RSSD library notification: glib or libinfr.  (default=libinfr)])],
        [if test x"${withval}" = xlibinfr; then 
            rssd=libinfr
        elif test x"${withval}" = xglib; then
            rssd=glib
        else
            AC_MSG_ERROR([bad value ${withval} for --with-rssd: please specify glib or libinfr.])
        fi],
        [rssd=libinfr]
    )
    AM_CONDITIONAL(RSSD, test x"${rssd}" = xlibinfr)
    if test x"${rssd}" = xlibinfr ; then
        AC_DEFINE([WITH_LIBINFR], [], [Use libinfr for RSS Notification])
    fi
    AC_MSG_RESULT("RSSD Implementation: ${rssd}")
    ]
)

AC_DEFUN([W2_ENABLE_NETSSAP],
    [AC_ARG_ENABLE(netssap,
        [AC_HELP_STRING([--disable-netssap],[turn off netssap support])],
        [if test x"${enableval}" = xyes; then
            netssap=true
        elif test x"${enableval}" = xno; then
            netssap=false
        else
            AC_MSG_ERROR(bad value ${enableval} for --enable-netssap)
        fi],
        [netssap=true]
    )
    AM_CONDITIONAL(NETSSAP, test x"${netssap}" = xtrue)
    AC_MSG_RESULT("Building netssap? ... ${netssap}")
    ]
)

# W2_FIND_PATH
# $1 == ENV that could be set.  If it is, we FORCE the use of this
#     So if $UDUNITS_DIR is set to /home/folder3/, we MUST find udunits here.
#     This keeps us from hunting all over the system during auto and special builds
#
# $2 == List of paths for the Force.  This should be all paths using ENV,
#     such as $UDUNITS_DIR/include
# $3 == List of optional paths to search through if ENV is blank. This should
#     be all paths without ENV in them
# $4 == List of Files to look for
# $5 == Variable to set to final path
#
# Result is fc_found = true/false
#             and fc_name fc_path set to first path and name match
#
#  W2_CHECK_HEADERS uses this macro
#

AC_DEFUN([W2_FIND_PATH],[

    # If ENV is set, use forced paths, otherwise others
    fp_path="$esyscmd(echo '$1' | tr -d '\n\r[:blank:]')";
    if test x"$fp_path" = x; then 
      fp_search="esyscmd(echo '$3' | tr -ds '\n\r' ' ')";
    else
      echo "--> Enforcing  **$1** to ENV setting of $fp_path";
      fp_search="esyscmd(echo '$2' | tr -ds '\n\r' ' ')";
    fi

    # Hunt for files in the forced path, or various paths
    fp_found=false
    for fc_mypath in $fp_search; do
     for fc_myname in esyscmd(echo '$4' | tr -ds '\n\r' ' '); do
      AC_CHECK_FILE($fc_mypath/$fc_myname,fp_found=true;break 2)
     done
    done
    
    # Did we find a matching file or not?
    if test x"$fp_found" = xfalse; then
      if test x"$fp_path" != x; then
        echo "--> You have explicitly set $1 in your environment, but the required files"
        echo "--> are missing.  Unset $1 or change it to a correct location."
      fi
      AC_MSG_ERROR("esyscmd(echo '$5' | tr -d '\n\r[:blank:]') path not found")
    else
     esyscmd(echo '$5' | tr -d '\n\r[:blank:]')=$fc_mypath
    fi
])

#
# Find -I first path
#
AC_DEFUN([W2_CHECK_HEADERS],[
   W2_FIND_PATH(
    esyscmd(echo '$1' | tr -d '\n\r'),
    esyscmd(echo '$2'),
    esyscmd(echo '$3'),
    esyscmd(echo '$4'),
    esyscmd(echo '$5'))

   # Set the value if found to -I plus path
   if test x"$fp_found" != xfalse; then
     esyscmd(echo '$5' | tr -d '\n\r[:blank:]')=-I$fc_mypath
   fi

dnl Not sure if this is still necessary,
dnl so I'll comment it out instead of deleting it.
dnl These two directories are *not* included anyway
dnl on some non-Linux platforms such as Interix.
dnl
dnl Make /usr/include or /usr/local/include are blank,
dnl since these are included anyway
dnl
dnl   if test x"$fc_mypath" = x/usr/include; then
dnl     esyscmd(echo '$5' | tr -d '\n\r[:blank:]')=""
dnl   fi
dnl   if test x"$fc_mypath" = x/usr/local/include; then
dnl     esyscmd(echo '$5' | tr -d '\n\r[:blank:]')=""
dnl   fi
])


dnl [in] $1 - list of directories to search
dnl [in] $2 - optional suffix to each directory
dnl [in] $3 - filename to look for
dnl [out] $4 - directory of the found file, or empty if no match
AC_DEFUN([WG_FIND_FILE],[
  wgff_found_dir=''
  for dir in "$1"
  do
    if test -n "$2"
    then
       wgff_file=$dir/$2/$3
       AC_CHECK_FILE($wgff_file,wgff_found_dir=$dir/$2;break)
    fi
    wgff_file=$dir/$3
    AC_CHECK_FILE($wgff_file,wgff_found_dir=$dir;break)
  done
  $4=$wgff_found_dir
])
  

dnl [in] $1 - name of the library we're looking for
AC_DEFUN([W2_CHECKING_LIBRARY],[
  if [ test "$enable_static" = "yes" ]
  then
    AC_CHECKING([for $1, static libraries preferred])
  else
    AC_CHECKING([for $1, shared libraries preferred])
  fi
])

dnl [in] $1 - exclusive env variable which, if set, must be used exclusively.
dnl [in] $2 - secondary paths to be used if $1 is not set
dnl [in] $3 - libraries to search for, omitting the "lib" prefix and ".so" or ".a" suffixes
dnl [out] $4 - directory of the found library, or empty if no match
dnl [out] $5 - basename of the found library, or empty if no match
AC_DEFUN([W2_FIND_LIBRARY],[

  case "$host_os" in
   *darwin*) shared_library_suffix=".dylib";;
   *) shared_library_suffix=".so";;
  esac

  # which do we look for first, shared or static versions?
  if [ test "$enable_static" = "yes" ]
  then
    wfl_suffix_1=".a"
    wfl_suffix_2=${shared_library_suffix}
  else
    wfl_suffix_1=${shared_library_suffix}
    wfl_suffix_2=".a"
  fi

  # if $1 is present, only use it.  Otherwise search all through $2
  if test -n "$1"
  then
    wfl_search_path="$1"
  else
    wfl_search_path="$2"
  fi

  wfl_found_dir=''
  wfl_found_base=''

  # first try with wfl_suffix_1
  for lib in "$3"
  do
    if test -z $wfl_found_dir
    then
      file="lib$lib$wfl_suffix_1"
      WG_FIND_FILE("$wfl_search_path", lib, $file, wfl_found_dir)
      if test -n "$wfl_found_dir"
      then
        wfl_found_base=$file
      fi
    fi
  done

  # if not found with wfl_suffix_1, try wfl_suffix_2
  if test -z $wfl_found_dir
  then
    for lib in "$3"
    do
      if test -z "$wfl_found_dir"
      then
        file="lib$lib$wfl_suffix_2"
        WG_FIND_FILE("$wfl_search_path", lib, $file, wfl_found_dir)
        if test -n "$wfl_found_dir"
        then
          wfl_found_base=$file
        fi
      fi
    done
  fi

  if test -n "$wfl_found_base"
  then
    $4="$wfl_found_dir"
    $5="$wfl_found_base"
  fi

  if test -z "$$4"
  then
    AC_MSG_ERROR([Can't find any of $3 in $2])
  fi
])

dnl [in] $1 - exclusive env variable which, if set, must be used exclusively.
dnl [in] $2 - secondary paths to be used if $1 is not set
dnl [in] $3 - libraries to search for, omitting the "lib" prefix and ".so" or ".a" suffixes
dnl [in] $4 - LIBS variable to append to
AC_DEFUN([W2_FIND_LIBRARY_AND_APPEND],[
  w2flaa_dir=''
  w2flaa_base=''
  W2_FIND_LIBRARY($1,$2,$3,w2flaa_dir,w2flaa_base)
  $4="$$4 $w2flaa_dir/$w2flaa_base"
  echo "$4: $$4"
])


dnl [in] $1 - exclusive env variable which, if set, must be used exclusively.
dnl [in] $2 - secondary paths to be used if $1 is not set
dnl [in] $3 - header to search for
dnl [in] $4 - CFLAGS variable to append to
AC_DEFUN([W2_FIND_HEADER_AND_APPEND],[
  if test -n $1
  then
    w2fhaa_search_path=$1
  else
    w2fhaa_search_path=$2
  fi
  w2fhaa_dir=''
  WG_FIND_FILE("$w2fhaa_search_path", "include", $3, w2fhaa_dir)
  if test -z "$w2fhaa_dir"
  then
    AC_MSG_ERROR([Could not ($1, $2) find header $3 in $w2fhaa_search_path])
  fi
  $4="$$4 -I$w2fhaa_dir"
  echo "$4: $$4"
])


#####################  DO COMPLETE CONFIGURATION HERE

AC_DEFUN([CHECK_LDUNITS],[

  # Use UDUNITS_DIR if given, otherwise use the built 3rd party version
  #ud_inc_search_path="/usr/include /usr/include/udunits2/"
  #ud_lib_search_path="/usr/lib64"
 #
  # Use built in third party...
  ud_inc_search_path="$prefix/include"
  ud_lib_search_path="$prefix/lib"

  AC_CHECKING(for UDUNITS header files)
  W2_FIND_HEADER_AND_APPEND("$UDUNITS_DIR", "$ud_inc_search_path", "udunits.h", UDUNITS_CFLAGS)

  W2_CHECKING_LIBRARY(UDUNITS)
  W2_FIND_LIBRARY_AND_APPEND("$UDUNITS_DIR", "$ud_lib_search_path", "udunits2", UDUNITS_LIBS)
])

AC_DEFUN([CHECK_OPENSSL],[
    #openssl_include_path="$prefix $code_search_path $PWD/.. /usr/include/openssl"
    #openssl_lib_path="$prefix $code_search_path $PWD/.. /usr/lib64 /usr/lib /usr/local"

    # We build using installed openssl rpms
    
    openssl_include_path="/usr/include/openssl"
    openssl_lib_path="/usr/lib64"

    AC_CHECKING(for openssl header files)
    W2_FIND_HEADER_AND_APPEND("$OPENSSL_INCLUDE", "$openssl_include_path", "evp.h", OPENSSL_CFLAGS)

    W2_CHECKING_LIBRARY(openssl)
    W2_FIND_LIBRARY_AND_APPEND("$OPENSSL_LIB", "$openssl_lib_path", "crypto", OPENSSL_LIBS)
])

AC_DEFUN([CHECK_PNG],[
  png_lib_search_path="/usr/lib64"
  png_inc_search_path="/usr/include"
  #png_lib_search_path="$prefix/lib"
  #png_inc_search_path="$prefix/include"

  AC_CHECKING(for PNG header files)
  if test -n "$PNGDIR"; then
    PNGDIR_INC="$PNGDIR/include $PNGDIR"
  fi 
  W2_FIND_HEADER_AND_APPEND("$PNGDIR_INC", "$png_inc_search_path", "png.h", PNG_CFLAGS)
  AC_SUBST(PNG_CFLAGS)

  W2_CHECKING_LIBRARY(png)
  W2_FIND_LIBRARY_AND_APPEND("$PNGDIR", "$png_lib_search_path", "png", PNG_LIBS)
  AC_SUBST(PNG_LIBS)

])

AC_DEFUN([CHECK_NETCDF],[

   # The build distribution script hard codes the NCDIR path to our build
   # if we are building netcdf from source in 3rd_party. These paths are used
   # if that is not the case (such as using system libraries)
   #netcdf_inc_search_path="/usr/include"
   #netcdf_lib_search_path="/usr/lib64"
   netcdf_inc_search_path="$prefix/include"
   netcdf_lib_search_path="$prefix/lib"

   AC_CHECKING(for NetCDF header files)
   W2_FIND_HEADER_AND_APPEND("$NCDIR", "$netcdf_inc_search_path", "netcdf.h", NETCDF_CFLAGS)
   AC_SUBST(NETCDF_CFLAGS)

   W2_CHECKING_LIBRARY(NetCDF)
   W2_FIND_LIBRARY_AND_APPEND("$NCDIR", "$netcdf_lib_search_path", "netcdf_c++", NETCDF_LIBS)
   W2_FIND_LIBRARY_AND_APPEND("$NCDIR", "$netcdf_lib_search_path", "netcdf", NETCDF_LIBS)
   AC_SUBST(NETCDF_LIBS)
])

AC_DEFUN([CHECK_GRIB2C],[

   # Use third party built path
   #grib2c_inc_search_path="/usr/include"
   #grib2c_lib_search_path="/usr/lib64"
   grib2c_inc_search_path="$prefix/include"
   grib2c_lib_search_path="$prefix/lib"

   AC_CHECKING(for grib2c header files)
   W2_FIND_HEADER_AND_APPEND("$GRIB2CDIR", "$grib2c_inc_search_path", "grib2.h", GRIB2C_CFLAGS)
   AC_SUBST(GRIB2C_CFLAGS)

   W2_CHECKING_LIBRARY(Grib2C)
   W2_FIND_LIBRARY_AND_APPEND("$GRIB2CDIR", "$grib2c_lib_search_path", "grib2c", GRIB2C_LIBS)
   #W2_FIND_LIBRARY_AND_APPEND("$GRIB2CDIR", "$grib2c_lib_search_path", "g2c_v1.6.0", GRIB2C_LIBS)
   AC_SUBST(GRIB2C_LIBS)
])

AC_DEFUN([CHECK_GDAL],[
  W2_WITH_GDAL()
  if test x"$gdal" = xtrue
  then
    GDAL_CFLAGS="`${prefix}/bin/gdal-config --cflags`"
    GDAL_LIBS="`${prefix}/bin/gdal-config --libs` `${prefix}/bin/gdal-config --dep-libs`"
  fi
  AC_SUBST(GDAL_CFLAGS)
  AC_SUBST(GDAL_LIBS)
])

AC_DEFUN([CHECK_FAM],[
  fam_search_path="/usr/include"

  AC_CHECKING(for FAM files)
  W2_FIND_HEADER_AND_APPEND("$FAMDIR", "$fam_search_path", "sys/inotify.h", FAMINCLUDE)
  AC_SUBST(FAMINCLUDE)

# inotify is built in glib, so no need to check library
# W2_CHECKING_LIBRARY(FAM)
# W2_FIND_LIBRARY_AND_APPEND("$FAMDIR", "$fam_search_path", "fam", FAMLIB)
# AC_SUBST(FAMLIB)

])

AC_DEFUN([CHECK_COMPRESSION],[

    # Use third party built path
    #z_inc_search_path="/usr/include"
    #z_lib_search_path="/usr/lib64"
    z_inc_search_path="$prefix/include"
    z_lib_search_path="$prefix/lib"

    # User system bzip...
    bz_inc_search_path="/usr/include"
    bz_lib_search_path="/usr/lib64"

    AC_CHECKING(for zlib header files)
    W2_FIND_HEADER_AND_APPEND("$ZDIR", "$z_inc_search_path", "zlib.h", ZLIB_CFLAGS)

    W2_CHECKING_LIBRARY(zlib)
    W2_FIND_LIBRARY_AND_APPEND("$ZDIR", "$z_lib_search_path", "z", ZLIB_LIBS)

    AC_CHECKING(for bzip header files)
    W2_FIND_HEADER_AND_APPEND("$BZDIR", "$bz_inc_search_path", "bzlib.h", BZLIB_CFLAGS)

    W2_CHECKING_LIBRARY(bzlib)
    W2_FIND_LIBRARY_AND_APPEND("$BZDIR", "$bz_lib_search_path", "bz2", BZLIB_LIBS)
])

AC_DEFUN([CHECK_EXTRAS],[
    if test x"${tdwr}" = xtrue; then
        echo "Building TDWRIngest? ... yes";
        TDWRINGEST="TDWRIngest";
        AC_SUBST(TDWRINGEST)
    fi
])

AC_DEFUN([W2_CONFIGURE_W2],[

  #### Configure only stuff needed for W2 directory
  W2_CONFIGURE_SHARED

  W2_WITH_RSSD

])

AC_DEFUN([W2_CONFIGURE_W2EXT],[

  #### Configure only stuff needed for W2EXT directory
  W2_CONFIGURE_SHARED
])

AC_DEFUN([W2_CONFIGURE_W2CONVERTERS],[
  CHECK_PNG
  CHECK_GDAL

  DISPLAY_3rdPARTY_LIBS="${DISPLAY_3rdPARTY_LIBS} ${PNG_LIBS}"
  DISPLAY_3rdPARTY_INCLUDES="${DISPLAY_3rdPARTY_INCLUDES} ${PNG_CFLAGS}"
  AC_SUBST(DISPLAY_3rdPARTY_LIBS)
  AC_SUBST(DISPLAY_3rdPARTY_INCLUDES)
])

AC_DEFUN([W2_CONFIGURE_W2TOOLS],[

  #### Configure only stuff needed for W2TOOLS directory
  W2_CONFIGURE_SHARED
  W2_CONFIGURE_W2CONVERTERS

])

AC_DEFUN([W2_CONFIGURE_W2ALGS],[

  #### Configure only stuff needed for W2ALGS directory
  W2_CONFIGURE_SHARED

  W2ALGS_WITH_TDWR
  W2ALGS_WITH_DEALIAS
  W2_ENABLE_NETSSAP

])

AC_DEFUN([W2_CONFIGURE_SHARED],[

  AC_REQUIRE([AC_CANONICAL_HOST])

  #### Stuff shared by W2, W2Algs, W2Tools
  W2_WITH_RSSD

  # SOURCELIBS has been set by now
  AC_SUBST(SOURCELIBS)

  CHECK_EXTRAS
  CHECK_NETCDF
  CHECK_LDUNITS
  CHECK_OPENSSL
  CHECK_FAM
  CHECK_COMPRESSION
  CHECK_GRIB2C

  # Always link to codedir lib and include FIRST to ensure
  # custom code over system
  CODE_3rdPARTY_LIBS="-L$prefix/lib"
  # Always link to codedir lib and include FIRST to ensure
  # custom code over system
  CODE_3rdPARTY_LIBS="-L$prefix/lib"
  CODE_3rdPARTY_INCLUDES="-I$prefix/include"
  DISPLAY_3rdPARTY_LIBS="-L$prefix/lib"
  DISPLAY_3rdPARTY_INCLUDES="-I$prefix/include"

  # Dualpol built into codedir first by script
  # Path is already our standard include/lib
  DUALPOL_CFLAGS=""
  DUALPOL_LIBS="-ldualpol -ldualpol_QPE"
  AC_SUBST(DUALPOL_CFLAGS)
  AC_SUBST(DUALPOL_LIBS)

  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${UDUNITS_LIBS}"
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${NETCDF_LIBS}"
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${GRIB2C_LIBS}"

  # System libs that can be in other locations
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${BZLIB_LIBS} ${ZLIB_LIBS}"
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} -lcurl"
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} -lm"
  AC_SUBST(CODE_3rdPARTY_LIBS)


  CODE_3rdPARTY_INCLUDES="${CODE_3rdPARTY_INCLUDES} ${UDUNITS_CFLAGS}"
  CODE_3rdPARTY_INCLUDES="${CODE_3rdPARTY_INCLUDES} ${NETCDF_CFLAGS}"
  CODE_3rdPARTY_INCLUDES="${CODE_3rdPARTY_INCLUDES} ${GRIB2C_CFLAGS}"
  CODE_3rdPARTY_INCLUDES="${CODE_3rdPARTY_INCLUDES} ${ZLIB_CFLAGS} ${BZLIB_CFLAGS}"
  AC_SUBST(CODE_3rdPARTY_INCLUDES)

  # Ok..make sure we hard link to the third party folder when making binaries.
  # This removes the need for LD_LIBRARY_PATH which is flawed and ensures we don't
  # use the wrong library version.  The downside is the build can't move
  LDFLAGS="$LDFLAGS -Wl,-rpath=$prefix/lib"
  AC_SUBST(LDFLAGS)
])


##### CODEINCLUDES and CODELIBRARIES are needed by algorithms
#
AC_DEFUN([CODE_CONFIGURE],[

  AC_CHECKING(for CODE header files)
  if test -n "$prefix"; then
     prefix_INC="$prefix/include/CODE  $prefix"
  fi 
  W2_FIND_HEADER_AND_APPEND("$prefix_INC", "$code_search_path", "data_object/code_Image.h", CODEINCLUDE)
  CODEINCLUDE="${CODEINCLUDE} ${CODE_3rdPARTY_INCLUDES}"
  AC_SUBST(CODEINCLUDE)

  AC_SUBST(BOOST_CFLAGS)
  AC_SUBST(BOOST_LIBS)

  W2_CHECKING_LIBRARY(CODE)
  W2_FIND_LIBRARY_AND_APPEND("$prefix", "$code_search_path", "sources", CODELIBRARIES)
  for tmplib in w2netcdf w2algs util_alg w2gis c_datatype ; do
    W2_FIND_LIBRARY_AND_APPEND("$prefix", "$code_search_path", $tmplib, CODELIBRARIES)
  done
  # gribw2 needs fam always
  AC_CHECKING(for FAM and FAM_NOTIFIER)
  W2_FIND_LIBRARY_AND_APPEND("$prefix", "$code_search_path", fam_notifier, CODELIBRARIES)
  for tmplib in data_object wdssii ; do
    W2_FIND_LIBRARY_AND_APPEND("$prefix", "$code_search_path", $tmplib, CODELIBRARIES)
  done

  CODELIBRARIES="${CODELIBRARIES} ${SOURCELIBS} ${CODE_3rdPARTY_LIBS}"
  AC_SUBST(CODELIBRARIES)
])

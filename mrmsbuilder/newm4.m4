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

AC_DEFUN([W2_WITH_QT],
    [AC_ARG_WITH([qt],
                 [AC_HELP_STRING([--with-qt],[build Qt GUI apps (default=no)])],
                 [case "${withval}" in
                   no) qt=false;;
                   yes) qt=true;;
                   *) AC_MSG_ERROR([bad value ${withval} for --with-qt]);;
                  esac],[qt=false])
     AM_CONDITIONAL(COND_QT, test x$qt = xtrue)
    ]
)
AC_DEFUN([W2_WITH_WX],
    [AC_ARG_WITH([wx],
                 [AC_HELP_STRING([--with-wx],[build wxWidgets GUI apps (default=no)])],
                 [case "${withval}" in
                   no) wx=false;;
                   yes) wx=true;;
                   *) AC_MSG_ERROR([bad value ${withval} for --with-wx]);;
                  esac],[wx=false])
     AM_CONDITIONAL(COND_WX, test x$wx = xtrue)
    ]
)
AC_DEFUN([W2_WITH_GTK],
    [AC_ARG_WITH([gtk],
                 [AC_HELP_STRING([--with-gtk],[build Gtk+ GUI apps (default=no)])],
                 [case "${withval}" in
                   no) gtk=false;;
                   yes) gtk=true;;
                   *) AC_MSG_ERROR([bad value ${withval} for --with-gtk]);;
                  esac],[gtk=true])
     AM_CONDITIONAL(COND_GTK, test x$gtk = xtrue)
    ]
)
AC_DEFUN([W2_WITH_PYTHONDEV],
    [AC_ARG_WITH([pythondev],
                 [AC_HELP_STRING([--with-pythondev],[build python development (default=no)])],
                 [case "${withval}" in
                   no) pythondev=false;;
                   yes) pythondev=true;;
                   *) AC_MSG_ERROR([bad value ${withval} for --with-pythondev]);;
                  esac],[pythondev=false])
     AM_CONDITIONAL(COND_PYTHONDEV, test x$pythondev = xtrue)
     dnl if test x"${pythondev}" = xtrue ; then
     dnl   AC_DEFINE([WITH_PYTHONDEV], [], [w2 python development support])
     dnl fi
    ]
)
AC_DEFUN([W2_WITH_FAM],
    [AC_ARG_WITH([fam],
                 [AC_HELP_STRING([--with-fam],[w2 event notification via inotify (default=yes)])],
                 [case "${withval}" in
                   no) fam=false;;
                   yes) fam=true;;
                   *) AC_MSG_ERROR([bad value ${withval} for --with-fam]);;
                  esac],[fam=true])
     AM_CONDITIONAL(COND_FAM, test x$fam = xtrue)
     if test x"${fam}" = xtrue ; then
        AC_DEFINE([WITH_FAM], [], [w2 event notification via FAM])
     fi
    ]
)
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

AC_DEFUN([W2_WITH_SDTS],
  [AC_ARG_WITH([sdts],
               [AC_HELP_STRING([--with-sdts],[support USGS terrain (default=no)])],
               [case "${withval}" in
                no) sdts=false;;
                yes) sdts=true;;
                *) AC_MSG_ERROR([bad value ${withval} for --with-sdts]);;
                esac],[sdts=false])
   AM_CONDITIONAL(SDTS, test x$sdts = xtrue)
  ]
)

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

AC_DEFUN([W2_ENABLE_HIRES],
    [AC_ARG_ENABLE(hires,
        [AC_HELP_STRING([--disable-hires],[turn off hires support (default=yes)])],
        [if test x"${enableval}" = xyes; then 
            hires=true
        elif test x"${enableval}" = xno; then
            hires=false
        else
            AC_MSG_ERROR(bad value ${enableval} for --enable-hires)
        fi],
        [hires=false]
    )
    AM_CONDITIONAL(HIRES, test x"${hires}" = xtrue)
    AC_MSG_RESULT("Building hires? ... ${hires}")
# hires is now in w2ext and is not pre-linked.
#    if test x"${hires}" = xtrue; then
#         SOURCELIBS="${SOURCELIBS} -lhires"
#    fi
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

AC_DEFUN([W2_ENABLE_NEXRAD],
    [AC_ARG_ENABLE(nexrad,
        [AC_HELP_STRING([--disable-nexrad],[turn off nexrad support])],
        [if test x"${enableval}" = xyes; then 
            nexrad=true
        elif test x"${enableval}" = xno; then
            nexrad=false
        else
            AC_MSG_ERROR(bad value ${enableval} for --enable-nexrad)
        fi],
        [nexrad=true]
    )
    AM_CONDITIONAL(NEXRAD, test x"${nexrad}" = xtrue)
    AC_MSG_RESULT("Building nexrad? ... ${nexrad}")
# nexrad now an extension library
#    if test x"${nexrad}" = xtrue; then
#         SOURCELIBS="${SOURCELIBS} -lw2nexrad"
#    fi
    ]
)

AC_DEFUN([W2_ENABLE_PSQL],
    [AC_ARG_ENABLE(psql,
        [AC_HELP_STRING([--enable-psql],[turn on psql support])],
        [if test x"${enableval}" = xyes; then 
            psql=true
        elif test x"${enableval}" = xno; then
            psql=false
        else
            AC_MSG_ERROR(bad value ${enableval} for --enable-psql)
        fi],
        [psql=false]
    )
    AM_CONDITIONAL(PSQL, test x"${psql}" = xtrue)
    AC_MSG_RESULT("Building psql? ... ${psql}")
    if test x"${psql}" = xtrue; then
         W2_FIND_LIBRARY_AND_APPEND("$prefix", "$code_search_path", "w2psql", SOURCELIBS)
    fi
    ]
)

AC_DEFUN([W2_ENABLE_ORPG],
    [AC_ARG_ENABLE(orpg,
        [AC_HELP_STRING([--enable-orpg],[turn on orpg support])],
        [if test x"${enableval}" = xyes; then
            orpg=true
        elif test x"${enableval}" = xno; then
            orpg=false
        else
            AC_MSG_ERROR(bad value ${enableval} for --enable-orpg)
        fi],
        [orpg=false]
    )
    AM_CONDITIONAL(ORPG, test x"${orpg}" = xtrue)
    AC_MSG_RESULT("Building orpg? ... ${orpg}")
# orpg_wdssii now in w2ext
#    if test x"${orpg}" = xtrue; then
#         SOURCELIBS="${SOURCELIBS} -lorpg_wdssii"
#    fi
    ]
)

AC_DEFUN([W2_ENABLE_WISH],
    [AC_ARG_ENABLE(wish,
        [AC_HELP_STRING([--disable-orpg],[turn off wish support])],
        [if test x"${enableval}" = xyes; then
            wish=true
        elif test x"${enableval}" = xno; then
            wish=false
        else
            AC_MSG_ERROR(bad value ${enableval} for --enable-wish)
        fi],
        [wish=false]
    )
    AM_CONDITIONAL(WISH, test x"${wish}" = xtrue)
    AC_MSG_RESULT("Building wish? ... ${wish}")
# wish now in w2ext
#    if test x"${wish}" = xtrue; then
#         SOURCELIBS="${SOURCELIBS} -lwish"
#    fi
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

AC_DEFUN([CHECK_BOOST],[
  boost_include_path="$prefix $code_search_path $PWD/.. /usr/include/boost141 /usr/include/boost133"
  boost_lib_path="$prefix $code_search_path $PWD/.. /usr/lib/boost141 /usr/lib/boost133"

  AC_CHECKING(for BOOST thread header files)
  W2_FIND_HEADER_AND_APPEND("$BOOST_INCLUDE", "$boost_include_path", "boost/thread.hpp", BOOST_CFLAGS)

  W2_CHECKING_LIBRARY(BOOST)
  W2_FIND_LIBRARY_AND_APPEND("$BOOST_LIB", "$boost_lib_path", "boost_thread-mt", BOOST_LIBS)
])

AC_DEFUN([CHECK_GL],[
   gl_lib_search_path="/usr/lib64"
   gl_inc_search_path="/usr/include"

   AC_CHECKING(for GL header files)
   W2_FIND_HEADER_AND_APPEND("$GLDIR", "$gl_inc_search_path", "GL/gl.h", GL_CFLAGS)
   AC_SUBST(GL_CFLAGS)

   W2_CHECKING_LIBRARY(GL)
   W2_FIND_LIBRARY_AND_APPEND("$GLDIR", "$gl_lib_search_path", "opengl32 GL", GL_LIBS)
   W2_FIND_LIBRARY_AND_APPEND("$GLDIR", "$gl_lib_search_path", "glu32 GLU", GL_LIBS)
   AC_SUBST(GL_LIBS)
])

AC_DEFUN([CHECK_FREETYPE],[
  ft_lib_search_path="/usr/lib64"
  ft_inc_search_path="/usr/include /usr/include/freetype2"

  AC_CHECKING(for FREETYPE header files)
 
  # Usually in /usr/include/freetype2
  W2_FIND_HEADER_AND_APPEND("$FREETYPEDIR_INC", "$ft_inc_search_path", "freetype/freetype.h", FREETYPE_CFLAGS)

  # Usually in /usr/include
  W2_FIND_HEADER_AND_APPEND("$FREETYPEDIR_INC", "$ft_inc_search_path", "ft2build.h", FREETYPE_CFLAGS)
  AC_SUBST(FREETYPE_CFLAGS)

  W2_CHECKING_LIBRARY(freetype)
  W2_FIND_LIBRARY_AND_APPEND("$FREETYPEDIR", "$ft_lib_search_path", "freetype", FREETYPE_LIBS)
  AC_SUBST(FREETYPE_LIBS)

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

AC_DEFUN([CHECK_CODE_OS],[

  case "$host_os" in

    *mingw*)
    AC_DEFINE([GLEW_STATIC], [], [wg builds glew itself and links it static])
    mingw_search_path="/mingw"
    W2_FIND_LIBRARY_AND_APPEND($mingw_search_path, "", "shlwapi", CODE_OS_LIBS)
    W2_FIND_LIBRARY_AND_APPEND($mingw_search_path, "", "ws2_32", CODE_OS_LIBS)
    W2_FIND_LIBRARY_AND_APPEND($mingw_search_path, "", "imagehlp", CODE_OS_LIBS)
    CODE_OS_CPPFLAGS="-DCURL_STATICLIB -DGLEW_STATIC"
    ;;

    *darwin*)
    AC_DEFINE([OS_X], [], [Are we compiling on OS/X?])
    CODE_OS_LIBS="$CODE_OS_LIBS -framework Carbon";;

    *)
    CODE_OS_LIBS="$CODE_OS_LIBS -ldl";;

  esac
  case "$host_vendor" in

    Sun*|sun*|SUN*)
    CODE_OS_LIBS="$CODE_OS_LIBS -lposix4";;

  esac
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

AC_DEFUN([CHECK_DUALPOL],[
    PKG_CHECK_MODULES([DUALPOL],
                      [dualpol],
                      [],
                      [dnl if we can't find the pkg-config file, use the standard WDSS2 search procedure
                       dualpol_search_path="$prefix $WDSSIIDIR $HOME/WDSS2/include $HOME/WDSS2/lib"
                       AC_CHECKING(for dualpol header files)
                       W2_FIND_HEADER_AND_APPEND("$DUALPOLDIR", "$dualpol_search_path", "dualpol/dualpol.h", DUALPOL_CFLAGS)
                       W2_CHECKING_LIBRARY(dualpol)
                       W2_FIND_LIBRARY_AND_APPEND("$DUALPOLDIR", "$dualpol_search_path", "dualpol", DUALPOL_LIBS)])
    AC_SUBST(DUALPOL_CFLAGS)
    AC_SUBST(DUALPOL_LIBS)
])

AC_DEFUN([CHECK_DUALPOL_QPE],[
    PKG_CHECK_MODULES([DUALPOL_QPE],
                      [dualpol_QPE],
                      [],
                      [dnl if we can't find the pkg-config file, use the standard WDSS2 search procedure
                       dualpol_search_path="$prefix $WDSSIIDIR $HOME/WDSS2/include $HOME/WDSS2/lib"
                       AC_CHECKING(for dualpol-QPE header files)
                       W2_FIND_HEADER_AND_APPEND("$DUALPOLDIR", "$dualpol_search_path", "dualpol-QPE/RadialRainfallRates.h", DUALPOL_CFLAGS)
                       W2_CHECKING_LIBRARY(dualpol_QPE)
                       W2_FIND_LIBRARY_AND_APPEND("$DUALPOLDIR", "$dualpol_search_path", "dualpol_QPE", DUALPOL_LIBS)])
    AC_SUBST(DUALPOL_QPE_CFLAGS)
    AC_SUBST(DUALPOL_QPE_LIBS)
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
  W2_WITH_FAM()
  if test x"$fam" = xtrue
  then

    #fam_search_path="$WDSSIIDIR/include /usr/local /usr"
    fam_search_path="/usr/include"

    AC_CHECKING(for FAM files)
    W2_FIND_HEADER_AND_APPEND("$FAMDIR", "$fam_search_path", "sys/inotify.h", FAMINCLUDE)
    AC_SUBST(FAMINCLUDE)

#    inotify is built in glib, so no need to check library
#    W2_CHECKING_LIBRARY(FAM)
#    W2_FIND_LIBRARY_AND_APPEND("$FAMDIR", "$fam_search_path", "fam", FAMLIB)
#    AC_SUBST(FAMLIB)

   fi
])

dnl AC_DEFUN([CHECK_PSQL],[
dnl
dnl  if test x"$psql" = xtrue
dnl  then
dnl
dnl    psql_search_path="$WDSSIIDIR/include /usr/local /usr"
dnl
dnl    AC_CHECKING(for PostgreSQL files)
dnl    W2_FIND_HEADER_AND_APPEND("$PSQLDIR", "$psql_search_path", "libpq-fe.h", PSQLINCLUDE)
dnl    AC_SUBST(PSQLINCLUDE)
dnl
dnl    W2_CHECKING_LIBRARY(PostgreSQL)
dnl    W2_FIND_LIBRARY_AND_APPEND("$PSQLDIR", "$psql_search_path", "pq", PSQLLIB)
dnl    AC_SUBST(PSQLLIB)
dnl
dnl  fi
dnl])

AC_DEFUN([CHECK_ORPGINFR],[

  # Regardless of which libraries we need, we always need the headers...
  W2_CHECK_HEADERS(
    ORPGDIR,
    [
      $ORPGDIR/include
      $ORPGDIR/lib/include
      $ORPGDIR/include/orpginfr/include
    ],
    [
      $prefix/include/orpginfr/include
      $HOME/include
      $HOME/include/orpginfr/include
      $HOME/WDSS2/include/orpginfr/include
      /usr/local/include
      /usr/include
      /usr/local/include/orpginfr/include
      /usr/include/orpginfr/include
      /export/home/codeorpg/include
      /export/home/codeorpg/lib/include
      /users/opup/nightly/OPUP/include/orpg
      /nssl/nsslsun/wdssii/orpginfr/lib/include
      /home/wdssii/orpginfr/include
      /home/wdssii/include/orpginfr/include
      /home/wdssii/include
      $PWD/../orpginfr/include
      $PWD/../orpginfr/lib/include
      $PWD/../include/orpginfr/include
    ],
    rss.h,
    ORPGINCLUDE)

  if test x"$orpg" = xtrue; then # full ORPG

    # full orpg libraries...
    AC_CHECKING(for --- full ORPG libraries ---)
    W2_FIND_PATH(
      ORPGDIR,
      [
        $ORPGDIR/../lib/lnux_x86
      ],
      [
        /usr/local/lib
        /usr/lib
        /export/home/codeorpg/lib/slrs_spk
        $HOME/lib
        $HOME/WDSS2/lib
        /users/opup/nightly/OPUP/lib
      ],
      liborpg.so,
      ORPGLIB_DIR)

    orpglib1="-lrpgc -lorpg++ -lorpg -lhci -linfr -lobjcore"
    orpglib2="-lsocket -lelf -lnsl -lXm -lXt -lX11 -lMrm -lz -lm"
    ORPG_LIBS="-L${ORPGLIB_DIR} $orpglib1 $orpglib2"

  elif test x"$rssd" = xlibinfr; then

    # Using libinfr implementation of rss_notifier
    W2_CHECKING_LIBRARY([ORPG's infr libraries])
    orpg_search_path="$prefix $HOME $code_search_path /usr/local /usr $HOME/WDSS2"
    orpg_search_path="$orpg_search_path /nssl/nsslsun/wdssii/orpginfr /home/wdssii"
    orpg_search_path="$orpg_search_path $HOME/lib/irix $PWD/../lib/irix"
    orpg_search_path="$orpg_search_path /export/home/codeorpg/lib/slrs_spk"
    W2_FIND_LIBRARY("$ORPGDIR", "$orpg_search_path", "infr", orpg_lib_dir, orpg_lib_base)
    ORPG_LIBS="$orpg_lib_dir/$orpg_lib_base"

  elif test x"$rssd" = xglib; then

    # Using glib implementation of rss_notifier
    GLIB_REQUIRED=2.2.0
    PKG_CHECK_MODULES(GLIB, glib-2.0 >= $GLIB_REQUIRED \
                            gobject-2.0 >= $GLIB_REQUIRED)
    ORPG_LIBS="$GLIB_LIBS"
    ORPGINCLUDE="$ORPGINCLUDE $GLIB_CFLAGS"

  else

    AC_MSG_ERROR([Don't know which implementation of rss_notifier to use!])

  fi

  AC_SUBST(ORPGINCLUDE)
  AC_SUBST(ORPG_LIBS)
])


AC_DEFUN([CHECK_WX],[
  W2_WITH_WX()
  if test x$wx = xtrue
  then
    WX_CC="`wx-config --cc`"
    WX_CXX="`wx-config --cxx`"
    WX_CXXFLAGS="`wx-config --cxxflags`"
    WX_CPPFLAGS="`wx-config --cppflags`"
    WX_LIBS="`wx-config --libs` `wx-config --gl-libs`"
  fi

  AC_SUBST(WX_CC)
  AC_SUBST(WX_CXX)
  AC_SUBST(WX_CXXFLAGS)
  AC_SUBST(WX_CPPFLAGS)
  AC_SUBST(WX_LIBS)
])

AC_DEFUN([CHECK_GTK],[
  W2_WITH_GTK()
  if test x$gtk = xtrue
  then
    GLIB_REQUIRED=2.2.0
    PANGO_REQUIRED=1.2.0
    GTK_REQUIRED=2.2.0
    GTKGLEXT_REQUIRED=1.0.6

    # check for the glib/gtk libraries needed by wg2
    PKG_CHECK_MODULES(GLIB, glib-2.0 >= $GLIB_REQUIRED \
                            gthread-2.0 >= $GLIB_REQUIRED \
                            gobject-2.0 >= $GLIB_REQUIRED)
    PKG_CHECK_MODULES(GTK, gtk+-2.0 >= $GTK_REQUIRED)
    PKG_CHECK_MODULES(GTKGLEXT, gtkglext-1.0 >= $GTKGLEXT_REQUIRED,,AC_MSG_WARN([gtkglext not found; wgtk will not build]))
  else
    echo "GTK checking skipped ... --with-gtk not set."
  fi

  AC_SUBST(GLIB_CFLAGS)
  AC_SUBST(GLIB_LIBS)
  AC_SUBST(GTK_CFLAGS)
  AC_SUBST(GTK_LIBS)
  AC_SUBST(GTKGLEXT_CFLAGS)
  AC_SUBST(GTKGLEXT_LIBS)
])

AC_DEFUN([CHECK_PYTHONDEV],[
  W2_WITH_PYTHONDEV()
  if test x$pythondev = xtrue
  then

    # Start with the redhat 7 stock python-devel
    python_search_path="/usr/include/python2.7/"

    AC_CHECKING(for python development header files)
    W2_FIND_HEADER_AND_APPEND("$PYTHONDEVDIR", "$python_search_path", "Python.h", PYTHONDEVINCLUDE)
    AC_SUBST(PYTHONDEVINCLUDE)
  else
    echo "Python development checking skipped ... --with-pythondev not set."
  fi

])

AC_DEFUN([CHECK_QT],[
  W2_WITH_QT()
  if test x$qt = xtrue
  then

    ##### Qt

    # We need strict QTDIR following for auto building
    if test x"${QTDIR}" != x; then

      # Check for include and libs in QTDIR, first shared, than static
      AC_CHECKING("for --- Qt files --- QTDIR is hard set in environment to ${QTDIR} ---")
      AC_CHECK_FILE($QTDIR/include/qdom.h, QTINCLUDE="-I$QTDIR/include")
      AC_CHECK_FILE($QTDIR/lib/libqt.so, QTLIB="$QTDIR/lib/libqt.so")
      if test x"${QTLIB}" = x; then
        # Static qt needs to link explicitly to certain X libraries or it fails
        AC_CHECK_FILE($QTDIR/lib/libqt.a, QTLIB="$QTDIR/lib/libqt.a";SOURCELIBS="${SOURCELIBS} -L/usr/X11R6/lib -lXft")
      fi
      if test x"${QTINCLUDE}" = x; then
       AC_MSG_ERROR( no include/qdom.h in ${QTDIR})
      fi
      if test x"${QTLIB}" = x; then
       AC_MSG_ERROR( no lib/libqt.* in ${QTDIR})
      fi
    else
      qt_search_path="/usr /usr/include/qt /usr/lib/qt3 /usr/lib/qt2 /usr/local/qt /usr/local/qt-2.2.2 /server/qt-2.2.3"
      AC_CHECKING(for Qt header files)
      W2_FIND_HEADER_AND_APPEND("$QTDIR", "$qt_search_path", "qdom.h", QTINCLUDE)
      W2_CHECKING_LIBRARY(qt)
      W2_FIND_LIBRARY_AND_APPEND("$QTDIR", "$qt_search_path", "qt", QTLIB)
    fi
  
    xpm_search_path="/usr/openwin /usr/X11R6 /usr $PWD/.."
    AC_CHECKING(for XPM header files)
    W2_FIND_HEADER_AND_APPEND("$XPMDIR", "$xpm_search_path", "X11/xpm.h", XPM_CFLAGS)
    W2_CHECKING_LIBRARY(Xpm)
    W2_FIND_LIBRARY_AND_APPEND("$XPMDIR", "$xpm_search_path", "Xpm", XPM_LIBS)
  fi

  AC_SUBST(QTINCLUDE)
  AC_SUBST(QTLIB)
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

AC_DEFUN([CHECK_SDTS_AND_STL],[

  ### SDTS

  if test x"$sdts" = xtrue; then

    sdts_search_path="/usr/local /usr $PWD/.."

    AC_CHECKING(for SDTS header files)
    W2_FIND_HEADER_AND_APPEND("$SDTSDIR", "$sdts_search_path", "sdts++/io/sio_Reader.h", SDTS_CFLAGS)

    W2_CHECKING_LIBRARY(SDTS)
    W2_FIND_LIBRARY_AND_APPEND("$SDTSDIR", "$sdts_search_path", "sdts", SDTS_LIBS)
    W2_FIND_LIBRARY_AND_APPEND("$SDTSDIR", "$sdts_search_path", "sysutils", SDTS_LIBS)

  fi

  case "$host" in

    *irix*)
    stlport_inc_search_path="$PWD/../STLport/stlport"
    stlport_lib_search_path="$PWD/../STLport"

    AC_CHECKING(for STLPORT header files)
    W2_FIND_HEADER_AND_APPEND("$STLPORTDIR", "$stlport_inc_search_path", "stl_user_config.h", STLPORT_CFLAGS)
 
    W2_CHECKING_LIBRARY(STLPORT)
    W2_FIND_LIBRARY_AND_APPEND("$STLPORTDIR", "$stlport_search_path", "stlport_gcc", STLPORT_LIBS)

  esac
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
  W2_ENABLE_NEXRAD
  W2_ENABLE_ORPG

])

AC_DEFUN([W2_CONFIGURE_W2EXT],[

  #### Configure only stuff needed for W2EXT directory
  W2_CONFIGURE_SHARED

  W2_ENABLE_HIRES
  W2_ENABLE_WISH
  W2_ENABLE_NEXRAD
  W2_ENABLE_ORPG
])

AC_DEFUN([W2_CONFIGURE_WG],[
  #### Libraries only needed by the display
  #
  # Ok, if no GTK asked for, skip all the display check stuff
  CHECK_GTK
  if test x$gtk = xtrue; then
    CHECK_QT
    CHECK_WX
    CHECK_GL
    CHECK_FREETYPE

    DISPLAY_3rdPARTY_LIBS="${DISPLAY_3rdPARTY_LIBS} ${QTLIB} ${FREETYPE_LIBS} ${GL_LIBS}"
    DISPLAY_3rdPARTY_INCLUDES="${DISPLAY_3rdPARTY_INCLUDES} ${GL_CFLAGS} ${XPM_CFLAGS} ${QTINCLUDE} ${FREETYPE_CFLAGS}"
  fi

  AC_SUBST(DISPLAY_3rdPARTY_LIBS)
  AC_SUBST(DISPLAY_3rdPARTY_INCLUDES)
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
  W2_CONFIGURE_WG

])

AC_DEFUN([W2_CONFIGURE_W2ALGS],[

  #### Configure only stuff needed for W2ALGS directory
  W2_CONFIGURE_SHARED

  #### Lightning still has a gui and needs QT
  #### Libraries only needed by the display
  #CHECK_QT
  #DISPLAY_3rdPARTY_LIBS="${DISPLAY_3rdPARTY_LIBS} ${QTLIB}"
  #DISPLAY_3rdPARTY_INCLUDES="${DISPLAY_3rdPARTY_INCLUDES} ${QTINCLUDE}"
  #AC_SUBST(DISPLAY_3rdPARTY_LIBS)
  #AC_SUBST(DISPLAY_3rdPARTY_INCLUDES)
  #### CHECK_G2C

  W2ALGS_WITH_TDWR
  W2ALGS_WITH_DEALIAS
  W2_ENABLE_NETSSAP

])

AC_DEFUN([W2_CONFIGURE_SHARED],[

  AC_REQUIRE([AC_CANONICAL_HOST])

  #### Stuff shared by W2, W2Algs, W2Tools
  W2_ENABLE_PSQL
  W2_WITH_RSSD
  W2_WITH_SDTS
  W2_WITH_QT
  W2_WITH_WX
  W2_WITH_GTK

  # SOURCELIBS has been set by now
  AC_SUBST(SOURCELIBS)

  CHECK_EXTRAS
  CHECK_SDTS_AND_STL
  CHECK_ORPGINFR
  CHECK_NETCDF
  CHECK_LDUNITS
  # CHECK_BOOST  -- not used
  CHECK_OPENSSL
  #CHECK_PSQL -- not used
  CHECK_PYTHONDEV
  CHECK_FAM
  CHECK_COMPRESSION
  CHECK_CODE_OS
  CHECK_GRIB2C
  CHECK_DUALPOL
  CHECK_DUALPOL_QPE

  # Always link to codedir lib and include FIRST to ensure
  # custom code over system
  CODE_3rdPARTY_LIBS="-L$prefix/lib"
  CODE_3rdPARTY_INCLUDES="-I$prefix/include"
  DISPLAY_3rdPARTY_LIBS="-L$prefix/lib"
  DISPLAY_3rdPARTY_INCLUDES="-I$prefix/include"

  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${SDTS_LIBS} ${STLPORT_LIBS}"
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${ORPG_LIBS}"
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${UDUNITS_LIBS}"
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${NETCDF_LIBS}"
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${GRIB2C_LIBS}"

  # System libs that can be in other locations
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${BZLIB_LIBS} ${ZLIB_LIBS}"
#  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${PSQLLIB}"
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} -lcurl"
  CODE_3rdPARTY_LIBS="${CODE_3rdPARTY_LIBS} ${CODE_OS_LIBS} -lm"
  AC_SUBST(CODE_3rdPARTY_LIBS)


  CODE_3rdPARTY_INCLUDES="${CODE_3rdPARTY_INCLUDES} ${SDTS_CFLAGS} ${STLPORT_CFLAGS}"
  CODE_3rdPARTY_INCLUDES="${CODE_3rdPARTY_INCLUDES} ${UDUNITS_CFLAGS}"
  CODE_3rdPARTY_INCLUDES="${CODE_3rdPARTY_INCLUDES} ${ORPGINCLUDE}"
  CODE_3rdPARTY_INCLUDES="${CODE_3rdPARTY_INCLUDES} ${NETCDF_CFLAGS}"
  CODE_3rdPARTY_INCLUDES="${CODE_3rdPARTY_INCLUDES} ${GRIB2C_CFLAGS}"
  CODE_3rdPARTY_INCLUDES="${CODE_3rdPARTY_INCLUDES} ${ZLIB_CFLAGS} ${BZLIB_CFLAGS}"
  CODE_3rdPARTY_INCLUDES="${CODE_3rdPARTY_INCLUDES} ${CODE_OS_CPPFLAGS}"
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
  for tmplib in w2netcdf w2algs util_alg w2gis c_datatype rss_notifier ; do
    W2_FIND_LIBRARY_AND_APPEND("$prefix", "$code_search_path", $tmplib, CODELIBRARIES)
  done
  W2_WITH_FAM()
  if test x"$fam" = xtrue; then
    W2_FIND_LIBRARY_AND_APPEND("$prefix", "$code_search_path", fam_notifier, CODELIBRARIES)
  fi
  for tmplib in data_object wdssii ; do
    W2_FIND_LIBRARY_AND_APPEND("$prefix", "$code_search_path", $tmplib, CODELIBRARIES)
  done

  CODELIBRARIES="${CODELIBRARIES} ${SOURCELIBS} ${CODE_3rdPARTY_LIBS}"
  AC_SUBST(CODELIBRARIES)
])

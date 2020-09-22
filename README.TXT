NSSL Package for building MRMS.
Robert Toomey May 2017

INSTRUCTIONS: 
0. Python versions are now in flux with different names such as python2, python, python38, etc.
I'd recommend doing something like
"python2 build.py"
or 
"python2 build.py configs/another.cfg" to choose a non-default configuration

or you can try the default which might fail due to python naming, etc.
1. Type "./build" to run the script
2. Update your shell env to have your proper SVN settings if 
   needed.

  This interactive script will help you build a fresh checkout
you can use to code MRMS.
  After building a set of SVN/environments settings will be given,
you will have to source those/add to your environment if you
want to change code and check it in.  You can still snv diff, etc.
by default.

--------------------------------------------------------------

2017-05-12: Initial checkin of builder package.
  Currently the script always tries to build wg, which means
  the w2tools build will end if you're missing gtk and opengl
  for display. If you are ok with this you can still build the
  w2convertors by going into that directory and typing make 
  install.

--------------------------------------------------------------

Robert Toomey

#                                               -*- Autoconf -*-
# Process this file with autoconf to produce a configure script.

AC_PREREQ(2.61)
AC_INIT([papertape], [1.1], [nf6x@nf6x.net], [papertape], [http://www.nf6x.net/tag/papertape])
AC_CONFIG_SRCDIR([pbmtape.cc])
AC_CONFIG_HEADER([config.h])
AC_CONFIG_AUX_DIR([build-aux])
AC_CONFIG_MACRO_DIR([build-aux])
AM_INIT_AUTOMAKE
AM_SILENT_RULES([yes])

AC_SUBST(CFLAGS, [-O2])
AC_SUBST(CXXFLAGS, [-O2])

# Checks for programs.
AC_PROG_CXX
AC_PROG_CC

# Checks for libraries.

# Checks for header files.
AC_HEADER_STDC

# Checks for typedefs, structures, and compiler characteristics.
AC_C_CONST

# Checks for library functions.
AC_CHECK_FUNCS(arc4random)
AC_CHECK_FUNCS(srandomdev)

AC_CONFIG_FILES([Makefile])

AH_BOTTOM([
/* We prefer to use arc4random(), but we'll settle for random() if
   it is not available. */
#ifdef HAVE_ARC4RANDOM
#  define RAND arc4random()
#  define SRAND ;
#  define RANDFUNCS "arc4random()"
#else
#  define RAND random()
#  ifdef HAVE_SRANDOMDEV
#    define SRAND srandomdev()
#    define RANDFUNCS "random() + srandomdev()"
#  else
#    define SRAND srandom(time(NULL))
#    define RANDFUNCS "random() + srandom(time())"
#  endif
#endif
])


AC_OUTPUT

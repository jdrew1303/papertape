AUTOMAKE_OPTIONS = dist-bzip2 no-dist-gzip
ACLOCAL_AMFLAGS  = -I build-aux

bin_PROGRAMS  = pt_render pt_asc2baudot pt_marquee
bin_PROGRAMS += pt_and pt_or pt_invert pt_xor pt_random
bin_PROGRAMS += pt_tape2txt pt_setmsb

dist_bin_SCRIPTS = pt_tapein.py


pt_render_SOURCES  = pt_render.cc pbmtape.cc papertape.h

pt_asc2baudot_SOURCES = pt_asc2baudot.cc papertape.h

pt_marquee_SOURCES = pt_marquee.cc papertape.h

pt_and_SOURCES = pt_and.cc papertape.h

pt_or_SOURCES = pt_or.cc papertape.h

pt_invert_SOURCES = pt_invert.cc papertape.h

pt_xor_SOURCES = pt_xor.cc papertape.h

pt_random_SOURCES = pt_random.cc papertape.h

pt_tape2txt_SOURCES = pt_tape2txt.cc papertape.h

pt_setmsb_SOURCES = pt_setmsb.cc papertape.h

EXTRA_DIST = ECMA-10.pdf

CLEANFILES = *~

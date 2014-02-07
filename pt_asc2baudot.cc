/**************************************************************************
 * Copyright (C) 2010 Mark J. Blair, NF6X
 *
 * This file is part of Papertape.
 *
 *  Papertape is free software: you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation, either version 3 of the License, or
 *  (at your option) any later version.
 *
 *  Papertape is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with Papertape.  If not, see <http://www.gnu.org/licenses/>.
 **************************************************************************/

/*!
 * \file
 * \brief Main entry point of papertape ASCII to Baudot converter executable.
 *
 */ 


#include "papertape.h"



// Defines for asc2tty array
#define INVC	(unsigned char)0377		// invalid character mapping
#define FIGS_F 	(unsigned char)0200		// figures required flag
#define ETHR_F	(unsigned char)0100		// valid in either shift
#define LTRS	(unsigned char)0037		// letters shift character
#define FIGS	(unsigned char)0033		// figures shift character
#define MSK5	(unsigned char)0037		// mask off 5 LSBs
#define MSK7	(unsigned char)0177		// mask off 7 LSBs


//! Array for converting ASCII to 5-level TTY code.
//
//! 5 LSBs are significant.
//! Bit 7 set if figures shift required.
//! 0xff indicates invalid character mapping.
//! Lower-case mapped to upper-case
//! DEL mapped to LTRS
//! See also:
//! http://homepages.cwi.nl/~dik/english/codes/5tape.html#teletype
//! ascii(7)
//
unsigned char asc2tty[] = {
    0100, INVC, INVC, INVC, INVC, INVC, INVC, 0233, // NUL, ..., BEL
    INVC, INVC, 0110, INVC, INVC, 0102, INVC, INVC, // ..., LF, ..., CR
    INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, // ...
    INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, // ...

    0104, 0226, 0221, 0205, 0222, INVC, 0213, 0224, // SP, punct.
    0236, 0211, INVC, INVC, 0206, 0230, 0207, 0227, // punct.
    0215, 0235, 0223, 0220, 0212, 0201, 0225, 0234, // 0-7
    0214, 0203, 0216, 0217, INVC, INVC, INVC, 0223, // 8-9, punct

    INVC, 0030, 0023, 0016, 0022, 0020, 0026, 0013, // @, A-G
    0005, 0014, 0032, 0036, 0011, 0007, 0006, 0003, // H-O
    0015, 0035, 0012, 0024, 0001, 0034, 0017, 0031, // P-W
    0027, 0025, 0021, INVC, INVC, INVC, INVC, INVC, // X-Z, punct

    INVC, 0030, 0023, 0016, 0022, 0020, 0026, 0013, // ', a-g
    0005, 0014, 0032, 0036, 0011, 0007, 0006, 0003, // h-o
    0015, 0035, 0012, 0024, 0001, 0034, 0017, 0031, // p-w
    0027, 0025, 0021, INVC, INVC, INVC, INVC, LTRS  // x-z, punct
    
};



//! Print version and usage instructions to stderr.
//
void PrintHelp(ostream& os) {
    os << endl;
    os << PACKAGE_STRING << " by Mark J. Blair, NF6X <nf6x@nf6x.net>" << endl;
    os << "Copyright (C) 2010 Mark J. Blair. Released under GPLv3" << endl;
    os << endl;
    os << "Description:" << endl;
    os << "  pt_asc2baudot reads ASCII text from stdin, converts it to 5-bit TTY code," << endl;
    os << "  and outputs the converted data (suitable for input to pt_render) to stdout." << endl;
    os << endl;
    os << "Usage:" << endl;
    os << "  pt_asc2baudot [-v]"
       << endl;
    os << "    -v: Verbose mode. Informational messages will be printed to stderr." << endl;
    os << endl;
}



//! Main entry point.
//
int main(int argc, char **argv)
{
    int			opt;		        // used for arg parsing
    data_t		data;			// data to be output
    unsigned char	c;			// input character
    bool		FigF = false;		// in figures shift?
    int			n;			// loop counter
    bool		Verbose = false;	// verbose mode


    // Disable getopt()'s internal error messages
    opterr = 0;

    // Parse command-line arguments
    while ((opt = getopt(argc, argv, ":h")) != -1) {

	switch (opt) {

	  case 'h':			// help
	    PrintHelp(cerr);
	    exit(0);
	    break;

	  case 'v':
	    Verbose = true;
	    break;

	  case ':':			// missing argument
	    cerr << "ERROR: option -"
		 << (unsigned char)optopt
		 << " requires an argument."
		 << endl;
	    PrintHelp(cerr);
	    exit(1);
	    break;

	  case '?':			// unknown option
	    cerr << "ERROR: option -"
		 << (unsigned char)optopt
		 << " is not valid."
		 << endl;
	    PrintHelp(cerr);
	    exit(1);
	    break;

	  default:
	    cerr << "ERROR: unknown error during argument parsing."
		 << endl;
	    PrintHelp(cerr);
	    exit(1);
	    break;
	}

    }

    //argc -= optind;
    //argv += optind;


    // read data to be transcoded from stdin
    if (Verbose) {
	cerr << "Reading from stdin..." << endl;
    }

    while (cin.good()) {
	c = (unsigned char)cin.get();
	if (!cin.good()) {
	    break;
	}

	// convert char to 5-level code
	c = asc2tty[c & MSK7];

	// check for valid char mapping
	if (c == INVC) {
	    // skip invalid character
	    continue;
	}

	// need to change shift?
	if (!(c & ETHR_F) && (c & FIGS_F) && !FigF) {
	    // Need figures shift
	    data.push_back(FIGS);
	    FigF = true;
	} else if (!(c & ETHR_F) && !(c & FIGS_F) && FigF) {
	    // Need letters shift
	    data.push_back(LTRS);
	    FigF = false;
	}

	data.push_back(c & MSK5);
    }

    // output the data
    for (n=0; n < (int)data.size(); n++) {
	cout.put(data[n]);
    }

    if (Verbose) {
	cerr << "Output " << dec << data.size() << " symbols." << endl;
    }

    return 0;
}

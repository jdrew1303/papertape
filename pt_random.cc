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
 * \brief Main entry point of papertape pseudorandom data generator executable.
 *
 */ 


#include "papertape.h"


//! Print version and usage instructions to stderr.
//
void PrintHelp(ostream& os) {
    os << endl;
    os << PACKAGE_STRING << " by Mark J. Blair, NF6X <nf6x@nf6x.net>" << endl;
    os << "Copyright (C) 2010 Mark J. Blair. Released under GPLv3" << endl;
    os << endl;
    os << "Usage:" << endl;
    os << "  pt_random [-v] <stream_length>"
       << endl;
    os << endl;
    os << "Description:" << endl;
    os << "  pt_random generates a stream of pseudorandom data suitable for input to" << endl;
    os << "  pt_render and other papertape suite tools." << endl;
    os << endl;
    os << "Options:" << endl;
    os << "  -v: Verbose mode. Informational messages will be printed to stderr." << endl;
    os << endl;
}



//! Main entry point.
//
int main(int argc, char **argv)
{
    int			opt;		        // used for arg parsing
    unsigned char	c;			// output character
    int			n;			// loop counters
    bool		Verbose = false;	// verbose mode
    int			StreamLen = 0;		// length of random number stream


    // Disable getopt()'s internal error messages
    opterr = 0;

    // Parse command-line arguments
    while ((opt = getopt(argc, argv, ":hv")) != -1) {

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

    argc -= optind;
    argv += optind;

    if (argc != 1) {
	cerr << "ERROR: Wrong number of arguments." << endl;
	PrintHelp(cerr);
	exit(1);
    }

    StreamLen = atoi(argv[0]);

    if (Verbose) {
        cerr << "Using "
             << RANDFUNCS
             << " for random number generation."
             << endl;
    }

    // output the data
    SRAND;
    for (n=0; n < StreamLen; n++) {
	c = RAND % 0x100;
	cout.put(c);;
    }

    if (Verbose) {
	cerr << "Output " << dec << StreamLen << " symbols." << endl;
    }


    return 0;


}

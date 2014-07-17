/**************************************************************************
 * Copyright (C) 2014 Mark J. Blair, NF6X
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
 * \brief Main entry point of papertape text converter executable.
 *
 */ 


#include "papertape.h"


//! Print version and usage instructions to stderr.
//
void PrintHelp(ostream& os) {
    os << endl;
    os << PACKAGE_STRING << " by Mark J. Blair, NF6X <nf6x@nf6x.net>" << endl;
    os << "Copyright (C) 2014 Mark J. Blair. Released under GPLv3" << endl;
    os << endl;
    os << "Usage:" << endl;
    os << "  pt_setmsb [-v] <file1>"
       << endl;
    os << endl;
    os << "Description:" << endl;
    os << "  pt_setmsb reads data from an input file, sets the most significant," <<endl;
    os << "  bit, and outputs the resulting data to stdout." << endl;
    os << "  NUL bytes in input stream are passed through unmodified." << endl;
    os << "  If the input filename is not specified, then input will be read from stdin." << endl;
    os << endl;
    os << "Options:" << endl;
    os << "  -v: Verbose mode. Informational messages will be printed to stderr." << endl;
    os << endl;
}


int process_data(istream &in, ostream &out) {
    int 		StreamLen = 0;
    unsigned char	c;

   // output the data
    while (in.good()) {
	c = (unsigned char)in.get();

	if (in.good()) {
	    ++StreamLen;
	    if (c == 0x00) {
		out.put(c);
	    } else {
		out.put(c | 0x80);
	    }
	}
    }
    return StreamLen;
}


//! Main entry point.
//
int main(int argc, char **argv)
{
    int			opt;		        // used for arg parsing
    ifstream		in1;			// input stream
    bool		Verbose = false;	// verbose mode
    int			StreamLen = 0;		// length of output stream


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

    if (argc > 1) {
	cerr << "ERROR: Wrong number of arguments." << endl;
	PrintHelp(cerr);
	exit(1);
    } else if (argc == 1) {
	// Open input stream
	in1.open(argv[0], ifstream::in | ifstream::binary);
	if (!in1.is_open()) {
	    cerr << "ERROR: Could not open \"" << argv[0] << "\"." << endl;
	    exit(1);
	}

	StreamLen = process_data(in1, cout);
	in1.close();
    } else {
	// Use stdin

	StreamLen = process_data(cin, cout);
    }


    if (Verbose) {
	cerr << "Output " << dec << StreamLen << " symbols." << endl;
    }

    in1.close();

    return 0;
}

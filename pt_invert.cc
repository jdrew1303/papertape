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
 * \brief Main entry point of papertape data inversion executable.
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
    os << "  pt_invert [-v]"
       << endl;
    os << endl;
    os << "Description:" << endl;
    os << "  pt_invert reads data from stdin, performs a bitwise inversion," << endl;
    os << "  and outputs to stdout." << endl;
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
    data_t		data;			// data to be output
    unsigned char	c;			// input character
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

    //argc -= optind;
    //argv += optind;

    if (Verbose) {
	cerr << "Reading from stdin..." << endl;
    }

    // read data to be encoded from stdin, invert, and output to stdout.
    while (cin.good()) {
	c = (unsigned char)cin.get();
	if (!cin.good()) {
	    break;
	}

	++StreamLen;
	cout.put(~c);
    }

    if (Verbose) {
	cerr << "Output " << dec << StreamLen << " symbols." << endl;
    }


    return 0;


}

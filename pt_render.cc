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
 * \brief Main entry point of papertape renderer executable.
 *
 */ 


#include "papertape.h"

extern void pbmtape(ostream& os, tape_t tape, data_t& data);

//! Print version and usage instructions to stderr.
//
void PrintHelp(ostream& os) {
    os << endl;
    os << PACKAGE_STRING << " by Mark J. Blair, NF6X <nf6x@nf6x.net>" << endl;
    os << "Copyright (C) 2010 Mark J. Blair. Released under GPLv3" << endl;
    os << endl;
    os << "Usage:" << endl;
    os << "  pt_render [-v] [-5|-8] [-p] [-f {format}] [-l {len}] [-t {len}]"
       << endl;
    os << endl;
    os << "Description:" << endl;
    os << "  pt_render reads data from stdin and generates a graphical representation" << endl;
    os << "  of punched paper tape conforming to the ECMA-10 standard." << endl;
    os << "  This representation is output to stdout as either ASCII text or a PBM bitmap." << endl;
    os << "  In PBM format, each pixel represents 0.01 inches." << endl;
    os << endl;
    os << "Options:" << endl;
    os << "  -v: Verbose mode. Informational messages will be printed to stderr." << endl;
    os << "  -5: 5-bit tape width." << endl;
    os << "  -8: 8-bit tape width (default)." << endl;
    os << "  -f: Specify format:" << endl;
    os << "      ascii: text output (default)" << endl;
    os << "      pbm:   Portable Bitmap" << endl;
    os << "  -p: Include even parity in MSB." << endl;
    os << "  -l: Specify leader length (default 0)." << endl;
    os << "  -t: Specify trailer length (default 0)." << endl;
    os << endl;
}



//! Main entry point.
//
int main(int argc, char **argv)
{
    int			opt;		        // used for arg parsing
    format_t		format = FMT_ASCII; 	// output format
    tape_t		tape = TAPE_8; 		// tape width
    int			leader = 0;		// leader length
    int			trailer = 0;		// trailer length
    data_t		data;			// data to be output
    unsigned char	c;			// input character
    int			n, b;			// loop counters
    int			numbits=8;		// number of bits
    bool		parity=false;		// even parity?
    bool		Verbose = false;	// verbose mode


    // Disable getopt()'s internal error messages
    opterr = 0;

    // Parse command-line arguments
    while ((opt = getopt(argc, argv, ":58f:hl:pt:v")) != -1) {

	switch (opt) {

	  case '5':
	    tape    = TAPE_5;
	    numbits = 5;
	    break;

	  case '8':
	    tape    = TAPE_8;
	    numbits = 8;
	    break;

	  case 'f':
	    if (strcmp(optarg, "ascii")==0) {
		format = FMT_ASCII;
	    } else if (strcmp(optarg, "pbm")==0) {
		format = FMT_PBM;
	    } else {
		cerr << "ERROR: Invalid format specified." << endl << endl;
		PrintHelp(cerr);
		exit(1);
	    }
	    break;

	  case 'l':
	    leader = atoi(optarg);
	    break;

	  case 'p':
	    parity = true;
	    break;

	  case 't':
	    trailer = atoi(optarg);
	    break;

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


    // add leader
    for (n=0; n<leader; n++) {
	data.push_back(0);
    }

    if (Verbose) {
	cerr << "Reading from stdin..." << endl;
    }

    // read data to be encoded from stdin
    while (cin.good()) {
	c = (unsigned char)cin.get();
	if (!cin.good()) {
	    break;
	}

	if (parity) {
	    // even parity in MSB
	    for (n=0, b=0; n<(numbits-1); n++) {
		b += ((c>>n) & 1);
	    }
	    
	    if (b&1) {
		// odd data bits, so set MSB
		c |= (1 << (numbits-1));
	    } else {
		// even data bits, so clear MSB
		c &= ~(1 << (numbits-1));
	    }
	}

	data.push_back(c);
    }

    // add trailer
    for (n=0; n<trailer; n++) {
	data.push_back(0);
    }


    // output the data
    switch (format) {

      case FMT_ASCII:

	// print leading edge
	cout << '+';
	for (b=0; b < (numbits+1); b++) {
	    cout << '-';
	}
	cout << '+' << endl;

	// print data
	for (n=0; n < (int)data.size(); n++) {
	    c = data[n];
	    cout << '|';

	    for (b=0; b < numbits; b++) {
		if (c & 1) {
		    cout << 'o';
		} else {
		    cout << ' ';
		}
		if (b == 2) {
		    cout << '.';
		}
		c = c >> 1;
	    }
	    cout << '|' << endl;
	}

	// print trailing edge
	cout << '+';
	for (b=0; b < (numbits+1); b++) {
	    cout << '-';
	}
	cout << '+' << endl;

	break;

      case FMT_PBM:
	pbmtape(cout, tape, data);
	break;

      default:
	exit(1);
	break;
    }

    if (Verbose) {
	cerr << "Output " << dec << data.size() << " symbols." << endl;
    }


    return 0;
}

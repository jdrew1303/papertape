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
 * \brief Generate PBM image of punched paper tape conforming to ECMA-10 specification.
 *
 */ 


#include "papertape.h"

// Each pixel = 0.01"

#define BIT_WIDTH	100
#define BITHOLE_DIAM	72
#define SPROCKET_DIAM	46
#define LEFTEDGE	42
#define RIGHTEDGE5	45
#define RIGHTEDGE7	58


void pbmtape(ostream& os, tape_t tape, data_t& data) {
    int			tapewidth;		// width in pixels
    int			tapelength;		// length in pixels
    vector <bool>	strip;			// strip of pixels
    unsigned char	c;
    int			n, b;
    int			x, y;
    int			offset;
    double		x1, y1, r;
    int			numbits;

    tapelength = data.size() * BIT_WIDTH;

    switch (tape) {
      case TAPE_5:
	tapewidth = LEFTEDGE + (BIT_WIDTH * 6) + RIGHTEDGE5;
	numbits = 5;
	break;

      case TAPE_8:
	tapewidth = LEFTEDGE + (BIT_WIDTH * 9) + RIGHTEDGE7;
	numbits = 8;
	break;

      default:
	exit(1);
	break;
    }

    strip.resize(tapewidth);

    os << "P4" << endl;
    os << dec << tapewidth << ' ' << tapelength << endl;

    for (n=0; n < (int)data.size(); n++) {
	for (y=0; y<BIT_WIDTH; y++) {
	    for (x=0; x < tapewidth; strip[x++] = false);

	    c = data[n];

	    for (b=0; b<3; b++) {
		if (c & 1) {
		    offset = (b * BIT_WIDTH) + LEFTEDGE;

		    for (x=0; x<BIT_WIDTH; x++) {
			x1 = x - (BIT_WIDTH/2);
			y1 = y - (BIT_WIDTH/2);

			r = sqrt((x1*x1) + (y1*y1));
			if (r <= BITHOLE_DIAM/2) {
			    strip[x+offset] = true;
			}
		    }
		}
		c = c >> 1;
	    }

	    offset = (b * BIT_WIDTH) + LEFTEDGE;
	    
	    for (x=0; x<BIT_WIDTH; x++) {
		x1 = x - (BIT_WIDTH/2);
		y1 = y - (BIT_WIDTH/2);
		
		r = sqrt((x1*x1) + (y1*y1));
		if (r <= SPROCKET_DIAM/2) {
		    strip[x+offset] = true;
		}
	    }

	    for ( ; b<numbits; b++) {
		if (c & 1) {
		    offset = ((b+1) * BIT_WIDTH) + LEFTEDGE;

		    for (x=0; x<BIT_WIDTH; x++) {
			x1 = x - (BIT_WIDTH/2);
			y1 = y - (BIT_WIDTH/2);

			r = sqrt((x1*x1) + (y1*y1));
			if (r <= BITHOLE_DIAM/2) {
			    strip[x+offset] = true;
			}
		    }
		}
		c = c >> 1;
	    }

	    for (x=0; x<tapewidth; x+=8) {
		for (c=0, b=0; b<8; b++) {
		    c = c << 1;
		    if (((x+b) < tapewidth) && strip[x+b]) {
			c |= 1;
		    }
		}
		os.put(c);
	    }

	}
    }

}



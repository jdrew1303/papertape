#!/usr/bin/env python
#
##########################################################################
# Copyright (C) 2014 Mark J. Blair, NF6X
#
# This file is part of papertape.
#
#  papertape is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  papertape is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with papertape.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

'''Generate PBM image of punched paper tape conforming to ECMA-10 specification.'''

import math

# Each pixel = 0.01"
BIT_WIDTH  = 100
BIT_DIAM   = 72
FEED_DIAM  = 46
LEFTEDGE   = 42
RIGHTEDGE5 = 45
RIGHTEDGE7 = 58

def pbmtape(tape, filename, width=8, invert=False):
    '''Generate PBM image of punched paper tape conforming to ECMA-10 specification.'''

    assert(width in [5,8])
    outfile = open(filename, 'wb')

    # Compute image size in pixels
    imglength = len(tape) * BIT_WIDTH
    if width == 5:
        imgwidth = LEFTEDGE + (BIT_WIDTH * 6) + RIGHTEDGE5
    else:
        imgwidth = LEFTEDGE + (BIT_WIDTH * 9) + RIGHTEDGE7

    # Image header
    outfile.write('P4\n')
    outfile.write('{:d} {:d}\n'.format(imgwidth, imglength))

    # Render image
    for char in tape:

        # Render each row of pixels for this bit
        for y in range(BIT_WIDTH):
            row = [0]*imgwidth
            c = char

            # Render first three bits
            for b in range(3):
                if c & 0x01:
                    offset = (b * BIT_WIDTH) + LEFTEDGE
                    for x in range(BIT_WIDTH):
                        x1 = x - (BIT_WIDTH/2)
                        y1 = y - (BIT_WIDTH/2)
                        r = math.sqrt((x1*x1) + (y1*y1))
                        if r <= (BIT_DIAM/2):
                            row[x+offset] = 1
                c = c >> 1

            # Render feed hole
            offset = (3 * BIT_WIDTH) + LEFTEDGE;
            for x in range(BIT_WIDTH):
                x1 = x - (BIT_WIDTH/2)
                y1 = y - (BIT_WIDTH/2)
                r = math.sqrt((x1*x1) + (y1*y1))
                if r <= (FEED_DIAM/2):
                    row[x+offset] = 1

            # Render remaining bits
            for b in range(3,width):
                if c & 0x01:
                    offset = ((b+1) * BIT_WIDTH) + LEFTEDGE
                    for x in range(BIT_WIDTH):
                        x1 = x - (BIT_WIDTH/2)
                        y1 = y - (BIT_WIDTH/2)
                        r = math.sqrt((x1*x1) + (y1*y1))
                        if r <= (BIT_DIAM/2):
                            row[x+offset] = 1
                c = c >> 1

            # Output the data for this row of pixels
            if invert:
                for x in range(imgwidth-1, 0, -8):
                    c = 0
                    for b in range(8):
                        c = c << 1
                        if ((x-b) >= 0) and row[x-b]:
                            c = c | 0x01
                    outfile.write(chr(c))
            else:
                for x in range(0, imgwidth, 8):
                    c = 0
                    for b in range(8):
                        c = c << 1
                        if ((x+b) < imgwidth) and row[x+b]:
                            c = c | 0x01
                    outfile.write(chr(c))

    outfile.close()    

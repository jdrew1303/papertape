#!/usr/bin/env python
#
##########################################################################
# Copyright (C) 2014 Mark J. Blair, NF6X
#
# This file is part of papertape
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
#  along with py  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

'''Read in tape from GNT4604 reader/punch at 4800 baud.'''

import serial
import sys
import signal

def handler(signum, frame):
    print ''
    print 'Done!'
    sys.exit(0)

if len(sys.argv) != 3:
    sys.stderr.write('Usage: pt_tapein <port> <outfile>\n')
    sys.exit(1)

reader = serial.Serial(port=sys.argv[1], baudrate=4800, bytesize=serial.EIGHTBITS,
                       parity=serial.PARITY_NONE, timeout=None, xonxoff=False,
                       rtscts=True, dsrdtr=False)

outfile = open(sys.argv[2], 'wb')


print 'Reading from:', sys.argv[1]
print 'Writing to:  ', sys.argv[2]
print '^C to exit...'

signal.signal(signal.SIGINT, handler)

count = 0

while True:
    c = reader.read(1)
    outfile.write(c)
    outfile.flush()
    sys.stdout.write('{:02X} '.format(ord(c)))
    if (count % 16) == 15:
        sys.stdout.write('\n')
    count = count + 1
    sys.stdout.flush()



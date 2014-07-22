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

'''Send tape to reader/punch over serial interface.'''

import sys
import signal
import serial
import argparse
import textwrap
import papertape


# Main entry point when called as an executable script.
if __name__ == '__main__':

    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(
        prog='tapeout.py',
        description=textwrap.dedent('''\
        Punched paper tape writer utility version {:s}
          {:s}
          {:s}
          {:s}\
        '''.format(papertape.__version__, papertape.__copyright__,
                       papertape.__pkg_url__, papertape.__dl_url__)),
        add_help=True,
        formatter_class=argparse.RawDescriptionHelpFormatter)


    parser.add_argument('--baud', action='store', nargs=1,
                        metavar='BAUD', default=[4800], type=int,
                        help='''Specify baud rate for tape punch output.
                        Defaults to 4800.''')

    parser.add_argument('port', action='store', nargs=1,
                        metavar='PORT',
                        help='Serial port for tape punch output.')

    parser.add_argument('file', action='store', nargs=1,
                        metavar='FILENAME',
                        help='Input file name.')

    # Parse the command-line arguments.
    args = parser.parse_args()


    # Open the tape punch serial port.
    try:
        punch = serial.Serial(port=args.port[0], baudrate=args.baud[0],
                               bytesize=serial.EIGHTBITS,
                               parity=serial.PARITY_NONE, timeout=None, xonxoff=False,
                               rtscts=True, dsrdtr=True)
    except:
        print punch
        sys.stderr.write('Error opening port.')

    infile = open(args.file[0], 'rb')

    count = 0

    for c in infile.read():
        punch.write(c)
        sys.stdout.write('{:02X} '.format(ord(c)))
        if (count % 16) == 15:
            sys.stdout.write('\n')
        count = count + 1
        sys.stdout.flush()

    sys.stdout.write('\n')

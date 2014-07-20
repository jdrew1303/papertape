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

'''Read in tape from reader/punch over serial interface.'''

import sys
import signal
import serial
import argparse
import textwrap
import papertape


def ctrlc_handler(signum, frame):
    '''Handler to be called when user presses ^C.'''
    print ''
    print 'Done!'
    sys.exit(0)


# Main entry point when called as an executable script.
if __name__ == '__main__':

    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(
        prog='tapein.py',
        description=textwrap.dedent('''\
        Punched paper tape reader utility version {:s}
          {:s}
          {:s}
          {:s}\
        '''.format(papertape.__version__, papertape.__copyright__,
                       papertape.__pkg_url__, papertape.__dl_url__)),
        add_help=True,
        formatter_class=argparse.RawDescriptionHelpFormatter)


    parser.add_argument('--baud', action='store', nargs=1,
                        metavar='BAUD', default=[4800], type=int,
                        help='''Specify baud rate for tape reader input.
                        Defaults to 4800.''')

    parser.add_argument('port', action='store', nargs=1,
                        metavar='PORT',
                        help='Serial port for tape reader input.')

    parser.add_argument('file', action='store', nargs=1,
                        metavar='FILENAME',
                        help='Output file name.')

    # Parse the command-line arguments.
    args = parser.parse_args()


    # Open the tape reader serial port.
    try:
        reader = serial.Serial(port=args.port[0], baudrate=args.baud[0],
                               bytesize=serial.EIGHTBITS,
                               parity=serial.PARITY_NONE, timeout=None, xonxoff=False,
                               rtscts=True, dsrdtr=False)
    except:
        print reader
        sys.stderr.write('Error opening port.')

    outfile = open(args.file[0], 'wb')


    print 'Start reader; press ^C to end capture.'

    signal.signal(signal.SIGINT, ctrlc_handler)

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

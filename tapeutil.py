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

'''Utility for manipulating images of punched paper tapes.'''

import sys
import argparse
import textwrap
import papertape


# Accumulate arguments in order encountered
class gather_args(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if not 'arg_sequence' in namespace:
            setattr(namespace, 'arg_sequence', [])
        prev = namespace.arg_sequence
        prev.append((self.dest, values))
        setattr(namespace, 'arg_sequence', prev)


# Main entry point when called as an executable script.
if __name__ == '__main__':

    # This is the in-memory buffer of the tape image
    tapebuf = papertape.tape()

    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(
        prog='tapeutil.py',
        description=textwrap.dedent('''\
        Punched paper tape image utility version {:s}
          {:s}
          {:s}
          {:s}

        Arguments are processed in the order encountered, with cumulative effects
        upon the tape image buffer. The tape image buffer is discarded at program
        exit, so the final argument should generally be one which outputs the
        buffer to a file, the screen, or a tape punch. Arguments may be abbreviated.\
        '''.format(papertape.__version__, papertape.__copyright__,
                       papertape.__pkg_url__, papertape.__dl_url__)),
        epilog=textwrap.dedent('''\
        Example:
          tapeutil.py --load myfile.txt --pad_crlf --set_msb \\
                      --add_leader 2 --title "MY TAPE" \\
                      --add_leader 5 --add_trailer 5 --save myfile.tap'''),
        add_help=True,
        formatter_class=argparse.RawDescriptionHelpFormatter)


    parser.add_argument('--clear', action=gather_args, nargs=0,
                        help='Clear the tape image buffer.')

    parser.add_argument('--load', action=gather_args, nargs=1,
                        metavar='FILENAME',
                        help='''Load tape image buffer from file, replacing previous
                        buffer contents.''')

    parser.add_argument('--append', action=gather_args, nargs=1,
                        metavar='FILENAME',
                        help='''Load tape image buffer from file, appending to previous
                        buffer contents.''')

    parser.add_argument('--save', action=gather_args, nargs=1,
                        metavar='FILENAME',
                        help='Save tape image buffer to file.')

    parser.add_argument('--hexdump', action=gather_args, nargs=0,
                        help='''Print a hex dump to stdout. Most significant bit
                        (bit number ) will be ignored for the ASCII representation.''')

    parser.add_argument('--trim', action=gather_args, nargs=0,
                        help='Trim leader and trailer of NUL chars from buffer.')

    parser.add_argument('--add_leader', action=gather_args, nargs=1,
                        metavar='INCHES', type=float,
                        help='Add NUL leader to buffer.')

    parser.add_argument('--add_trailer', action=gather_args, nargs=1,
                        metavar='INCHES', type=float,
                        help='Add NUL trailer to buffer.')

    parser.add_argument('--strip_nul', action=gather_args, nargs=0,
                        help='Remove all NUL chars from buffer.')

    parser.add_argument('--strip_del', action=gather_args, nargs=0,
                        help='Remove all DEL chars from buffer.')

    parser.add_argument('--set_msb', action=gather_args, nargs=0,
                        help='''Set most significant bit (bit number 7) of all
                        chars in buffer.''')

    parser.add_argument('--clear_msb', action=gather_args, nargs=0,
                        help='''Clear most significant bit (bit number 7) of all
                        chars in buffer.''')

    parser.add_argument('--pad_crlf', action=gather_args, nargs=0,
                        help='Add two DEL chars after each CR-LF sequence in buffer.')

    parser.add_argument('--title', action=gather_args, nargs=1,
                        metavar='TITLE',
                        help='''Add human-readable title to beginning of buffer,
                        using a font composed of 5x7 punched hole patterns. Title
                        will be right side up for tapes following ECMA-10 standard,
                        but inverted on machines like the Teletype 33 ASR.''')

    parser.add_argument('--inv_title', action=gather_args, nargs=1,
                        metavar='TITLE',
                        help='''Add human-readable title to beginning of buffer,
                        using a font composed of 5x7 punched hole patterns. Title
                        will be right side up on machines like the Teletype 33 ASR,
                        but inverted on tapes following ECMA-10 standard.''')

    parser.add_argument('--rot_title', action=gather_args, nargs=1,
                        metavar='TITLE',
                        help='''Add human-readable title to beginning of buffer,
                        using a font composed of 5x7 punched hole patterns. Rotate the
                        letters to fit on a 5-bit tape. Title
                        will be right side up for tapes following ECMA-10 standard,
                        but inverted on machines like the Teletype 33 ASR.''')

    parser.add_argument('--rot_inv_title', action=gather_args, nargs=1,
                        metavar='TITLE',
                        help='''Add human-readable title to beginning of buffer,
                        using a font composed of 5x7 punched hole patterns. Rotate the
                        letters to fit on a 5-bit tape. Title
                        will be right side up on machines like the Teletype 33 ASR,
                        but inverted on tapes following ECMA-10 standard.''')

    parser.add_argument('--mask5', action=gather_args, nargs=0,
                        help='''Mask lower 5 bits of entire buffer in order to clear MSBs
                        of a 5-level tape read on an 8 bit reader.''')

    parser.add_argument('--ascii2tty', action=gather_args, nargs=0,
                        help='Translate entire buffer from ASCII to 5-level TTY coding.')

    parser.add_argument('--tty2ascii', action=gather_args, nargs=0,
                        help='Translate entire buffer from 5-level TTY to ASCII coding.')

    parser.add_argument('--render_ascii', action=gather_args, nargs=1,
                        metavar='WIDTH', type=int,
                        choices=[5,8],
                        help='''Create an ASCII art rendering of a punched tape,
                        in a style similar to the bcd(1) program. WIDTH specifies the
                        tape width in bits, and must be 5 or 8. Rendering will be printed
                        to stdout. Leading edge of tape will be at top.
                        Tape will be top side up on ECMA-10 compliant machines,
                        or top side down on machines like the Teletype 33 ASR.''')

    parser.add_argument('--inv_render_ascii', action=gather_args, nargs=1,
                        metavar='WIDTH', type=int,
                        choices=[5,8],
                        help='''Create an ASCII art rendering of a punched tape,
                        in a style similar to the bcd(1) program. WIDTH specifies the
                        tape width in bits, and must be 5 or 8. Rendering will be printed
                        to stdout. Leading edge of tape will be at top.
                        Tape will be top side up on machines like the Teletype 33 ASR,
                        or top side down on ECMA-10 compliant machines.''')

    parser.add_argument('--render_pbm', action=gather_args, nargs=2,
                        metavar=('WIDTH', 'FILENAME'),
                        help='''Create a rendering of a punched tape in Portable
                        Bitmap (.pbm) format, with each pixel representing 0.01
                        inches. WIDTH specifies the tape width in bits, and must
                        be 5 or 8. Leading edge of tape will be at top.
                        Tape will be top side up on ECMA-10 compliant machines,
                        or top side down on machines like the Teletype 33 ASR.''')

    parser.add_argument('--inv_render_pbm', action=gather_args, nargs=2,
                        metavar=('WIDTH', 'FILENAME'),
                        help='''Create a rendering of a punched tape in Portable
                        Bitmap (.pbm) format, with each pixel representing 0.01
                        inches. WIDTH specifies the tape width in bits, and must
                        be 5 or 8. Leading edge of tape will be at top.
                        Tape will be top side up on machines like the Teletype 33 ASR,
                        or top side down on ECMA-10 compliant machines.''')


    # Parse the command-line arguments. Need to create empty arg_sequence
    # in case no command-line arguments were included.
    args = parser.parse_args()
    if not 'arg_sequence' in args:
        setattr(args, 'arg_sequence', [])


    # Execute each command-line argument in the order encountered.
    for arg in args.arg_sequence:
        cmd = arg[0]
        opt = arg[1]

        if cmd == 'clear':
            tapebuf.clear()

        elif cmd == 'load':
            tapebuf.load(opt[0], append=False)

        elif cmd == 'append':
            tapebuf.load(opt[0], append=True)

        elif cmd == 'save':
            tapebuf.save(opt[0])

        elif cmd == 'hexdump':
            print tapebuf.hexdump()

        elif cmd == 'trim':
            tapebuf.trim()

        elif cmd == 'add_leader':
            tapebuf.add_leader(length = int(opt[0] * 10))

        elif cmd == 'add_trailer':
            tapebuf.add_trailer(length = int(opt[0] * 10))

        elif cmd == 'strip_nul':
            tapebuf.strip_nul()

        elif cmd == 'strip_del':
            tapebuf.strip_del()

        elif cmd == 'set_msb':
            tapebuf.set_msb()

        elif cmd == 'clear_msb':
            tapebuf.clear_msb()

        elif cmd == 'pad_crlf':
            tapebuf.pad_crlf()

        elif cmd == 'title':
            tapebuf.add_title(title=opt[0], rotate=False, invert=False)

        elif cmd == 'inv_title':
            tapebuf.add_title(title=opt[0], rotate=False, invert=True)

        elif cmd == 'rot_title':
            tapebuf.add_title(title=opt[0], rotate=True, invert=False)

        elif cmd == 'rot_inv_title':
            tapebuf.add_title(title=opt[0], rotate=True, invert=True)

        elif cmd == 'mask5':
            tapebuf.and_buf(0x1F)

        elif cmd == 'ascii2tty':
            tapebuf.ascii2tty()

        elif cmd == 'tty2ascii':
            tapebuf.tty2ascii()

        elif cmd == 'render_ascii':
            print tapebuf.render_ascii(width=opt[0], invert=False)
            
        elif cmd == 'inv_render_ascii':
            print tapebuf.render_ascii(width=opt[0], invert=True)
            
        elif cmd == 'render_pbm':
            if int(opt[0]) not in [5,8]:
                sys.stderr.write('ERROR: --render_pbm width must be 5 or 8.\n')
                exit(1)
            tapebuf.render_pbm(filename=opt[1], width=int(opt[0]), invert=False)
            
        elif cmd == 'inv_render_pbm':
            if int(opt[0]) not in [5,8]:
                sys.stderr.write('ERROR: --render_pbm width must be 5 or 8.\n')
                exit(1)
            tapebuf.render_pbm(filename=opt[1], width=int(opt[0]), invert=True)
            
        else:
            sys.stderr.write('Internal parser error: Unexpected argument "{:s}".'.format(cmd))
            exit(1)
            

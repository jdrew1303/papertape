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
#  along with papertape.  If not, see <http:#www.gnu.org/licenses/>.
##########################################################################

'''ASCII/TTY coding conversion data.'''

# Constants for asc2tty array
INVC	= 0377		# invalid character mapping
FIGS_F 	= 0200		# figures required flag
ETHR_F	= 0100		# valid in either shift
LTRS	= 0037		# letters shift character
FIGS	= 0033		# figures shift character
MSK5	= 0037		# mask off 5 LSBs
MSK7	= 0177		# mask off 7 LSBs


# Array for converting ASCII to 5-level TTY code.
#
# 5 LSBs are significant.
# Bit 7 set if figures shift required.
# 0xff indicates invalid character mapping.
# Lower-case mapped to upper-case
# See also:
# http://homepages.cwi.nl/~dik/english/codes/5tape.html#teletype
# ascii(7)
#
asc2tty = [
    0100, INVC, INVC, INVC, INVC, INVC, INVC, 0233, # NUL, ..., BEL
    INVC, INVC, 0110, INVC, INVC, 0102, INVC, INVC, # ..., LF, ..., CR
    INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, # ...
    INVC, INVC, INVC, INVC, INVC, INVC, INVC, INVC, # ...

    0104, 0226, 0221, 0205, 0222, INVC, 0213, 0224, # SP, punct.
    0236, 0211, INVC, INVC, 0206, 0230, 0207, 0227, # punct.
    0215, 0235, 0231, 0220, 0212, 0201, 0225, 0234, # 0-7
    0214, 0203, 0216, 0217, INVC, INVC, INVC, 0223, # 8-9, punct

    INVC, 0030, 0023, 0016, 0022, 0020, 0026, 0013, # @, A-G
    0005, 0014, 0032, 0036, 0011, 0007, 0006, 0003, # H-O
    0015, 0035, 0012, 0024, 0001, 0034, 0017, 0031, # P-W
    0027, 0025, 0021, INVC, INVC, INVC, INVC, INVC, # X-Z, punct

    INVC, 0030, 0023, 0016, 0022, 0020, 0026, 0013, # ', a-g
    0005, 0014, 0032, 0036, 0011, 0007, 0006, 0003, # h-o
    0015, 0035, 0012, 0024, 0001, 0034, 0017, 0031, # p-w
    0027, 0025, 0021, INVC, INVC, INVC, INVC, INVC  # x-z, punct, DEL
]


# Arrays for converting 5-level TTY code to ASCII.

tty_ltrs2asc = [
    '\x00', 'T', '\x0D', 'O',  ' ', 'H', 'N', 'M',
    '\x0A', 'L', 'R',    'G',  'I', 'P', 'C', 'V',
    'E',    'Z', 'D',    'B',  'S', 'Y', 'F', 'X',
    'A',    'W', 'J',    FIGS, 'U', 'Q', 'K', LTRS]

tty_figs2asc = [
    '\x00', '5', '\x0D', '9',  ' ', '#', ',', '.',
    '\x0A', ')', '4',    '&',  '8', '0', ':', ';',
    '3',    '"', '$',    '?',  "'", '6', '!', '/',
    '-',    '2', '\x07', FIGS, '7', '1', '(', LTRS]


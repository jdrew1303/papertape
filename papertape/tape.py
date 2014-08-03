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

'''This class provides support for manipulating images of punched paper tapes.'''

import string
__printable__ = string.ascii_letters + string.digits + string.punctuation

import font5x7
import pbmtape
import tty


class tape(bytearray):
    '''Class representing the contents of a punched paper tape.'''

    def clear(self):
        '''Discard buffer contents.'''

        del self[0:len(self)]


    def load(self, filename, append=False):
        '''Load buffer from a disk file.

        Previous buffer contents will be discarded unless append is True.'''

        if not append:
            self.clear()
        f = open(filename, 'rb')
        self.extend(f.read())
        f.close()


    def save(self, filename):
        '''Save buffer to a disk file.

        Will overwrite existing file with same name.'''

        f = open(filename, 'wb')
        f.write(self)
        f.close()


    def hexdump(self):
        '''Return string containing hex dump of buffer.

        MSBs are ignored in the ASCII representation.'''

        dump = ''
        for n in range(len(self)):
            if (n % 16) == 0:
                offset = '{:04X}:'.format(n)
                hexfld = ''
                ascfld = ''
            hexfld = hexfld + ' {:02X}'.format(self[n])
            if (n % 4) == 3:
                hexfld = hexfld + ' '
            b = chr(self[n] & 0x7F)
            if b in __printable__:
                ascfld = ascfld + b
            else:
                ascfld = ascfld + ' '
            if (n % 4) == 3:
                ascfld = ascfld + ' '
            if ((n % 16) == 15) or (n == len(self)-1):
                dump = dump + '{:5s} {:52s} {:20s}\n'.format(offset,hexfld,ascfld)
        return dump

                
    def trim(self, char=0x00):
        '''Remove leader and trailer from beginning and end of buffer.

        By default, expect leader and trailer to consist of NUL bytes.
        Set char to ASCII value to be removed otherwise.'''

        while self[0] == char:
            del self[0]
        while self[-1] == char:
            del self[-1]


    def strip_char(self, char):
        '''Remove each instance of the specified character from the buffer.'''

        while True:
            try:
                self.remove(char)
            except ValueError:
                break


    def strip_nul(self):
        '''Remove all NUL characters from the buffer.'''

        self.strip_char(0x00)
                

    def strip_del(self):
        '''Remove all DEL characters from the buffer.'''

        self.strip_char(0x7F)
                

    def xor_buf(self, mask):
        '''Replace each byte of buffer with bitwise XOR of mask with previous value.'''

        for n in range(len(self)):
            self[n] = self[n] ^ (mask & 0xFF)


    def inv_buf(self):
        '''Invert all bits of each byte of buffer.'''

        self.xor_buf(0xFF)


    def and_buf(self, mask):
        '''Replace each byte of buffer with bitwise AND of mask with previous value.'''

        for n in range(len(self)):
            self[n] = self[n] & mask


    def or_buf(self, mask):
        '''Replace each byte of buffer with bitwise OR of mask with previous value.'''

        for n in range(len(self)):
            self[n] = self[n] | (mask & 0xFF)


    def set_msb(self):
        '''Set the most significant bit of each byte in the buffer.'''

        self.or_buf(0x80)


    def clear_msb(self):
        '''Clear the most significant bit of each byte in the buffer.'''

        self.and_buf(0x7f)


    def add_leader(self, length=10, char=0x00):
        '''Add a leader to the beginning of the buffer.

        By default, length is 10 characters (typically one inch).
        By default, leader consists of NUL bytes.
        Set char to ASCII value to be added otherwise.'''

        for n in range(length):
            self.insert(0, char)


    def add_trailer(self, length=10, char=0x00):
        '''Add a trailer to the end of the buffer.

        By default, length is 10 characters (typically one inch).
        By default, trailer consists of NUL bytes.
        Set char to ASCII value to be added otherwise.'''

        self.extend(chr(char)*length)


    def pad_crlf(self):
        '''Add two DEL chars after each CR-LF sequence.'''

        if len(self) > 1:
            buf = bytearray()
            buf.append(self[0])
            for n in range(1, len(self)):
                buf.append(self[n])
                if (self[n] == 0x0A) and (self[n-1] == 0x0D):
                    buf.append(0x7F)
                    buf.append(0x7F)
            self.clear()
            self.extend(buf)


    def add_title(self, title, rotate=False, invert=False):
        '''Add a human-readable title to the beginning of the buffer.'''
        
        # Build the title pattern
        buf = bytearray('\x00')
        for char in title:
            letter = font5x7.font5x7[int(ord(char) & 0x7F)]
            if rotate:
                letter = font5x7.rotate_char(letter)
                if invert:
                    letter = font5x7.invert_char(letter, 5)
            else:
                if invert:
                    letter = font5x7.invert_char(letter, 7)
            for column in letter:
                buf.append(column)
            buf.append(0x00)

        # Prepend the title to the tape
        for column in reversed(buf):
            self.insert(0, column)


    def reverse_bits(self, numbits=8):
        '''Reverse the order of numbits least significant bits of
        each byte in the buffer, discarding more significant bits.'''

        for n in range(len(self)):
            self[n] = sum(1<<(numbits-1-i) for i in range(numbits) if self[n]>>i&1)


    def ascii2tty(self):
        '''Convert from ASCII to 5-level TTY code.

        Assumes reader may initially be in either letters or figures
        shift, and emits a shift char prior to first output char that
        is not valid in either shift.'''

        figs = None
        buf  = bytearray()

        # Emit initial shift if needed
        if len(self) > 0:
            char = tty.asc2tty[self[0] & tty.MSK7]
            if (char & tty.ETHR_F):
                # Valid in either shift
                pass
            elif (char & tty.FIGS_F):
                # Must be in figures shift
                buf.append(tty.FIGS)
                figs = True
            else:
                # Must be in letters shift
                buf.append(tty.LTRS)
                figs = False
        
        # Convert chars
        for char in self:
            # Drop MSB and convert
            char = tty.asc2tty[char & tty.MSK7]

            # Convert if valid
            if char != tty.INVC:

                # Emit shift char if needed
                if (char & tty.ETHR_F):
                    # Valid in either shift
                    pass
                elif (char & tty.FIGS_F):
                    # Must be in figures shift
                    if figs is not True:
                        # Not already in figures shift
                        # i.e. either in letters shift or indeterminate
                        buf.append(tty.FIGS)
                        figs = True
                elif figs is not False:
                    # In figures or indeterminate shift, but must be in letter shift
                    buf.append(tty.LTRS)
                    figs = False

                # Emit the converted char
                buf.append(char & tty.MSK5)

        # Replace buffer contents with converted data
        self.clear()
        self.extend(buf)


    def tty2ascii(self):
        '''Convert from 5-level TTY code to ASCII.

        Assumes initial letters shift state.'''

        figs = False
        buf  = bytearray()

        # Convert buffer contents
        for char in self:
            char = char & tty.MSK5
            if char == tty.LTRS:
                figs = False
            elif char == tty.FIGS:
                figs = True
            else:
                if figs:
                    char = tty.tty_figs2asc[char]
                else:
                    char = tty.tty_ltrs2asc[char]
                buf.append(char)

        # Replace buffer contents with converted data
        self.clear()
        self.extend(buf)



    def render_ascii(self, width=8, invert=False):
        '''Create ASCII art rendering of buffer, in style of bcd(1).'''

        # Leading edge
        buf = '+'
        for col in range(width + 1):
            buf = buf + '-'
        buf = buf + '+\n'

        # Render the rows
        for row in self:
            buf = buf + '|'
            if invert:
                for n in reversed(range(width)):
                    if row & (0x01 << (width-1)):
                        buf = buf + 'o'
                    else:
                        buf = buf + ' '
                    if n == 3:
                        buf = buf + '.'
                    row = row << 1
            else:
                for n in range(width):
                    if row & 0x01:
                        buf = buf + 'o'
                    else:
                        buf = buf + ' '
                    if n == 2:
                        buf = buf + '.'
                    row = row >> 1
            buf = buf + '|\n'

        # Trailing edge
        buf = buf + '+'
        for col in range(width + 1):
            buf = buf + '-'
        buf = buf + '+\n'

        return buf


    def render_pbm(self, filename, width=8, invert=False):
        '''Generate PBM image of punched paper tape.'''

        pbmtape.pbmtape(tape=self, filename=filename, width=width, invert=invert)


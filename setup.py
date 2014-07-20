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

'''Installation script for papertape.

papertape provides support for manipulating images of punched paper tapes.

Usage examples:

    Install in your user directory:
        ./setup.py install --user

    Install in the system default location:
        sudo ./setup.py install

    Install under /usr/local:
        sudo ./setup.py install --prefix /usr/local'''


from distutils.core import setup
from papertape import __version__, __pkg_url__, __dl_url__

setup(name          = 'papertape',
      version       = __version__,
      description   = 'Punched Paper Tape Manipulation Tools',
      author        = 'Mark J. Blair',
      author_email  = 'nf6x@nf6x.net',
      url           = __pkg_url__,
      download_url  = __dl_url__,
      license       = 'GPLv3',
      packages      = ['papertape'],
      scripts       = ['tapeutil.py', 'tapein.py'])


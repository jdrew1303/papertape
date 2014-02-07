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
 * \brief Misc. includes and definitions
 *
 */ 

#ifndef _PAPERTAPE_H_
#define _PAPERTAPE_H_

#include "config.h"

#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include <iostream>
#include <fstream>
#include <iomanip>
#include <vector>
#include <math.h>

using namespace std;


enum format_t {FMT_ASCII, FMT_PBM};
enum tape_t   {TAPE_5, TAPE_8};

typedef vector <unsigned char> data_t;

#endif // _PAPERTAPE_H_

#!/usr/bin/env python3.9
# -*- coding: utf-8 -*-
################################################################################
#    Wisteria Copyright (C) 2021 suizokukan
#    Contact: suizokukan _A.T._ orange dot fr
#
#    This file is part of Wisteria.
#    Wisteria is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Wisteria is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Wisteria.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
"""
    wisteria/globs.py

    Global variables.

    ___________________________________________________________________________

    o  VERBOSITY_MINIMAL
    o  VERBOSITY_NORMAL
    o  VERBOSITY_DETAILS
    o  VERBOSITY_DEBUG

    o  ARGS

    o  TIMEITNUMBER

    o  TMPFILENAME

    o  REGEX_CMP
    o  REGEX_CMP__HELP

    o  REPORT_MINIMAL_STRING
    o  REPORT_FULL_STRING
"""
import re


# values defined for --verbosity:
VERBOSITY_MINIMAL = 0
VERBOSITY_NORMAL = 1
VERBOSITY_DETAILS = 2
VERBOSITY_DEBUG = 3

# will be set to argparse.ArgumentParser(...).parse_args()
ARGS = None

# number of times
TIMEITNUMBER = 10

TMPFILENAME = "wisteria.tmp"

REGEX_CMP = re.compile(r"^\s*(?P<serializer1>[^\s\(\)]+)"
                       r"((\svs\s|\sversus\s|\sagainst\s)(?P<serializer2>[^\s\(\)]+))?"
                       r"(\s*\((?P<data>all|cwc|ini)\))?\s*$")
REGEX_CMP__HELP = "all|serializer1[vs all|serializer2][(all|cwc|ini)]"

REPORT_MINIMAL_STRING = "C;"
REPORT_FULL_STRING = "titles;A;B1a;B1b;B1c;B2a;B2b;C1a;C1b;C2a;C2b;"

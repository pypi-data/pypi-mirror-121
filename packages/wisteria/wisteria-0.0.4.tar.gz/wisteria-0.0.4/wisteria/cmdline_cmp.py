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
    cmdline_cmp.py

    Just the parsing of --cmp.

    ___________________________________________________________________________

    o  read_cmpstring(cmpstring)
"""
import re

from wisteria.msg import msgerror
from wisteria.globs import REGEX_CMP, REGEX_CMP__HELP
import wisteria.globs


def read_cmpstring(cmpstring):
    """
        read_cmpstring()

        Return a simpler representation of (str)<cmpstring>.

        Some valid examples, "..." being "(bool/success)True".
        --cmp="jsonpickle vs all (all)"
        --cmp="jsonpickle vs all"
        --cmp="jsonpickle"
          > ..., (serializer#1/str)"jsonpickle", (serializer#2/str)"all", (data/str)"all"

        --cmp="jsonpickle (ini)"
          > ..., (serializer#1/str)"jsonpickle", (serializer#2/str)"all", (data/str)"ini"

        --cmp="jsonpickle vs json"
          > ..., (serializer#1/str)"jsonpickle", (serializer#2/str)"json", (data/str)"all"

        "vs" may be used as well as "versus" or "against".

        _______________________________________________________________________

        ARGUMENT: (str)cmpstring, the source string to be read.
                syntax: "all|serializer1[vs all|serializer2][(all|cwc|ini)]"

        RETURNED VALUE: (bool)success,
                        (str)serializer1,
                        (str)serializer2,
                        (str:"all|cwc|ini")cmpdata
    """
    serializers = wisteria.globs.SERIALIZERS

    if res := re.match(REGEX_CMP, cmpstring):
        serializer1 = res.group("serializer1")
        if serializer1 is None or serializer1 == "others":
            serializer1 = "all"
        serializer2 = res.group("serializer2")
        if serializer2 is None or serializer2 == "others":
            serializer2 = "all"
        cmpdata = res.group("data")
        if cmpdata is None:
            cmpdata = "all"

        if not (serializer1 == "all" or serializer1 in serializers):
            msgerror(f"(ERRORID009) Unknown serializer #1 from cmp string '{cmpstring}': "
                     f"what is '{serializer1}' ? "
                     f"Known serializers #1 are 'all' and {tuple(serializers.keys())}.")
            return False, None, None, None
        if not (serializer2 == "all" or serializer2 == "others" or serializer2 in serializers):
            msgerror(f"(ERRORID010) Unknown serializer #2 from cmp string '{cmpstring}': "
                     f"what is '{serializer2}' ? "
                     "Known serializers #2 are 'all', 'others' and "
                     f"{tuple(serializers.keys())}.")
            return False, None, None, None
        if serializer1 == serializer2 and serializer1 != "all":
            msgerror(f"(ERRORID011) Both serializer-s from cmp string '{cmpstring}' "
                     f"(here, both set to '{serializer1}') "
                     "can't have the same value, 'all' and 'all' excepted.")
            return False, None, None, None

        return True, serializer1, serializer2, cmpdata

    msgerror(f"(ERRORID012) Ill-formed cmp string '{cmpstring}'. "
             f"Expected syntax is '{REGEX_CMP__HELP}'.")
    return False, None, None, None

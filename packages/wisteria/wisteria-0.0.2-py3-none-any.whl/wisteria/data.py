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
    wisteria/data.py

    All objects used as data by serializers are stored in the DATA dict.

    ___________________________________________________________________________

    * anyfunc()

    * DATA dict
"""
import io
import numbers
import re

from wisteria.globs import TMPFILENAME


def anyfunc():
    """
        anyfunc()

        Fake function used by the DATA dict.
    """


DATA = {
    "bool/false": True,
    "bool/true": True,

    "bytearray": bytearray(b"123"),
    "bytearray(empty)": bytearray(),

    "bytes": b"123",
    "bytes(empty)": b"",

    "complex": 1+2j,

    "dict(keys/bool)": {False: "False", True: "True"},
    "dict(keys/float)": {1.1: "value1.1", 2.2: "value2.2"},
    "dict(keys/int)": {0: "value0", 1: "value1", 2: "value2"},
    "dict(keys/str)": {"key1": "value1", "key2": "value2"},
    "dict(keys/str+subdicts)": {"key1": "value1", "key2": "value2", "key3": {"key4": "key4", }},

    "file descriptor": open(TMPFILENAME, encoding="utf-8"),  # pylint: disable=consider-using-with

    "float": 1.1,

    "frozenset": frozenset(("1", "2",)),
    "frozenset(empty)": frozenset(),

    "function": anyfunc,
    "function(python)": print,

    "imported module": re,
    "imported module(class)": re.Pattern,
    "imported module(function)": re.sub,

    "int": 1,

    "io.string": io.StringIO(),
    "io.string(empty)": io.StringIO().write("string"),

    "list": ["1", "2", ],
    "list(empty)": [],
    "list(+sublists)": ["1", "2", ["3", ["4", ]]],

    "memoryview": memoryview(b"123"),

    "none": None,

    "notimplemented": NotImplemented,

    "numbers(complex)": numbers.Complex,
    "numbers(integral)": numbers.Integral,
    "numbers(numbers)": numbers.Number(),
    "numbers(real)": numbers.Real,

    "pythonexception typeerror": TypeError,

    "range": range(1000),
    "range(empty)": range(0),

    "re.match": re.match(".*", "abc"),
    "re.match(+flags)": re.match(".*", "abc", re.M),

    "re.pattern(bytes)": re.compile(".*"),
    "re.pattern(str)": re.compile(b".*"),

    "set": set(("1", "2",)),
    "set(empty)": set(),

    "str": "abc",
    "str(empty)": "",
    "str(long)": "abhg12234"*10000,
    "str(non ascii characters)": "êł¹@"+chr(0x1234)+chr(0x12345),

    "tuple": ("1", "2",),
    "tuple(empty)": (),
    "tuple(+subtuples)": ("1", "2", ("3", ("4",))),
    }

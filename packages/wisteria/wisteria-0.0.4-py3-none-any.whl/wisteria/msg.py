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
    msg.py

TODO
    msgreport() is reserved to report messages.

Dans ce projet, choisir une fonction msgxxx() n'est pas une question de priorité :
c'est d'abord un problème d'apparence (voir les préfixes @, >, !); la priorité
est gérée à chaque appel de msgxxx() par un test du type
     if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
"""
from rich import print as rprint
from wisteria.reportaspect import aspect_title
import wisteria.globs


def _message(obj):
    """
        _message()

        Internal function: displays and/or writes <obj> in the log file.

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file
    """
    if wisteria.globs.OUTPUT[0]:
        rprint(obj)
    if wisteria.globs.OUTPUT[1]:
        wisteria.globs.FILECONSOLE.print(obj)


def msgcritical(obj=""):
    """
        msgcritical()

        Display and/or write <obj> in the log file; to be used like log.critical() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message("!!! "+str(obj))


def msgdebug(obj=""):
    """
        msgcritical()

        Display and/or write <obj> in the log file; to be used like log.debug() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message("@ "+str(obj))


def msgerror(obj=""):
    """
        msgerror()

        Display and/or write <obj> in the log file; to be used like log.error() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message(obj)


def msginfo(obj=""):
    """
        msginfo()

        Display and/or write <obj> in the log file; to be used like log.info() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message("> "+str(obj))


def msgreport(obj=""):
    """
        msgreport()

        Display and/or write <obj> in the log file; to be used like log.info() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message(obj)


def msgreporttitle(obj=""):
    """
        msgreporttitle()

        Display and/or write <obj> in the log file; to be used like log.info() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message(aspect_title(obj))


def warning(obj=""):
    """
        msgwarning()

        Display and/or write <obj> in the log file; to be used like log.warning() .

        _______________________________________________________________________

        ARGUMENT: <obj>, the object to be displayed/written in the log file.
    """
    _message("! "+str(obj))

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
    results.py
"""
from rich.console import Console
from rich.progress_bar import ProgressBar

import wisteria.data
import wisteria.globs
from wisteria.globs import VERBOSITY_DETAILS, VERBOSITY_DEBUG
from wisteria.globs import PROGRESSBAR_LENGTH
from wisteria.wisteriaerror import WisteriaError
from wisteria.msg import msgdebug, msginfo, msgerror
from wisteria.serializers_classes import SerializationResults


def get_serializers_selection(serializer1,
                              serializer2):
    """
        get_serializers_selection()

        Return a tuple of all serializers defined by (str)<serializer1>, (str)<serializer1>.

        _______________________________________________________________________

        ARGUMENTS:
        o    <serializer1> : value returned by read_cmpstring()
        o    <serializer2> : value returned by read_cmpstring()

        RETURNED VALUE: a tuple of str
    """
    res = set()

    if serializer1 == "all":
        for serializer in wisteria.globs.SERIALIZERS:
            res.add(serializer)
    else:
        res.add(serializer1)

    if serializer2 == "all":
        for serializer in wisteria.globs.SERIALIZERS:
            res.add(serializer)
    else:
        res.add(serializer2)

    return tuple(res)


def get_data_selection(data,
                       config):
    """
        get_data_selection()

        Return a tuple of the data objects names selected by the <config>.

        _______________________________________________________________________

        ARGUMENTS:
        o  data:   (str)"all" or "ini"
        o  config: (dict) dict returned by read_cfgfile()

        RETURNED VALUE: (tuple) a tuple of (str)data keys
    """
    res = []

    if data == "all":
        res = tuple(wisteria.globs.DATA.keys())
    elif data == "ini":
        if config["data selection"]["data selection"] == "all":
            res = tuple(config["objects"].keys())
        elif config["data selection"]["data selection"] == "only if yes":
            res = (data_name for data_name in config["data objects"]
                   if config["data objects"][data_name])
        elif config["data selection"]["data selection"].startswith("data set/"):
            res = tuple(config["data sets"][config["data selection"]["data selection"]])
        else:
            raise WisteriaError(
                "(ERRORID020) "
                "Can't understand a value given to \\[data selection]'data selection': "
                f"what is '{config['data selection']['data selection']}' ? "
                "Known values are 'all', 'ini' and 'data set/xxx' "
                "where xxx is a string.")
    else:
        raise WisteriaError(
            "(ERRORID021) Can't understand a value given to the 'data' part in --cmp: "
            f"what is '{data}' ? "
            "Known values are 'all' and 'ini'. ")

    return res


def compute_results(config,
                    serializer1,
                    serializer2,
                    cmpdata):
    """
        compute_results()

        Create a SerializationResults object and try to fill it with all
        required encodings/decodings defined by <serializer1>,
        <serializer2> and <cmpdata>.

        TODO : arguments

        RETURNED VALUE:    (SerializationResults, None) if no error occured
                        or (None, (int)exit_code) if an error occured
    """
    try:
        # serializers and data to be used through the tests:
        _serializers = get_serializers_selection(serializer1, serializer2)
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"serializers to be used are: {_serializers}")
        _dataobjs = get_data_selection(cmpdata, config)
        if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"data objs to be used are: {_dataobjs}")

        if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
            msginfo("Please wait until all required encodings/decodings have been computed.")

        results = SerializationResults()

        # (progress bar)
        # Please note that there can be NO progress bar if the debug mode is enabled:
        # the output can't display both correctly.
        if wisteria.globs.ARGS.verbosity != VERBOSITY_DEBUG:
            console = Console()
            progressbar = ProgressBar(width=PROGRESSBAR_LENGTH,
                                      total=len(_serializers)*len(_dataobjs))
            console.show_cursor(False)
            progressbar_index = 0

        for serializer in _serializers:
            results[serializer] = {}
            for data_name in _dataobjs:
                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"About to call function for serializer='{serializer}' "
                             f"and data name='{data_name}'")

                results[serializer][data_name] = wisteria.globs.SERIALIZERS[serializer].func(
                    action="serialize",
                    obj=wisteria.globs.DATA[data_name])

                # (progress bar)
                # Please note that there can be NO progress bar if the debug mode is enabled:
                # the output can't display both correctly.
                if wisteria.globs.ARGS.verbosity != VERBOSITY_DEBUG:
                    progressbar_index += 1
                    progressbar.update(progressbar_index)
                    console.print(progressbar)
                    console.file.write("\r")

                if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
                    msgdebug(f"result: {results[serializer][data_name]}")

        # (progress bar)
        # Please note that there can be NO progress bar if the debug mode is enabled:
        # the output can't display both correctly.
        if wisteria.globs.ARGS.verbosity != VERBOSITY_DEBUG:
            # the following lines make disappear the progresse bar.
            # the next rprint() will overwrite the spaces that are about
            # to be added:
            if PROGRESSBAR_LENGTH is None:
                console.file.write(" "*console.width)
            else:
                console.file.write(" "*PROGRESSBAR_LENGTH)
            console.file.write("\r")

            console.show_cursor(True)

        if not results.finish_initialization():
            msgerror("(ERRORID015) Incorrect data, the program has to stop.")

            # (pimydoc)exit codes
            # ⋅*  0: normal exit code
            # ⋅*  1: normal exit code after --checkup
            # ⋅*  2: normal exit code after --downloadconfigfile
            # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
            # ⋅* -2: error, ill-formed --cmp string
            # ⋅* -3: internal error, data can't be loaded
            # ⋅* -4: internal error, an error occured while computing the results
            # ⋅* -5: internal error, an error in main()
            # ⋅* -6: error, ill-formed --output string
            return None, -3
        if results.dataobjs_number == 0:
            msginfo("No data to handle, the program can stop.")

            # (pimydoc)exit codes
            # ⋅*  0: normal exit code
            # ⋅*  1: normal exit code after --checkup
            # ⋅*  2: normal exit code after --downloadconfigfile
            # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
            # ⋅* -2: error, ill-formed --cmp string
            # ⋅* -3: internal error, data can't be loaded
            # ⋅* -4: internal error, an error occured while computing the results
            # ⋅* -5: internal error, an error in main()
            # ⋅* -6: error, ill-formed --output string
            return None, 2

        return results, None

    except WisteriaError as exception:
        msgerror(f"An error occured: {exception}")

        # (pimydoc)exit codes
        # ⋅*  0: normal exit code
        # ⋅*  1: normal exit code after --checkup
        # ⋅*  2: normal exit code after --downloadconfigfile
        # ⋅* -1: error, given config file can't be read (missing or ill-formed file)
        # ⋅* -2: error, ill-formed --cmp string
        # ⋅* -3: internal error, data can't be loaded
        # ⋅* -4: internal error, an error occured while computing the results
        # ⋅* -5: internal error, an error in main()
        # ⋅* -6: error, ill-formed --output string
        return None, -4

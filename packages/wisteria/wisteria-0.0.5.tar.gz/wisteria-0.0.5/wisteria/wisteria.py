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
    wisteria.py

    (pimydoc)exit codes
    ⋅*  0: normal exit code
    ⋅*  1: normal exit code after --checkup
    ⋅*  2: normal exit code after --downloadconfigfile
    ⋅* -1: error, given config file can't be read (missing or ill-formed file)
    ⋅* -2: error, ill-formed --cmp string
    ⋅* -3: internal error, data can't be loaded
    ⋅* -4: internal error, an error occured while computing the results
    ⋅* -5: internal error, an error in main()
    ⋅* -6: error, ill-formed --output string

TODO : functions ?
"""
import argparse
import atexit
import datetime
import os
import os.path
import sys

import rich.console
from rich import print as rprint

import wisteria.globs
from wisteria.globs import REPORT_SHORTCUTS
from wisteria.globs import TMPFILENAME, REGEX_CMP__HELP
from wisteria.globs import VERBOSITY_MINIMAL, VERBOSITY_NORMAL, VERBOSITY_DETAILS, VERBOSITY_DEBUG
from wisteria.globs import DEFAULT_CONFIG_FILENAME
from wisteria.aboutproject import __projectname__, __version__
from wisteria.report import report
from wisteria.results import compute_results
from wisteria.utils import normpath
import wisteria.serializers
import wisteria.data
from wisteria.wisteriaerror import WisteriaError
from wisteria.msg import msginfo, msgerror, msgdebug, msgreport
from wisteria.cmdline_output import parse_output_argument
from wisteria.cmdline_cmp import read_cmpstring
from wisteria.cfgfile import read_cfgfile, downloadconfigfile


# =============================================================================
# (01) command line parsing
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) command line parsing
# ⋅- (02) --output string
# ⋅- (03) logfile opening
# ⋅- (04) project name & version
# ⋅- (05) ARGS.report interpretation
# ⋅- (06) exit handler
# ⋅- (07) serializers import
# ⋅- (08) checkup
# ⋅- (09) download default config file
# ⋅- (10) temp file opening
# ⋅- (11) known data init
# ⋅- (12) call to main()
# ⋅       - (12.1) main(): debug messages
# ⋅       - (12.2) main(): cmp string interpretation
# ⋅       - (12.3) main(): config file reading
# ⋅       - (12.4) main(): results computing
# ⋅       - (12.5) main(): report
PARSER = \
    argparse.ArgumentParser(description='Comparisons of different Python serializers. '
                            'Try $wisteria --checkup then $wisteria --cmp="pickle against marshal"',
                            epilog=f"{__projectname__}: {__version__}",
                            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
PARSER.add_argument(
    '--version', '-v',
    action='version',
    version=f"{__projectname__} {__version__}",
    help="Show the version and exit.")

PARSER.add_argument(
    '--cmp',
    action='store',
    default="all vs all",
    help=f"Comparisons details. Expected syntax: '{REGEX_CMP__HELP}'.")

PARSER.add_argument(
    '--cfgfile',
    action='store',
    default=DEFAULT_CONFIG_FILENAME,
    help="config file to be used.")

PARSER.add_argument(
    '--checkup',
    action='store_true',
    help="show installed serializers, try to read current config file and exit")

PARSER.add_argument(
    '--downloadconfigfile',
    action='store_true',
    help="download default config file and exit")

PARSER.add_argument(
    '--output',
    action='store',
    default='console;logfile/w=report.txt',
    help="'console' or 'logfile' or 'console;logfile'. "
    "Instead of 'logfile' you may specify 'logfile/a' (append mode) or 'logfile/w' (write mode). "
    "Instead of 'logfile' you may specify 'logfile=myfile.log'. "
    "Combinations like 'logfile/w=report.txt' are accepted. See by example the default value.")

PARSER.add_argument(
    '--report',
    action='store',
    default="minimal",
    help=f"Report format: "
    f"you may use one of the special keywords {tuple(REPORT_SHORTCUTS.keys())} "
    "or a list of section parts, e.g. 'A1;B1a;'. "
    "You may use shorter strings like 'B' (=B1+B2, i.e. B1a+B1b...+B2a+B2b...) "
    "or like 'B1' (=B1a+B1b+B1c). "
    "Accepted section parts are "
    f"{tuple(wisteria.report.STR2REPORTSECTION.keys())}. "
    "More informations in the documentation. "
    "Please notice that --verbosity has no effect upon --report.")

PARSER.add_argument(
    '--verbosity',
    type=int,
    default=VERBOSITY_NORMAL,
    choices=(VERBOSITY_MINIMAL,
             VERBOSITY_NORMAL,
             VERBOSITY_DETAILS,
             VERBOSITY_DEBUG),
    help="Verbosity level: 0(=minimal), 1(=normal), 2(=normal+details), 3(=debug). "
    "Please notice that --verbosity has no effect upon --report.")

wisteria.globs.ARGS = PARSER.parse_args()


# =============================================================================
# (02) --output string
# =============================================================================
wisteria.globs.OUTPUT = parse_output_argument(wisteria.globs.ARGS.output)
if not wisteria.globs.OUTPUT[0]:
    # no log available, hence the use of rprint():
    rprint("[bold red]Ill-formed --output string. The program has to stop.[/bold red]")
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
    sys.exit(-6)
wisteria.globs.OUTPUT = wisteria.globs.OUTPUT[1:]

# =============================================================================
# (03) logfile opening
# =============================================================================
# TODO refermer ce fichier (dans exit handler ?)
# TODO vérifier que le fichier est bien fermé à la fin du programme.
wisteria.globs.FILECONSOLE = rich.console.Console(file=open(wisteria.globs.OUTPUT[3],
                                                            wisteria.globs.OUTPUT[2],
                                                            encoding="utf-8"))

# =============================================================================
# (04) project name & version
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) command line parsing
# ⋅- (02) --output string
# ⋅- (03) logfile opening
# ⋅- (04) project name & version
# ⋅- (05) ARGS.report interpretation
# ⋅- (06) exit handler
# ⋅- (07) serializers import
# ⋅- (08) checkup
# ⋅- (09) download default config file
# ⋅- (10) temp file opening
# ⋅- (11) known data init
# ⋅- (12) call to main()
# ⋅       - (12.1) main(): debug messages
# ⋅       - (12.2) main(): cmp string interpretation
# ⋅       - (12.3) main(): config file reading
# ⋅       - (12.4) main(): results computing
# ⋅       - (12.5) main(): report
if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
    msginfo(f"{__projectname__}, {__version__} ({str(datetime.datetime.now())})")


# =============================================================================
# (05) ARGS.report interpretation
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) command line parsing
# ⋅- (02) --output string
# ⋅- (03) logfile opening
# ⋅- (04) project name & version
# ⋅- (05) ARGS.report interpretation
# ⋅- (06) exit handler
# ⋅- (07) serializers import
# ⋅- (08) checkup
# ⋅- (09) download default config file
# ⋅- (10) temp file opening
# ⋅- (11) known data init
# ⋅- (12) call to main()
# ⋅       - (12.1) main(): debug messages
# ⋅       - (12.2) main(): cmp string interpretation
# ⋅       - (12.3) main(): config file reading
# ⋅       - (12.4) main(): results computing
# ⋅       - (12.5) main(): report
if wisteria.globs.ARGS.report in REPORT_SHORTCUTS:
    if wisteria.globs.ARGS.verbosity >= VERBOSITY_DETAILS:
        msginfo(f"--report '{wisteria.globs.ARGS.report}' "
                f"interpreted as '{REPORT_SHORTCUTS[wisteria.globs.ARGS.report]}'.")
    wisteria.globs.ARGS.report = REPORT_SHORTCUTS[wisteria.globs.ARGS.report]
elif not wisteria.globs.ARGS.report.endswith(";"):
    wisteria.globs.ARGS.report += ";"
    if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
        msginfo("--report: semicolon added at the end; "
                f"--report is now '{wisteria.globs.ARGS.report}'.")
if wisteria.globs.ARGS.verbosity == VERBOSITY_DEBUG:
    msgdebug("From now --report (wisteria.globs.ARGS.report) is set "
             f"to '{wisteria.globs.ARGS.report}'.")

# =============================================================================
# This point is only reached if there's no --version/--help argument
# on the command line.
# =============================================================================
ARGS = wisteria.globs.ARGS


# =============================================================================
# (06) exit handler
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) command line parsing
# ⋅- (02) --output string
# ⋅- (03) logfile opening
# ⋅- (04) project name & version
# ⋅- (05) ARGS.report interpretation
# ⋅- (06) exit handler
# ⋅- (07) serializers import
# ⋅- (08) checkup
# ⋅- (09) download default config file
# ⋅- (10) temp file opening
# ⋅- (11) known data init
# ⋅- (12) call to main()
# ⋅       - (12.1) main(): debug messages
# ⋅       - (12.2) main(): cmp string interpretation
# ⋅       - (12.3) main(): config file reading
# ⋅       - (12.4) main(): results computing
# ⋅       - (12.5) main(): report

# exit handler: let's remove the tmp file if it exists.
def exit_handler():
    """
        exit_handler()

        Remove the tmp file if it exists
    """
    if os.path.exists(TMPFILENAME):
        os.remove(TMPFILENAME)


atexit.register(exit_handler)


# =============================================================================
# (07) serializers import
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) command line parsing
# ⋅- (02) --output string
# ⋅- (03) logfile opening
# ⋅- (04) project name & version
# ⋅- (05) ARGS.report interpretation
# ⋅- (06) exit handler
# ⋅- (07) serializers import
# ⋅- (08) checkup
# ⋅- (09) download default config file
# ⋅- (10) temp file opening
# ⋅- (11) known data init
# ⋅- (12) call to main()
# ⋅       - (12.1) main(): debug messages
# ⋅       - (12.2) main(): cmp string interpretation
# ⋅       - (12.3) main(): config file reading
# ⋅       - (12.4) main(): results computing
# ⋅       - (12.5) main(): report
wisteria.serializers.init_serializers()


# =============================================================================
# (08) checkup
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) command line parsing
# ⋅- (02) --output string
# ⋅- (03) logfile opening
# ⋅- (04) project name & version
# ⋅- (05) ARGS.report interpretation
# ⋅- (06) exit handler
# ⋅- (07) serializers import
# ⋅- (08) checkup
# ⋅- (09) download default config file
# ⋅- (10) temp file opening
# ⋅- (11) known data init
# ⋅- (12) call to main()
# ⋅       - (12.1) main(): debug messages
# ⋅       - (12.2) main(): cmp string interpretation
# ⋅       - (12.3) main(): config file reading
# ⋅       - (12.4) main(): results computing
# ⋅       - (12.5) main(): report
def checkup():
    """
        checkup()

        Show some informations :
        - installed serializers;
        - configuration file that would be used; does this file exist ?
          can this file be read without errors ?
    """
    serializers = wisteria.globs.SERIALIZERS

    msgreport("* Serializers:")
    for serializer in serializers.values():
        msgreport(f"  - {serializer.checkup_repr()}")

    msgreport("")

    msgreport("* Config file:")
    if not os.path.exists(ARGS.cfgfile):
        diagnostic = "Such a file doesn't exist."
    else:
        if read_cfgfile(ARGS.cfgfile) is None:
            diagnostic = "Such a file exists but can't be read correctly."
        else:
            diagnostic = "Such a file exists and can be read without errors."

    msgreport(f"  With current arguments, configuration file would be '{ARGS.cfgfile}' "
              f"({normpath(ARGS.cfgfile)}). " + diagnostic)


if wisteria.globs.ARGS.checkup:
    checkup()
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
    sys.exit(1)


# =============================================================================
# (09) download default config file
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) command line parsing
# ⋅- (02) --output string
# ⋅- (03) logfile opening
# ⋅- (04) project name & version
# ⋅- (05) ARGS.report interpretation
# ⋅- (06) exit handler
# ⋅- (07) serializers import
# ⋅- (08) checkup
# ⋅- (09) download default config file
# ⋅- (10) temp file opening
# ⋅- (11) known data init
# ⋅- (12) call to main()
# ⋅       - (12.1) main(): debug messages
# ⋅       - (12.2) main(): cmp string interpretation
# ⋅       - (12.3) main(): config file reading
# ⋅       - (12.4) main(): results computing
# ⋅       - (12.5) main(): report
if wisteria.globs.ARGS.downloadconfigfile:
    downloadconfigfile()
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
    sys.exit(2)


# =============================================================================
# (10) temp file opening
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) command line parsing
# ⋅- (02) --output string
# ⋅- (03) logfile opening
# ⋅- (04) project name & version
# ⋅- (05) ARGS.report interpretation
# ⋅- (06) exit handler
# ⋅- (07) serializers import
# ⋅- (08) checkup
# ⋅- (09) download default config file
# ⋅- (10) temp file opening
# ⋅- (11) known data init
# ⋅- (12) call to main()
# ⋅       - (12.1) main(): debug messages
# ⋅       - (12.2) main(): cmp string interpretation
# ⋅       - (12.3) main(): config file reading
# ⋅       - (12.4) main(): results computing
# ⋅       - (12.5) main(): report

# Such a file is required to create file descriptor objects.
# The temp. file will be removed at the end of the program.
if not os.path.exists(TMPFILENAME):
    with open(TMPFILENAME, "w", encoding="utf-8") as tmpfile:
        pass


# =============================================================================
# (11) known data init
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) command line parsing
# ⋅- (02) --output string
# ⋅- (03) logfile opening
# ⋅- (04) project name & version
# ⋅- (05) ARGS.report interpretation
# ⋅- (06) exit handler
# ⋅- (07) serializers import
# ⋅- (08) checkup
# ⋅- (09) download default config file
# ⋅- (10) temp file opening
# ⋅- (11) known data init
# ⋅- (12) call to main()
# ⋅       - (12.1) main(): debug messages
# ⋅       - (12.2) main(): cmp string interpretation
# ⋅       - (12.3) main(): config file reading
# ⋅       - (12.4) main(): results computing
# ⋅       - (12.5) main(): report
wisteria.data.init_data()


def main():
    """
        main()

        Main entrypoint in the project. This method is called when Wisteria is called from outside,
        e.g. by the command line.

        _______________________________________________________________________

        RETURNED VALUE:
                (pimydoc)exit codes
                ⋅*  0: normal exit code
                ⋅*  1: normal exit code after --checkup
                ⋅*  2: normal exit code after --downloadconfigfile
                ⋅* -1: error, given config file can't be read (missing or ill-formed file)
                ⋅* -2: error, ill-formed --cmp string
                ⋅* -3: internal error, data can't be loaded
                ⋅* -4: internal error, an error occured while computing the results
                ⋅* -5: internal error, an error in main()
                ⋅* -6: error, ill-formed --output string
    """
    data = wisteria.globs.DATA
    serializers = wisteria.globs.SERIALIZERS

    # =========================================================================
    # (12.1) main(): debug messages
    # =========================================================================
    # (pimydoc)code structure
    # ⋅- (01) command line parsing
    # ⋅- (02) --output string
    # ⋅- (03) logfile opening
    # ⋅- (04) project name & version
    # ⋅- (05) ARGS.report interpretation
    # ⋅- (06) exit handler
    # ⋅- (07) serializers import
    # ⋅- (08) checkup
    # ⋅- (09) download default config file
    # ⋅- (10) temp file opening
    # ⋅- (11) known data init
    # ⋅- (12) call to main()
    # ⋅       - (12.1) main(): debug messages
    # ⋅       - (12.2) main(): cmp string interpretation
    # ⋅       - (12.3) main(): config file reading
    # ⋅       - (12.4) main(): results computing
    # ⋅       - (12.5) main(): report
    if ARGS.verbosity == VERBOSITY_DEBUG:
        msgdebug(f"known data: {list(data.keys())}")
    if ARGS.verbosity == VERBOSITY_DEBUG:
        msgdebug(f"known serializers: {serializers}")

    try:
        # =========================================================================
        # (12.2) main(): cmp string interpretation
        # =========================================================================
        # (pimydoc)code structure
        # ⋅- (01) command line parsing
        # ⋅- (02) --output string
        # ⋅- (03) logfile opening
        # ⋅- (04) project name & version
        # ⋅- (05) ARGS.report interpretation
        # ⋅- (06) exit handler
        # ⋅- (07) serializers import
        # ⋅- (08) checkup
        # ⋅- (09) download default config file
        # ⋅- (10) temp file opening
        # ⋅- (11) known data init
        # ⋅- (12) call to main()
        # ⋅       - (12.1) main(): debug messages
        # ⋅       - (12.2) main(): cmp string interpretation
        # ⋅       - (12.3) main(): config file reading
        # ⋅       - (12.4) main(): results computing
        # ⋅       - (12.5) main(): report
        success, serializer1, serializer2, cmpdata = read_cmpstring(ARGS.cmp)
        if ARGS.verbosity == VERBOSITY_DEBUG:
            msgdebug(f"Result of the call to read_cmpstring('{ARGS.cmp}'): "
                     f"{success}, {serializer1}, {serializer2}, {cmpdata}")

        if not success:
            msgerror("(ERRORID013) an error occured "
                     f"while reading cmp string '{ARGS.cmp}'.")

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
            return -2

        # =========================================================================
        # (12.3) main(): config file reading
        # =========================================================================
        # (pimydoc)code structure
        # ⋅- (01) command line parsing
        # ⋅- (02) --output string
        # ⋅- (03) logfile opening
        # ⋅- (04) project name & version
        # ⋅- (05) ARGS.report interpretation
        # ⋅- (06) exit handler
        # ⋅- (07) serializers import
        # ⋅- (08) checkup
        # ⋅- (09) download default config file
        # ⋅- (10) temp file opening
        # ⋅- (11) known data init
        # ⋅- (12) call to main()
        # ⋅       - (12.1) main(): debug messages
        # ⋅       - (12.2) main(): cmp string interpretation
        # ⋅       - (12.3) main(): config file reading
        # ⋅       - (12.4) main(): results computing
        # ⋅       - (12.5) main(): report
        config = None
        if cmpdata == "ini":
            config = read_cfgfile(ARGS.cfgfile)

            if config is None:
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
                return -1

        # =========================================================================
        # (12.4) main(): results computing
        # =========================================================================
        # (pimydoc)code structure
        # ⋅- (01) command line parsing
        # ⋅- (02) --output string
        # ⋅- (03) logfile opening
        # ⋅- (04) project name & version
        # ⋅- (05) ARGS.report interpretation
        # ⋅- (06) exit handler
        # ⋅- (07) serializers import
        # ⋅- (08) checkup
        # ⋅- (09) download default config file
        # ⋅- (10) temp file opening
        # ⋅- (11) known data init
        # ⋅- (12) call to main()
        # ⋅       - (12.1) main(): debug messages
        # ⋅       - (12.2) main(): cmp string interpretation
        # ⋅       - (12.3) main(): config file reading
        # ⋅       - (12.4) main(): results computing
        # ⋅       - (12.5) main(): report
        compute_results__res = compute_results(config,
                                               serializer1,
                                               serializer2,
                                               cmpdata)
        if compute_results__res[0] is None:
            return compute_results__res[1]
        results = compute_results__res[0]

        # =========================================================================
        # (12.5) main(): report
        # =========================================================================
        # (pimydoc)code structure
        # ⋅- (01) command line parsing
        # ⋅- (02) --output string
        # ⋅- (03) logfile opening
        # ⋅- (04) project name & version
        # ⋅- (05) ARGS.report interpretation
        # ⋅- (06) exit handler
        # ⋅- (07) serializers import
        # ⋅- (08) checkup
        # ⋅- (09) download default config file
        # ⋅- (10) temp file opening
        # ⋅- (11) known data init
        # ⋅- (12) call to main()
        # ⋅       - (12.1) main(): debug messages
        # ⋅       - (12.2) main(): cmp string interpretation
        # ⋅       - (12.3) main(): config file reading
        # ⋅       - (12.4) main(): results computing
        # ⋅       - (12.5) main(): report
        report(results,
               (serializer1, serializer2, cmpdata))

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
        return 0

    except WisteriaError as exception:
        msgerror(exception)

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
        # TODO
        return -5


# =============================================================================
# (12) call to main()
# =============================================================================
# (pimydoc)code structure
# ⋅- (01) command line parsing
# ⋅- (02) --output string
# ⋅- (03) logfile opening
# ⋅- (04) project name & version
# ⋅- (05) ARGS.report interpretation
# ⋅- (06) exit handler
# ⋅- (07) serializers import
# ⋅- (08) checkup
# ⋅- (09) download default config file
# ⋅- (10) temp file opening
# ⋅- (11) known data init
# ⋅- (12) call to main()
# ⋅       - (12.1) main(): debug messages
# ⋅       - (12.2) main(): cmp string interpretation
# ⋅       - (12.3) main(): config file reading
# ⋅       - (12.4) main(): results computing
# ⋅       - (12.5) main(): report
if __name__ == '__main__':
    sys.exit(main())

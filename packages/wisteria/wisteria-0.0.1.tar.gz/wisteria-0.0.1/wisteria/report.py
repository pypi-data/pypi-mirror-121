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
    report.py

    report() function which prints the report.

    ___________________________________________________________________________

    o  report_section_a()
    o  report_section_b1a(results)
    o  report_section_b1b(results)
    o  report_section_b1c(results)
    o  report_section_b2a(results)
    o  report_section_b2b(results)
    o  report_section_c1a(results)
    o  report_section_c1b(results)
    o  report_section_c2b(results)
    o  report(results, s1s2d)
"""
import rich.table
from rich import print as rprint

import wisteria.globs
from wisteria.wisteriaerror import WisteriaError


def report_section_a(results):
    """
        report_section_a()

        Sub-function of report() for report section "A"
        (pimydoc)report sections
        ⋅* A         : main title
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C     : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
    """
    args = wisteria.globs.ARGS

    if "titles;" in args.report:
        rprint("[bold white on blue](A) REPORT with --cmp set to "
               f"'[italic]{args.cmp}[/italic]'[/bold white on blue]")
        rprint()


def report_section_b1a(results):
    """
        report_section_b1a()

        Sub-function of report() for report section "B1a"
        (pimydoc)report sections
        ⋅* A         : main title
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C     : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
    """
    args = wisteria.globs.ARGS

    if "titles;" in args.report:
        rprint("[bold white on blue](B1a) full details: serializer * data object[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("serializer/data object", width=25)
    table.add_column("enc. ok ?", width=12)
    table.add_column("enc. time", width=10)
    table.add_column("jsonstr. len.", width=13)
    table.add_column("dec. ok ?", width=12)
    table.add_column("dec. time", width=10)
    table.add_column("enc ⇆ dec ?", width=12)

    for serializer in results.serializers:
        table.add_row("[yellow]" + serializer + ":" + "[/yellow]")
        for dataobj in results.dataobjs:
            table.add_row(
                "> " + "[white]" + dataobj + "[/white]",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time"),
                results.repr_attr(serializer, dataobj, "encoding_strlen"),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time"),
                results.repr_attr(serializer, dataobj, "similarity"))
    rprint(table)
    rprint()


def report_section_b1b(results):
    """
        report_section_b1b()

        Sub-function of report() for report section "B1b"
        (pimydoc)report sections
        ⋅* A         : main title
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C     : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
    """
    args = wisteria.globs.ARGS

    if "titles;" in args.report:
        rprint("[bold white on blue](B1b) full details: serializers[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("serializer", width=25)
    table.add_column(f"enc. ok ? (max={results.dataobjs_number})", width=12)
    table.add_column("Σ enc. time", width=10)
    table.add_column("Σ jsonstr. len.", width=13)
    table.add_column(f"dec. ok ? (max={results.dataobjs_number})", width=12)
    table.add_column("Σ dec. time", width=10)
    table.add_column(f"enc ⇆ dec ? (max={results.dataobjs_number})", width=12)

    for serializer in results.serializers:
        table.add_row(
            f"[yellow]{serializer}[/yellow]",
            f"{results.ratio_encoding_success(serializer=serializer)}",
            f"{results.total_encoding_time(serializer=serializer)}",
            f"{results.total_encoding_strlen(serializer=serializer)}",
            f"{results.ratio_decoding_success(serializer=serializer)}",
            f"{results.total_decoding_time(serializer=serializer)}",
            f"{results.ratio_similarity(serializer=serializer)}",
        )
    rprint(table)
    rprint()


def report_section_b1c(results):
    """
        report_section_b1c()

        Sub-function of report() for report section "B1c"
        (pimydoc)report sections
        ⋅* A         : main title
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C     : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
    """
    args = wisteria.globs.ARGS

    if "titles;" in args.report:
        rprint("[bold white on blue](B1c) full details: serializer <S> can't handle <dataobj>[/bold white on blue]")
    for serializer in results.serializers:
        _list = tuple(dataobj for dataobj in results[serializer]
                      if not results[serializer][dataobj].similarity)
        if not _list:
            rprint(f"* [yellow]({serializer})[/yellow] There's no data object that serializer '[yellow]{serializer}[/yellow]' can't handle.")
        else:
            rprint(f"* [yellow]({serializer})[/yellow] Serializer '[yellow]{serializer}[/yellow]' can't handle the following data objects:")
            for dataobj in _list:
                rprint("  - ", "[white]" + dataobj + "[/white]")
    rprint()


def report_section_b2a(results):
    """
        report_section_b2a()

        Sub-function of report() for report section "B2a"
        (pimydoc)report sections
        ⋅* A         : main title
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C     : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
    """
    args = wisteria.globs.ARGS

    if "titles;" in args.report:
        rprint("[bold white on blue](B2a) full details: data object * serializer[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("data object/serializer", width=25)
    table.add_column("enc. ok ?", width=12)
    table.add_column("enc. time", width=10)
    table.add_column("jsonstr. len.", width=13)
    table.add_column("dec. ok ?", width=12)
    table.add_column("dec. time", width=10)
    table.add_column("enc ⇆ dec ?", width=12)

    for dataobj in results.dataobjs:
        table.add_row("[white]" + dataobj + ":" + "[/white]")
        for serializer in results.serializers:
            table.add_row(
                "> " + "[yellow]" + serializer + "[/yellow]",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time"),
                results.repr_attr(serializer, dataobj, "encoding_strlen"),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time"),
                results.repr_attr(serializer, dataobj, "similarity")
            )
    rprint(table)
    rprint()


def report_section_b2b(results):
    """
        report_section_b2b()

        Sub-function of report() for report section "B2b"
        (pimydoc)report sections
        ⋅* A         : main title
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C     : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
    """
    args = wisteria.globs.ARGS

    if "titles;" in args.report:
        rprint("[bold white on blue](B2b) full details: data objects[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("data object", width=25)
    table.add_column(f"enc. ok ? (max={results.serializers_number})", width=12)
    table.add_column("Σ enc. time", width=10)
    table.add_column("Σ jsonstr. len.", width=13)
    table.add_column(f"dec. ok ? (max={results.serializers_number})", width=12)
    table.add_column("Σ dec. time", width=10)
    table.add_column(f"enc ⇆ dec ? (max={results.serializers_number})", width=12)

    for dataobj in results.dataobjs:
        table.add_row(
            f"[white]{dataobj}[/white]",
            f"{results.ratio_encoding_success(dataobj=dataobj)}",
            f"{results.total_encoding_time(dataobj=dataobj)}",
            f"{results.total_encoding_strlen(dataobj=dataobj)}",
            f"{results.ratio_decoding_success(dataobj=dataobj)}",
            f"{results.total_decoding_time(dataobj=dataobj)}",
            f"{results.ratio_similarity(dataobj=dataobj)}",
        )
    rprint(table)
    rprint()


def report_section_c1a(results):
    """
        report_section_c1a()

        Sub-function of report() for report section "C1a"
        (pimydoc)report sections
        ⋅* A         : main title
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C     : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
    """
    args = wisteria.globs.ARGS

    if "titles;" in args.report:
        rprint("[bold white on blue](C1a) full details: serializer * data object (base 100)[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("serializer/data object", width=25)
    table.add_column("enc. ok ?", width=12)

    if base100 := results._get_base('encoding_time'):
        table.add_column(
            "enc. time "
            f"(base 100 = {results.repr_attr(serializer=base100.serializer, dataobj=base100.dataobj, attribute_name='encoding_time')})",
            width=10)
    else:
        table.add_column("enc. time [red](NO BASE 100)[/red]",
                         width=10)

    if base100 := results._get_base('decoding_time'):
        table.add_column(
            "jsonstr. len. "
            f"(base 100 = {results.repr_attr(serializer=base100.serializer, dataobj=base100.dataobj, attribute_name='encoding_strlen')})",
            width=13)
    else:
        table.add_column("jsonstr. len. [red](NO BASE 100)[/red]",
                         width=13)

    table.add_column("dec. ok ?", width=12)

    if base100 := results._get_base('decoding_time'):
        table.add_column(
            "dec. time "
            f"(base 100 = {results.repr_attr(serializer=base100.serializer, dataobj=base100.dataobj, attribute_name='decoding_time')})",
            width=10)
    else:
        table.add_column("dec. time [red](NO BASE 100)[/red]",
                         width=10)

    table.add_column("enc ⇆ dec ?", width=12)

    for serializer in results.serializers:
        table.add_row("[yellow]" + serializer + ":" + "[/yellow]")
        for dataobj in results.dataobjs:
            table.add_row(
                "> " + "[white]" + dataobj + "[/white]",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time", output="base100"),
                results.repr_attr(serializer, dataobj, "encoding_strlen", output="base100"),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time", output="base100"),
                results.repr_attr(serializer, dataobj, "similarity"))
    rprint(table)
    rprint()


def report_section_c1b(results):
    """
        report_section_c1b()

        Sub-function of report() for report section "C1b"
        (pimydoc)report sections
        ⋅* A         : main title
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C     : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
    """
    args = wisteria.globs.ARGS

    if "titles;" in args.report:
        rprint("[bold white on blue](C1b) full details: serializers (base 100)[/bold white on blue]")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("serializer", width=25)
    table.add_column(f"enc. ok ? (max={results.dataobjs_number})", width=12)
    if base100 := results._get_serializers_base('encoding_time'):
        table.add_column("Σ enc. time "
                         f"(base 100 = {results.total_encoding_time(serializer=base100)})",
                         width=10)
    else:
        table.add_column("Σ enc. time [red](NO BASE 100)[/red]",
                         width=10)

    if base100 := results._get_serializers_base('encoding_strlen'):
        table.add_column("Σ jsonstr. len. "
                         f"(base 100 = {results.total_encoding_strlen(serializer=base100)})",
                         width=13)
    else:
        table.add_column("Σ jsonstr. len. [red](NO BASE 100)[/red]", width=13)

    table.add_column(f"dec. ok ? (max={results.dataobjs_number})", width=12)

    if base100 := results._get_serializers_base('decoding_time'):
        table.add_column("Σ dec. time "
                         f"(base 100 = {results.total_decoding_time(serializer=base100)})",
                         width=10)
    else:
        table.add_column("Σ dec. time [red](NO BASE 100)[/red]",
                         width=10)

    table.add_column(f"enc ⇆ dec ? (max={results.dataobjs_number})", width=12)

    for serializer in results.serializers:
        table.add_row(
            f"[yellow]{serializer}[/yellow]",
            f"{results.ratio_encoding_success(serializer=serializer)}",
            f"{results.total_encoding_time(serializer=serializer, output='base100')}",
            f"{results.total_encoding_strlen(serializer=serializer, output='base100')}",
            f"{results.ratio_decoding_success(serializer=serializer)}",
            f"{results.total_decoding_time(serializer=serializer, output='base100')}",
            f"{results.ratio_similarity(serializer=serializer)}",
        )
    rprint(table)
    rprint()


def report_section_c2a(results):
    """
        report_section_c2a()

        Sub-function of report() for report section "C2a"
        (pimydoc)report sections
        ⋅* A         : main title
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C     : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
    """
    args = wisteria.globs.ARGS

    if "titles;" in args.report:
        rprint("[bold white on blue](C2a) full details: data object * serializer (base 100)[/bold white on blue]")
    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("data object/serializer", width=25)

    table.add_column("enc. ok ?", width=12)

    if base100 := results._get_base('encoding_time'):
        table.add_column(
            "enc. time "
            f"(base 100 = {results.repr_attr(serializer=base100.serializer, dataobj=base100.dataobj, attribute_name='encoding_time')})",
            width=10)
    else:
        table.add_column("enc. time [red](NO BASE 100)[/red]",
                         width=10)

    if base100 := results._get_base('encoding_strlen'):
        table.add_column(
            "jsonstr. len. "
            f"(base 100 = {results.repr_attr(serializer=base100.serializer, dataobj=base100.dataobj, attribute_name='encoding_strlen')})",
            width=13)
    else:
        table.add_column("jsonstr. len. [red](NO BASE 100)[/red]",
                         width=13)

    table.add_column("dec. ok ?", width=12)

    if base100 := results._get_base('decoding_time'):
        table.add_column(
            "dec. time "
            f"(base 100 = {results.repr_attr(serializer=base100.serializer, dataobj=base100.dataobj, attribute_name='decoding_time')})",
            width=10)
    else:
        table.add_column("dec. time [red](NO BASE 100)[/red]",
                         width=10)

    table.add_column("enc ⇆ dec ?", width=12)

    for dataobj in results.dataobjs:
        table.add_row("[white]" + dataobj + ":" + "[/white]")
        for serializer in results.serializers:
            table.add_row(
                "> " + "[yellow]" + serializer + "[/yellow]",
                results.repr_attr(serializer, dataobj, "encoding_success"),
                results.repr_attr(serializer, dataobj, "encoding_time", output='base100'),
                results.repr_attr(serializer, dataobj, "encoding_strlen", output='base100'),
                results.repr_attr(serializer, dataobj, "decoding_success"),
                results.repr_attr(serializer, dataobj, "decoding_time", output='base100'),
                results.repr_attr(serializer, dataobj, "similarity")
            )
    rprint(table)
    rprint()


def report_section_c2b(results):
    """
        report_section_c2b()

        Sub-function of report() for report section "C2b"
        (pimydoc)report sections
        ⋅* A         : main title
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C     : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)

        _______________________________________________________________________

        ARGUMENT:
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
    """
    args = wisteria.globs.ARGS

    if "titles;" in args.report:
        rprint("[bold white on blue](C2b) full details: data objects (base 100)[/bold white on blue]")

    table = rich.table.Table(show_header=True, header_style="bold blue")
    table.add_column("data object", width=25)
    table.add_column(f"enc. ok ? (max={results.serializers_number})", width=12)

    if base100 := results._get_dataobjs_base('encoding_time'):
        table.add_column("Σ enc. time "
                         f"(base 100 = {results.total_encoding_time(dataobj=base100)})",
                         width=10)
    else:
        table.add_column("Σ enc. time [red](NO BASE 100)[/red]",
                         width=10)

    if base100 := results._get_dataobjs_base('encoding_strlen'):
        table.add_column("Σ jsonstr. len. "
                         f"(base 100 = {results.total_encoding_strlen(dataobj=base100)})",
                         width=13)
    else:
        table.add_column("Σ jsonstr. len. [red](NO BASE 100)[/red]", width=13)

    table.add_column(f"dec. ok ? (max={results.serializers_number})", width=12)

    if base100 := results._get_dataobjs_base('decoding_time'):
        table.add_column("Σ dec. time "
                         f"(base 100 = {results.total_decoding_time(dataobj=base100)})",
                         width=10)
    else:
        table.add_column("Σ dec. time [red](NO BASE 100)[/red]",
                         width=10)

    table.add_column(f"enc ⇆ dec ? (max={results.serializers_number})", width=12)

    for dataobj in results.dataobjs:
        table.add_row(
            f"[white]{dataobj}[/white]",
            f"{results.ratio_encoding_success(dataobj=dataobj)}",
            f"{results.total_encoding_time(dataobj=dataobj, output='base100')}",
            f"{results.total_encoding_strlen(dataobj=dataobj, output='base100')}",
            f"{results.ratio_decoding_success(dataobj=dataobj)}",
            f"{results.total_decoding_time(dataobj=dataobj, output='base100')}",
            f"{results.ratio_similarity(dataobj=dataobj)}",
        )
    rprint(table)
    rprint()


def report(results,
           s1s2d):
    """
        report()

        Print an analyze of <results>.

        (pimydoc)report sections
        ⋅* A         : main title
        ⋅* B         : full details (raw results)
        ⋅  - B1      : full details (serializers)
        ⋅    . B1a   : full details: serializer * data object
        ⋅    . B1b   : full details: serializers
        ⋅    . B1c   : full details: full details: serializer <S> can't handle <dataobj>
        ⋅  - B2      : full details (data objects)
        ⋅    . B2a   : full details: data object * serializer
        ⋅    . B2b   : full details: data objects
        ⋅* C     : full details (base 100)
        ⋅  - C1      : full details (serializers, base 100)
        ⋅    . C1a   : full details: serializer * data object (base 100)
        ⋅    . C1b   : full details: serializers (base 100)
        ⋅  - C2      : full details (data objects, base 100)
        ⋅    . C2a   : full details: data object * serializer (base 100)
        ⋅    . C2b   : full details: data objects (base 100)
        _______________________________________________________________________

        ARGUMENTS:
TODO
        o  results: (SerializationResults)a dict of
                    [(str)serializer][(str)data_name] = SerializationResult
    """
    args = wisteria.globs.ARGS

    serializer1, serializer2, data = s1s2d

    str2reportsection = {
        "A": (report_section_a,),
        "B": (report_section_b1a,
              report_section_b1b,
              report_section_b1c,
              report_section_b2a,
              report_section_b2b),
        "B1": (report_section_b1a,
               report_section_b1b,
               report_section_b1c),
        "B1a": (report_section_b1a,),
        "B1b": (report_section_b1b,),
        "B1c": (report_section_b1c,),
        "B2": (report_section_b2a,
               report_section_b2b),
        "B2a": (report_section_b2a,),
        "B2b": (report_section_b2b,),
        "C": (report_section_c1a,
              report_section_c1b,
              report_section_c2a,
              report_section_c2b),
        "C1": (report_section_c1a,
               report_section_c1b,),
        "C1a": (report_section_c1a,),
        "C1b": (report_section_c1b,),
        "C2": (report_section_c2b,),
        "C2a": (report_section_c2a,),
        "C2b": (report_section_c2b,),
        }

    for report_section in args.report.split(";"):
        if report_section in str2reportsection:
            for func in str2reportsection[report_section]:
                func(results)
        elif report_section.strip() != "":
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRXXX
            # ⋅- checkup messages start with *
            raise WisteriaError(
                f"(ERR017) Can't interpret report section; "
                f"what is '{report_section}' ? args.report is '{args.report}' .")

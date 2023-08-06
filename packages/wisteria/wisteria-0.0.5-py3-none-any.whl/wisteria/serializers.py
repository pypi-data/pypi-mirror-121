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
    serializers.py

    All known serializers are defined here, in the SERIALIZERS dict. Each serializer
    has its own serializer_xxx function.
    A reference to each module imported is added in the MODULES dict.

    ___________________________________________________________________________

    o  MODULES dict

    o  SerializerDataObj class

    o  _len(obj)

    o  SerializationResults class
    o  SerializationResult class
    o  SerializationData class

    * serializer_iaswn(action="serialize", obj=None)
    * serializer_json(action="serialize", obj=None)
    * serializer_jsonpickle(action="serialize", obj=None)
    * serializer_marshal(action="serialize", obj=None)
    * serializer_pickle(action="serialize", obj=None)

    * SERIALIZERS dict
"""
import sys
import timeit

import wisteria.globs
from wisteria.globs import TIMEITNUMBER, MODULES
from wisteria.wisteriaerror import WisteriaError
from wisteria.utils import trytoimport
from wisteria.serializers_classes import SerializerData, SerializationResult


def _len(obj):
    """
        _len()

        Return the length of <obj>

        _______________________________________________________________________

        ARGUMENT: (bytes|str)<obj>

        RETURNED VALUE: the length of <obj>
    """
    if isinstance(obj, str):
        return len(bytes(obj, "utf-8"))
    return len(obj)


def serializer_iaswn(action="serialize",
                     obj=None):
    """
        serializer_iaswn()

        Serializer for the Iaswn module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["iaswn"]

    # -------------------
    # action == "version"
    # -------------------
    if action == "version":
        return module.__version__

    # ---------------------
    # action == "serialize"
    # ---------------------
    if action != "serialize":
        raise WisteriaError(f"(ERRORID030) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.encode(obj)
        _timeit = timeit.Timer('module.encode(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except module.IaswnError:
        _error = True

    if not _error:
        try:
            _res2 = module.decode(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.decode(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except module.IaswnError:
            pass

    return res


def serializer_json(action="serialize",
                    obj=None):
    """
        serializer_json()

        Serializer for the json module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["json"]

    if action == "version":
        return module.__version__

    if action != "serialize":
        raise WisteriaError(f"(ERRORID031) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except TypeError:
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except (TypeError, AttributeError):
            pass

    return res


def serializer_jsonpickle(action="serialize",
                          obj=None):
    """
        serializer_jsonpickle()

        Serializer for the jsonpickle module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["jsonpickle"]

    if action == "version":
        return module.__version__

    if action != "serialize":
        raise WisteriaError(f"(ERRORID032) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except TypeError:
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except (TypeError, AttributeError):
            pass

    return res


def serializer_marshal(action="serialize",
                       obj=None):
    """
        serializer_marshal()

        Serializer for the marshal module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["marshal"]

    if action == "version":
        return f"version {module.version}; (Python version) {sys.version}"

    if action != "serialize":
        raise WisteriaError(f"(ERRORID033) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except (TypeError, ValueError):
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except (TypeError, AttributeError):
            pass

    return res


def serializer_pickle(action="serialize",
                      obj=None):
    """
        serializer_pickle()

        Serializer for the pickle module.

        Like every serializer_xxx() function:
        * this function may return (action='version') the version of the concerned module.
        * this function may try (action='serialize') to encode/decode an <obj>ect.
        * if the serializer raises an error, this error is silently converted and no exception
          is raised. If an internal error happpens, a WisteriaError exception is raised.

        This function assumes that the concerned module has already be imported.

        _______________________________________________________________________

        ARGUMENTS:
        o  action: (str) either "version" either "serialize"
        o  obj:    the object to be serialized

        RETURNED VALUE:
           - None if an error occcured
           - if <action> is (str)"version", return a string.
           - if <action> is (str)"serialize", return a SerializationResult object.
    """
    module = MODULES["pickle"]

    if action == "version":
        return "(Python version) "+sys.version

    if action != "serialize":
        raise WisteriaError(f"(ERRORID034) Unknown 'action' keyword '{action}'.")

    res = SerializationResult()

    _error = False
    try:
        _res = module.dumps(obj)
        _timeit = timeit.Timer('module.dumps(obj)',
                               globals=locals())
        res.encoding_success = True
        res.encoding_strlen = _len(_res)
        res.encoding_time = _timeit.timeit(TIMEITNUMBER)
    except TypeError:
        _error = True

    if not _error:
        try:
            _res2 = module.loads(_res)
            res.decoding_success = True
            _timeit = timeit.Timer("module.loads(_res)",
                                   globals=locals())
            res.decoding_time = _timeit.timeit(TIMEITNUMBER)

            if obj == _res2:
                res.similarity = True
        except (TypeError, AttributeError):
            pass

    return res


def init_serializers():
    """
        init_serializers()

        Initialize wisteria.globs.SERIALIZERS
    """
    wisteria.globs.SERIALIZERS = {
        "iaswn": SerializerData(
            human_name="Iaswn",
            internet="https://github.com/suizokukan/iaswn",
            available=trytoimport("iaswn"),
            func=serializer_iaswn),
        "json": SerializerData(
            human_name="json",
            internet="https://docs.python.org/3/library/json.html",
            available=trytoimport("json"),
            func=serializer_json),
        "jsonpickle": SerializerData(
            human_name="jsonpickle",
            internet="https://jsonpickle.github.io/",
            available=trytoimport("jsonpickle"),
            func=serializer_jsonpickle),
        "marshal": SerializerData(
            human_name="marshal",
            internet="https://docs.python.org/3/library/marshal.html#module-marshal",
            available=trytoimport("marshal"),
            func=serializer_marshal),
        "pickle": SerializerData(
            human_name="pickle",
            internet="https://docs.python.org/3/library/pickle.html",
            available=trytoimport("pickle"),
            func=serializer_pickle),
    }
    for _serializer in wisteria.globs.SERIALIZERS:
        if wisteria.globs.SERIALIZERS[_serializer].available:
            wisteria.globs.SERIALIZERS[_serializer].version = \
                wisteria.globs.SERIALIZERS[_serializer].func("version")

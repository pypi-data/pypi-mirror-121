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

    * MODULES dict

    *  trytoimport(module_name)
    *  _len(obj)

    * SerializationResult class
    * SerializationData class

    * serializer_iaswn(action="serialize", obj=None):
    * serializer_jsonpickle(action="serialize", obj=None):

    * SERIALIZERS dict
"""
from dataclasses import dataclass
import importlib
import timeit

from rich import print as rprint

from wisteria.globs import VERBOSITY_DETAILS
from wisteria.globs import ARGS, TIMEITNUMBER
from wisteria.wisteriaerror import WisteriaError

MODULES = {}


@dataclass
class SerializerDataObj:
    """
        SerializerDataObj class

        Nothing but an easy way to set (serializer, dataobj)
    """
    serializer: str = None
    dataobj: str = None


def trytoimport(module_name):
    """
        trytoimport()

        Try to import <module_name> module.
        _______________________________________________________________________

        ARGUMENT:
        o  (str)module_name: the module to be imported

        RETURNED VALUE: (bool)success
    """
    res = True
    try:
        MODULES[module_name] = importlib.import_module(module_name)
        if ARGS.verbosity >= VERBOSITY_DETAILS:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRXXX
            # ⋅- checkup messages start with *
            rprint(f"> Module '{module_name}' successfully imported.")
    except ModuleNotFoundError:
        res = False
    return res


def _len(obj):
    if isinstance(obj, str):
        return len(bytes(obj, "utf-8"))
    return len(obj)


class SerializationResults(dict):
    """
        SerializationResults class

        SerializationResults objects are used to store all results created during the tests.

        A SerializationResults object has the following structure:
                SerializationResults[(str)serializer][(str)dataobj] = SerializationResult object

        Do not forget to call ._finish_initialization() once you have finished initializing <self>.

        _______________________________________________________________________

TODO
class attr ?

TODO il en manque !
        o  __init__(self)
        o  _finish_initialization(self)
        o  _format_ratio(self, inttotal_and_floatratio)
        o  _format_stringlength(self, int_stringlength)
        o  _format_success(self, bool_success)
        o  _get_dataobjs_base(self)
        o  _format_time(self, floattime)
        o  ratio_decoding_success(self, serializer=None, dataobj=None)
        o  ratio_encoding_success(self, serializer=None, dataobj=None)
        o  ratio_identify(self, serializer=None, dataobj=None)
        o  repr_attr(self, serializer, dataobj, attribute_name)
        o  total_decoding_time(self, serializer=None, dataobj=None)
        o  total_encoding_strlen(self, serializer=None, dataobj=None)
        o  total_encoding_time(self, serializer=None, dataobj=None)
    """
    def __init__(self):
        """
            SerializationResults.__init__()
        """
        dict.__init__(self)
        self.serializers = []
        self.dataobjs = []
        self.serializers_number = None
        self.dataobjs_number = None

    def _finish_initialization(self):
        """
            SerializationResults._finish_initialization()

            Once the initialization of <self> is over, this method must be called to
            set self.self.serializers, self.dataobjs, self.serializers_number
            and self.dataobjs_number.

            ___________________________________________________________________

            RETURNED VALUE: (bool)success
        """
        self.serializers = sorted(self.keys())
        self.serializers_number = len(self.serializers)

        if self.serializers_number == 0:
            # (pimydoc)console messages
            # ⋅- debug messages start with   @
            # ⋅- info messages start with    >
            # ⋅- error messages start with   ERRXXX
            # ⋅- checkup messages start with *
            rprint("ERR016: Incorrect data, there's no serializer.")
            return False

        first_serializer = tuple(self.serializers)[0]
        self.dataobjs = sorted(self[first_serializer].keys())
        self.dataobjs_number = len(self.dataobjs)

        return True

    @staticmethod
    def _format_base100(bool_is_base100_value,
                        float_base100):
        """
TODO
        """
        prefix = " "
        suffix = ""
        if bool_is_base100_value:
            prefix = "[italic]*"
            suffix = "[/italic]"

        return f"{prefix}{float_base100:.2f}{suffix}"

    @staticmethod
    def _format_ratio(inttotal_and_floatratio):
        """
            SerializationResults._format_ratio()

            Format the input argument into a string. The input argument is an absolute
            (int)number and a (float)fraction, its ratio.
                ex: (3, 0.5) > "3 (50 %)"

            _______________________________________________________________

            ARGUMENT: (int, float)inttotal_and_floatratio

            RETURNED VALUE: a formatted string representing the input argument.
        """
        if inttotal_and_floatratio != (None, None):
            return f"{inttotal_and_floatratio[0]} ({100*inttotal_and_floatratio[1]:.2f} %)"
        return "(no data)"

    @staticmethod
    def _format_stringlength(int_stringlength):
        """
            SerializationResults._format_stringlength()

            Format the input argument into a string. The input argument is a (int)number
            of characters
                ex: 3 > "3 chars"

            _______________________________________________________________

            ARGUMENT: (int)int_stringlength, a string number.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        return f"{int_stringlength} chars"

    @staticmethod
    def _format_success(bool_success):
        """
            SerializationResults._format_success()

            Format the input argument into a string. The input argument is a (bool)success.
                ex: False > "NOT OK"

            _______________________________________________________________

            ARGUMENT: (bool)bool_success

            RETURNED VALUE: a formatted string representing the input argument.
        """
        return "ok" if bool_success else "[red]NOT OK[/red]"

    @staticmethod
    def _format_time(floattime):
        """
            SerializationResults._format_time()

            Format the input argument into a string. The input argument is a (float)time laps.
                ex: 0.333345677 > "0.333345"
            _______________________________________________________________

            ARGUMENT: (float)floattime

            RETURNED VALUE: a formatted string representing the input argument.
        """
        return f"{floattime:.6f}"

    def _get_base(self,
                  attribute):
        """
TODO
        Return serializer+base data object for attribute <attribute>.

attribute: seulement 3 possibilités et non pas 5
        """
        if attribute == "encoding_time":
            for serializer in self.serializers:
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj].encoding_time:
                        return SerializerDataObj(serializer=serializer, dataobj=dataobj)
            return SerializerDataObj()

        if attribute == "decoding_time":
            for serializer in self.serializers:
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj].decoding_time:
                        return SerializerDataObj(serializer=serializer, dataobj=dataobj)
            return SerializerDataObj()

        if attribute == "encoding_strlen":
            for serializer in self.serializers:
                for dataobj in self.dataobjs:
                    if self[serializer][dataobj].encoding_strlen:
                        return SerializerDataObj(serializer=serializer, dataobj=dataobj)
            return SerializerDataObj()

        raise WisteriaError(f"Internal error: can't compute base100 for attribute '{attribute}'.")

    def _get_dataobjs_base(self,
                           attribute):
        """
        TODO

        Return base data object for attribute <attribute>.
        """
        if attribute == "encoding_time":
            for dataobj in self.dataobjs:
                if self[self.serializers[0]][dataobj].encoding_success:
                    return dataobj
            return None

        if attribute == "encoding_strlen":
            for dataobj in self.dataobjs:
                if self[self.serializers[0]][dataobj].encoding_strlen:
                    return dataobj
            return None

        if attribute == "decoding_time":
            for dataobj in self.dataobjs:
                if self[self.serializers[0]][dataobj].decoding_success:
                    return dataobj
            return None

        raise WisteriaError("Internal error: the result could not be computed. "
                          f"{attribute=};")

    def _get_serializers_base(self,
                              attribute):
        """
        TODO

        Return base serializer for attribute <attribute>.
        """
        if attribute == "encoding_time":
            for serializer in self.serializers:
                if self[serializer][self.dataobjs[0]].encoding_success:
                    return serializer
            return None

        if attribute == "encoding_strlen":
            for serializer in self.serializers:
                if self[serializer][self.dataobjs[0]].encoding_strlen:
                    return serializer
            return None

        if attribute == "decoding_time":
            for serializer in self.serializers:
                if self[serializer][self.dataobjs[0]].decoding_success:
                    return serializer
            return None

        raise WisteriaError("Internal error: the result could not be computed. "
                          f"{attribute=};")

    def ratio_decoding_success(self,
                               serializer=None,
                               dataobj=None):
        """
            SerializationResults.ratio_decoding_success()

            Compute and format the ratio of decoding success for a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <dataobj> can be set to
                         None.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None

        count = 0  # number of serializers or dataobjs that are taken in account.

        # serializer is not None:
        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_ratio((None, None))

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].decoding_success:
                    count += 1
            return SerializationResults._format_ratio((count, count/self.dataobjs_number))

        # dataobj is not None:
        if self.dataobjs_number == 0:
            return SerializationResults._format_ratio((None, None))

        for _serializer in self:
            if self[_serializer][dataobj].decoding_success:
                count += 1
        return SerializationResults._format_ratio((count, count/self.serializers_number))

    def ratio_encoding_success(self,
                               serializer=None,
                               dataobj=None):
        """
            SerializationResults.ratio_encoding_success()

            Compute and format the ratio of encoding success for a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <dataobj> can be set to
                         None.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None

        count = 0  # number of serializers or dataobjs that are taken in account.

        # serializer is not None:
        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_ratio((None, None))

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].encoding_success:
                    count += 1
            return SerializationResults._format_ratio((count, count/self.dataobjs_number))

        # dataobj is not None:
        if self.dataobjs_number == 0:
            return SerializationResults._format_ratio((None, None))

        for _serializer in self:
            if self[_serializer][dataobj].encoding_success:
                count += 1
        return SerializationResults._format_ratio((count, count/self.serializers_number))

    def ratio_similarity(self,
                         serializer=None,
                         dataobj=None):
        """
            SerializationResults.ratio_similarity()

            Compute and format the ratio of similarity success for a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <dataobj> can be set to
                         None.

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None

        count = 0  # number of serializers or dataobjs that are taken in account.

        # serializer is not None:
        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_ratio((None, None))

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].similarity:
                    count += 1
            return SerializationResults._format_ratio((count, count/self.dataobjs_number))

        # dataobj is not None:
        if self.dataobjs_number == 0:
            return SerializationResults._format_ratio((None, None))

        for _serializer in self:
            if self[_serializer][dataobj].similarity:
                count += 1
        return SerializationResults._format_ratio((count, count/self.serializers_number))

    def repr_attr(self,
                  serializer,
                  dataobj,
                  attribute_name,
                  output="formattedstr"):
        """
            SerializationResults.repr_attr()

            Format the value stored into self[serializer][dataobj].<attribute_name>.

            _______________________________________________________________
TODO
            ARGUMENT:
output="formattedstr" | "base100"

            RETURNED VALUE: a formatted string representing
                            self[serializer][dataobj].<attribute_name>
        """
        res = None  # unexpected result !

        # TODO
        # base100 n'existe que dans certains cas, il est donc impossible et inutile
        # de le calculer tout le temps.
        if output == "base100":
            base100_serializerdataobj = self._get_base(attribute=attribute_name)
            base100 = self[base100_serializerdataobj.serializer][base100_serializerdataobj.dataobj]

        if attribute_name == "decoding_success":
            if output == "formattedstr":
                res = SerializationResults._format_success(
                    self[serializer][dataobj].decoding_success)
            else:
                raise WisteriaError("Internal error. "
                                  f"Can't compute base 100 for attribute_name='{attribute_name}'.")

        if attribute_name == "decoding_time":
            if output == "formattedstr":
                res = SerializationResults._format_time(
                    self[serializer][dataobj].decoding_time)
            else:
                # output == "base100"
                res = SerializationResults._format_base100(
                    serializer == base100_serializerdataobj.serializer and
                    dataobj == base100_serializerdataobj.dataobj,
                    100*self[serializer][dataobj].decoding_time/base100.decoding_time)

        if attribute_name == "encoding_strlen":
            if output == "formattedstr":
                res = SerializationResults._format_stringlength(
                    self[serializer][dataobj].encoding_strlen)
            else:
                # output == "base100"
                res = SerializationResults._format_base100(
                    serializer == base100_serializerdataobj.serializer and
                    dataobj == base100_serializerdataobj.dataobj,
                    100*self[serializer][dataobj].encoding_strlen/base100.encoding_strlen)

        if attribute_name == "encoding_time":
            if output == "formattedstr":
                res = SerializationResults._format_time(
                    self[serializer][dataobj].encoding_time)
            else:
                # output == "base100"
                res = SerializationResults._format_base100(
                    serializer == base100_serializerdataobj.serializer and
                    dataobj == base100_serializerdataobj.dataobj,
                    100*self[serializer][dataobj].encoding_time/base100.encoding_time)

        if attribute_name == "encoding_success":
            if output == "formattedstr":
                res = SerializationResults._format_success(
                    self[serializer][dataobj].encoding_success)
            else:
                raise WisteriaError("Internal error. "
                                  f"Can't compute base 100 for attribute_name='{attribute_name}'.")

        if attribute_name == "similarity":
            if output == "formattedstr":
                res = SerializationResults._format_success(
                    self[serializer][dataobj].similarity)
            else:
                raise WisteriaError("Internal error. "
                                  f"Can't compute base 100 for attribute_name='{attribute_name}'.")

        if res is None:
            raise WisteriaError("Internal error: the result could not be computed. "
                              f"{serializer=}; {dataobj=}; {attribute_name=};")
        return res

    def total_decoding_time(self,
                            serializer=None,
                            dataobj=None,
                            output="formattedstr"):
        """
            SerializationResults.total_decoding_time()

            Compute and format the total decoding time used by a <serializer>
            OR by a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "formattedstr": formatted string (str)
                    - "base100": formatted string based on a "base 100" value (str)
            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None

        res = None  # unexpected result !
        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_time(None)

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].decoding_success:
                    total += self[serializer][_dataobj].decoding_time
            if output == "value":
                res = total
            if output == "formattedstr":
                res = SerializationResults._format_time(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    serializer == self._get_serializers_base('decoding_time'),
                    100*total/self.total_decoding_time(
                        serializer=self._get_serializers_base('decoding_time'),
                        output="value"))

        else:
            if self.dataobjs_number == 0:
                return SerializationResults._format_time(None)

            for _serializer in self:
                if self[_serializer][dataobj].decoding_success:
                    total += self[_serializer][dataobj].decoding_time
            if output == "value":
                res = total
            if output == "formattedstr":
                res = SerializationResults._format_time(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    dataobj == self._get_dataobjs_base('decoding_time'),
                    100*total/self.total_decoding_time(
                        dataobj=self._get_dataobjs_base('decoding_time'),
                        output="value"))

        if res is None:
            raise WisteriaError("Internal error: the result could not be computed. "
                              f"{serializer=}; {dataobj=}; {output=};")
        return res

    def total_encoding_strlen(self,
                              serializer=None,
                              dataobj=None,
                              output="formattedstr"):
        """
            SerializationResults.total_encoding_strlen()

            Compute and format the total encoding string length created by a <serializer>
            OR for a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "formattedstr": formatted string (str)
                    - "base100": formatted string based on a "base 100" value (str)

            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None

        res = None  # unexpected result !
        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_stringlength(None)

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].encoding_strlen:
                    total += self[serializer][_dataobj].encoding_strlen
            if output == "value":
                res = total
            if output == "formattedstr":
                res = SerializationResults._format_stringlength(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    serializer == self._get_serializers_base('encoding_strlen'),
                    100*total/self.total_encoding_strlen(
                        serializer=self._get_serializers_base('encoding_strlen'),
                        output="value"))

        else:
            if self.dataobjs_number == 0:
                return SerializationResults._format_stringlength(None)

            for _serializer in self:
                if self[_serializer][dataobj].encoding_strlen:
                    total += self[_serializer][dataobj].encoding_strlen
            if output == "value":
                res = total
            if output == "formattedstr":
                res = SerializationResults._format_stringlength(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    dataobj == self._get_dataobjs_base('encoding_strlen'),
                    100*total/self.total_encoding_strlen(
                        dataobj=self._get_dataobjs_base('encoding_strlen'),
                        output="value"))

        if res is None:
            raise WisteriaError("Internal error: the result could not be computed. "
                              f"{serializer=}; {dataobj=}; {output=};")
        return res

    def total_encoding_time(self,
                            serializer=None,
                            dataobj=None,
                            output="formattedstr"):
        """
            SerializationResults.

            Compute and format the total decoding time used by a <serializer>
            OR by a <dataobj>ect.

            _______________________________________________________________

            ARGUMENTS:
            o  <None|str>serializer: if not None, name of the serializer to be used.
            o  <None|str>dataobj: if not None, name of the data object to be used.
                BEWARE ! One and pnly one argument among <serializer> and <dataobj> can be set to
                         None.
            o  (str)output: output type and format
                    - "value": raw value (float)
                    - "formattedstr": formatted string (str)
                    - "base100": formatted string based on a "base 100" value (str)
            RETURNED VALUE: a formatted string representing the input argument.
        """
        assert serializer is None or dataobj is None

        res = None  # unexpected result !
        total = 0  # total time

        if serializer is not None:
            if self.serializers_number == 0:
                return SerializationResults._format_time(None)

            for _dataobj in self[serializer]:
                if self[serializer][_dataobj].encoding_success:
                    total += self[serializer][_dataobj].encoding_time
            if output == "value":
                res = total
            if output == "formattedstr":
                res = SerializationResults._format_time(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    serializer == self._get_serializers_base('encoding_time'),
                    100*total/self.total_encoding_time(
                        serializer=self._get_serializers_base('encoding_time'),
                        output="value"))

        else:
            if self.dataobjs_number == 0:
                res = SerializationResults._format_time(None)

            for _serializer in self:
                if self[_serializer][dataobj].encoding_success:
                    total += self[_serializer][dataobj].encoding_time
            if output == "value":
                res = total
            if output == "formattedstr":
                res = SerializationResults._format_time(total)
            if output == "base100":
                res = SerializationResults._format_base100(
                    dataobj == self._get_dataobjs_base('encoding_time'),
                    100*total/self.total_encoding_time(
                        dataobj=self._get_dataobjs_base('encoding_time'),
                        output="value"))

        if res is None:
            raise WisteriaError("Internal error: the result could not be computed. "
                              f"{serializer=}; {dataobj=}; {output=};")
        return res


class SerializationResult:
    """
        SerializationResult class

        Class used to store tests results in a SerializationResults object.

        _______________________________________________________________________

        o  __init__(self, encoding_success=False, encoding_time=None, encoding_strlen=None,
                    decoding_success=False, decoding_time=None, similarity=False)
        o  __repr__(self)
    """
    def __init__(self,
                 encoding_success=False,
                 encoding_time=None,
                 encoding_strlen=None,
                 decoding_success=False,
                 decoding_time=None,
                 similarity=False):
        """
            SerializationResult.__init__()
        """
        self.encoding_success = encoding_success
        self.encoding_time = encoding_time
        self.encoding_strlen = encoding_strlen
        self.decoding_success = decoding_success
        self.decoding_time = decoding_time
        self.similarity = similarity

    def __repr__(self):
        """
            SerializationResult.__repr__()
        """
        return f"{self.encoding_success=}; {self.encoding_time=}; {self.encoding_strlen=}; " \
            f"{self.decoding_success=}; {self.decoding_time=}; {self.similarity=}"


class SerializerData:
    """
        SerializerData class

        SerializerData are used to store infos. about serializers in the SERIALIZERS dict.

        _______________________________________________________________________

        o  __init__(self, human_name, internet, available, func)
        o  __repr__(self)
        o  checkup_repr(self)
    """
    def __init__(self,
                 human_name,
                 internet,
                 available,
                 func):
        """
            SerializerData.__init__()
        """
        self.human_name = human_name
        self.internet = internet
        self.available = available
        self.version = None
        self.func = func

    def __repr__(self):
        """
            SerializerData.__repr__()

            For the check up output, see .checkup_repr().
        """
        return f"{self.human_name=}; {self.internet=}; " \
            f"{self.available=}; {self.version=}; {self.func=}"

    def checkup_repr(self):
        """
            SerializerData.checkup_repr()

            Does the same as .__repr__() but for the check up output.
        """
        if self.available:
            return f"(available)     '{self.human_name}' ({self.version}), see {self.internet}."
        return f"(not available) '{self.human_name}' (see {self.internet})."


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
        raise WisteriaError(f"Unknown 'action' keyword '{action}'.")

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
        raise WisteriaError(f"Unknown 'action' keyword '{action}'.")

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


SERIALIZERS = {
    "iaswn": SerializerData(human_name="Iaswn",
                            internet="https://github.com/suizokukan/iaswn",
                            available=trytoimport("iaswn"),
                            func=serializer_iaswn),
    "jsonpickle": SerializerData(human_name="jsonpickle",
                                 internet="https://jsonpickle.github.io/",
                                 available=trytoimport("jsonpickle"),
                                 func=serializer_jsonpickle),
    }
for _serializer in SERIALIZERS:
    if SERIALIZERS[_serializer].available:
        SERIALIZERS[_serializer].version = SERIALIZERS[_serializer].func("version")

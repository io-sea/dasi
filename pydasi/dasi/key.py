# Copyright 2023 European Centre for Medium-Range Weather Forecasts (ECMWF)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from ._dasi_cffi import ffi, ffi_decode, ffi_encode, lib
from .utils import DEBUG, getLogger

logger = getLogger(__name__)
logger.setLevel(DEBUG)


class Key:
    """
    Container for keyword:value pairs.
    """

    def __init__(self, pair=None):
        if isinstance(pair, Key):
            self = pair.copy()
        elif isinstance(pair, ffi.CData):
            if ffi.typeof(pair) is ffi.typeof("dasi_key_t *"):
                self._cdata = pair
        else:
            self._new_key(pair)
            self.insert(pair)

    def __setitem__(self, keyword, value):
        lib.dasi_key_set(self._cdata, ffi_encode(keyword), ffi_encode(value))

    def __getitem__(self, keyword):
        value = ffi.new("const char **")
        lib.dasi_key_get(self._cdata, ffi_encode(keyword), value)
        return ffi_decode(value[0])

    def __delitem__(self, keyword):
        lib.dasi_key_erase(self._cdata, ffi_encode(keyword))

    def _new_key(self, pair=None):
        # allocate an instance
        ckey = ffi.new("dasi_key_t **")
        if isinstance(pair, str):
            lib.dasi_new_key_from_string(ckey, ffi_encode(pair))
        else:
            lib.dasi_new_key(ckey)
        # set the free function
        ckey = ffi.gc(ckey[0], lib.dasi_free_key)
        self._cdata = ckey

    @property
    def name(self):
        return "".join(
            "_" + c.lower() if c.isupper() else c
            for c in self.__class__.__name__
        ).strip("_")

    @staticmethod
    def key_class_name(name):
        return "".join(part[:1].upper() + part[1:] for part in name.split("_"))

    def insert(self, pair):
        if isinstance(pair, dict):
            # @todo 'value' can be dict
            for [keyword, value] in pair.items():
                self[keyword] = value

    def copy(self):
        return Key(self._cdata)

    def print(self, stream):
        raise NotImplementedError

    def has(self, keyword: str) -> bool:
        has = ffi.new("dasi_bool_t*", 1)
        lib.dasi_key_has(self._cdata, ffi_encode(keyword), has)
        return has[0] != 0

    def count(self) -> int:
        count = ffi.new("long*", 0)
        lib.dasi_key_count(self._cdata, count)
        return count[0]

    def clear(self):
        lib.dasi_key_clear(self._cdata)

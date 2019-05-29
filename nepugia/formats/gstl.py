# -*- coding: utf-8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015 Alex Headley <aheadley@waysaboutstuff.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from construct import *
from nepugia.common.construct import *

# The format of the string storage format (the *.gstr files). This is where
# the bulk of localization efforts would go, though there are localized strings
# in other files as well.
GSTLFormat = Struct(
    'header' / Struct(
        Const(b'GSTL'),

        Const(b'\x01\x00\x00\x00'),
        Const(b'\x10\x00\x00\x00'),
        Const(b'\x04\x00\x00\x00'),
        Const(b'\x01\x00\x00\x00'),
        Const(b'\x40\x00\x00\x00'),

        # number of str labels (ex: IDS_SOMETHING_OR_OTHER)
        # @0x18
        'label_count' / Int32ul,

        # these are always observed to be 12, and 3 (respectively), use is
        # unknown (year and month of creation maybe?)
        Const(b'\x0C\x00\x00\x00'),
        Const(b'\x03\x00\x00\x00'),

        # end of header maybe, of end of label list
        'end' / Int32ul,
        # total count of labels and strings
        'str_count' / Int32ul,
        # @0x2c
        'str_offset' / Int32ul,

        # 0x04 then zeros till @0x44
        Const(b'\x04\x00\x00\x00'),
        Padding(16),
    ),
    # @0x44
    Array(lambda ctx: ctx.header.label_count,
        'labels' / Struct(
            'id' / Int32ul,
            # starting offset of string
            'start_offset' / Int32ul,
            # ending offset of string
            # the final value will be 5 as a sentinal value or something
            'end_offset' / Int32ul,
            # note that this is a computed value and not present in the
            # on-disk structure, and because of the above note will not be
            # valid for the last item
            'v_length' / Computed(lambda ctx: ctx.end_offset - ctx.start_offset),
        )
    ),
    Padding(8),
    'a_strings_start' / Tell,
    Array(lambda ctx: ctx.header.str_count,
        # CString('strings')
        'strings' / Struct(
            'start_offset' / Tell,
            'v_relative_offset' / Computed(lambda ctx: ctx.start_offset - ctx._.a_strings_start),
            'value' / CString(type_strings),
            'end_offset' / Tell,
        )
    )
)

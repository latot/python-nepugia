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

def GBNLFormat(row_model=None):
    return Struct('gbnl',
        # note, footer struct size is 64
        Pointer(lambda ctx: -64,
            Struct('footer',
                'a_start' / Tell,
                Const('GBNL'),

                # # 0x01 00 00 00
                # Const(ULInt32('const_00'), 0x01),
                # # 0x10 00 00 00
                # Const(ULInt32('const_01'), 0x10),
                # # 0x04 00 00 00
                # Const(ULInt32('const_02'), 0x04),
                # # 0x01 00 00 00
                # Const(ULInt32('const_03'), 0x01),
                # # 0x00 00 00 00
                # Const(ULInt32('const_04'), 0x00),
                # Padding(20),

                Const('\x01\x00\x00\x00'),
                Const('\x10\x00\x00\x00'),
                Const('\x04\x00\x00\x00'),
                # this is 1 if there are strings at the end of the file, and 0
                # otherwise. not sure why since there is also a str_count field
                'has_strings_flag' /Int32ul,
                Const('\x00\x00\x00\x00'),

                # @0x18
                # possible string count?
                'row_count' / Int32ul,
                # @0x1c
                # seems to be row size
                'row_size' / Int32ul,
                # @0x20
                # this is the id of the model to use for the rows
                'row_model_id' / Int32ul,
                # @0x24
                # some other kind of offset
                'data_end_offset' / Int32ul,
                # @0x28
                # also possible string count
                # almost certainly string count
                'str_count' / Int32ul,
                # @0x2c
                # string offset start
                'str_offset' / Int32ul,

                'v_offset_diff' / Computed(lambda ctx: ctx.str_offset - ctx.data_end_offset),
                'v_expected_data_size' / Computed(lambda ctx: ctx.row_count * ctx.row_size),
                'v_data_size_diff' / Computed(lambda ctx: ctx.data_end_offset - ctx.v_expected_data_size),

                # # @0x30
                # Const(ULInt32('const_05'), 0x04),
                Padding(4),

                # all 0x00
                Padding(12),
            )
        ),

        Array(lambda ctx: ctx.footer.row_count,
            Struct('rows',
                Embedded(row_model),
                Padding(lambda ctx: max(0, ctx._.footer.row_size - row_model.sizeof()))
            ) if row_model is not None else Padding(lambda ctx: ctx.footer.row_size)
        ),

        # this seems to be garbage data between the end of the data and start of the
        # strings
        Padding(lambda ctx: max(0, ctx.footer.v_offset_diff + ctx.footer.v_data_size_diff)),

        'a_strings_start' / Tell,
        Array(lambda ctx: ctx.footer.str_count,
            # CString('strings')
            Struct('strings',
                'start_offset' / Tell,
                'v_relative_offset' / Computed(lambda ctx: ctx.start_offset - ctx._.a_strings_start),
                CString('value'),
                'end_offset' / Tell,
            )
        ),
        'a_strings_end' / Tell,
        # this seems to be garbage data between the end of the strings and the start
        # of the footer
        Padding(lambda ctx: ctx.footer.a_start - ctx.a_strings_end),

        'a_expected_footer_start' / Tell,
        # the footer struct would go here if we didn't need to parse it first

        'v_strings_db' / Computed(lambda ctx: {
            s.v_relative_offset: s.value \
            for s in ctx.strings
        }),
    )

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

from ..util.file_io import FileInFile

# The format of the packed file container. Nearly all game files are stored
# in side this container format.
PACFormat = 'pac' / Struct(
    'header' / Struct(
        Const(b'DW_PACK\0'),
        # this is a guess based on minor_id
        Const(0x00, 'major_id' / Int32ul),
        'entry_count' / Int32ul,
        # this seems to correlate to the sequential files, eg:
        # GAME00000.pac has 0 here
        # GAME00001.pac has 1 here
        'minor_id' / Int32ul,
    ),

    Array(lambda ctx: ctx.header.entry_count,
        'entries' / Struct(
            Const(b'\x00\x00\x00\x00'),
            'id' / Int32ul,
            'name' / String(260),
            Const(b'\x00\x00\x00\x00'),
            'stored_size' / Int32ul,
            'real_size' / Int32ul,
            # all files are compressed
            Const(1, 'compression_flag' / Int32ul),
            'offset' / Int32ul,

            If(lambda ctx: ctx.compression_flag,
                LazyField(Pointer(lambda ctx: ctx._.a_entry_list_end + ctx.offset,
                    'chunk_set' / Struct(
                        'header' / Struct(
                            # Const(b'\x34\x12\x00\x00'),
                            Const(0x1234, 'magic' / Int32ul),
                            'chunk_count' / Int32ul,
                            'chunk_size' / Int32ul,
                            'header_size' / Int32ul,
                        ),
                        Array(lambda ctx: ctx.header.chunk_count, 'chunks' / Struct(
                            'real_size' / Int32ul,
                            'stored_size' / Int32ul,
                            'offset' / Int32ul,

                            'vf_open' / Computed(lambda ctx: lambda handle:
                                FileInFile(handle, ctx._.header.header_size + ctx.offset,
                                    ctx.stored_size)),
                        )),
                        'a_chunk_list_end' / Tell,
                    ),
                )),
            ),

            'vf_open' / Computed(lambda ctx: lambda handle:
                FileInFile(handle, ctx._.a_entry_list_end + ctx.offset, ctx.stored_size)),
        )
    ),
    'a_entry_list_end' / Tell,
)

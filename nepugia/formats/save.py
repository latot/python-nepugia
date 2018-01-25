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
from nepugia.formats.gbnl_models import *

RB2_SAVFormat = 'rb2_sav' / Struct(
    'header' / Struct(
        'game_id' / Int16ul,
        'save_slot_id' / Int16ul,

        Padding(8),

        'save_count' / Int32ul,
        Padding(4),
        Const('\xD0\xB0\x0C\x00'),
        # only seems to be 3, 7, or 10
        'unknown_01' / Int32ul,
        'cursor_pos_x' / Float32l,
        'cursor_pos_y' / Float32l,

        # Padding(3784),
        Padding(3548),
        # @3584

        'game_stats' / Struct(
            Padding(60),

            'battle_count' / Int32ul,
            'kill_count' / Int32ul,
            # suspect one of these is per-cycle
            'cycle_kill_count' / Int32ul,
            'ko_count' / Int32ul,
            'escape_count' / Int32ul,
            'hdd_activation_count' / Int32ul,
            'max_damage_dealt' / Int32ul,
            'max_combo_dealt' / Int32ul,

            # always seems to be 0
            Padding(4),

            'total_damage_dealt' / Int32ul,

            Padding(4),

            'total_damage_taken' / Int32ul,

            Padding(12),
            Array(4, 'unknown_12' / Int32sl),

            'jump_count' / Int32ul,

            Padding(4),
            'unknown_14' / Int32ul,

            'rush_attack_count' / Int32ul,
            'power_attack_count' / Int32ul,
            'break_attack_count' / Int32ul,

            Array(5, 'unknown_15' / Int32sl),

            'credits_spent' / Int32ul,
            # Array(4, SLInt16('unknown_18')),
            Padding(8),
            'credits_gained' / Int32ul,
            Padding(4),
            'credits_spent2' / Int32ul,

            Padding(16),
            'quests_completed_count' / Int32ul,
            Padding(12),
        ),
        # Array(59, SLInt32('unknown_10')),

        # @3820
        'chapter_title' / CString(),
        Padding(lambda ctx: max(48 - (len(ctx.chapter_title)+1), 0)),
    ),

    Padding(20),

    # @3888
    Array(22, 'characters' / Struct(
        # struct total = 1288 bytes

        # this probably means something but i have no idea what
        # Array(4, 'unknown_10')),
        Padding(8),
        'name' / String(32, padchar='\x00'),

        'xp_total' / Int32ul,
        'unknown_22' / Int16ul,
        'level' / Int16ul,
        # Array(4, 'unknown_12')),
        Padding(8),
        # this is some kind of id, maybe in stcharaplayer
        'unknown_20' / Int32ul,
        'unknown_21' / Int32ul,
        # this and the sp seem to be the current values (i.e. could be lower
        # if saved in a dungeon, could be higher if at full health since it
        # includes equipment bonuses)
        'current_hp' / Int32ul,
        # seems to always be 0
        # 'unknown_23'),
        Padding(4),
        'current_sp' / Int32ul,
        # seems to always be 100 so not going to record it
        # 'unknown_25'),
        Padding(4),

        # these seem to be the base stats before equipment bonuses
        # unsure of order of agi/men/luk
        CharStats,

        Padding(20),
        'equipment' / Struct(
            'unknown_30' / Int32ul,

            'weapon_id' / Int32ul,
            'armor_id' / Int32ul,
            'bracelet_id' / Int32ul,
            'clothing_id' / Int32ul,
            'accessory_id' / Int32ul,

            'cpu_c_id' / Int32ul,
            'cpu_h_id' / Int32ul,
            'cpu_b_id' / Int32ul,
            'cpu_s_id' / Int32ul,
            'cpu_w_id' / Int32ul,
            'cpu_l_id' / Int32ul,
        ),

        Padding(1072),
    )),
    # @32224

    Padding(19564),
    # @51788
    'inventory' / Struct(
        'filled_slot_count' / Int32ul,
        Array(3000, 'slots' / Struct(
            'item_id' / Int16ul,
            'count' / Int8ul,
            'flags' / BitStruct(
                Padding(5),
                # this one seems exclusive to plans, but not all plans have it
                'bitflag_00' / Flag,
                # this seems to be related to dlc content
                'bitflag_01' / Flag,
                # all plans seem to have this, but is not exclusive to plans
                'bitflag_02' / Flag,
            ),
        )),

        # @63792
        'current_credits' / Int32ul,
    ),


    Padding(492532),

    # @556328
    # Array(2420, 'unknown_80')),
    Padding(4840),

    Padding(249432),

    # @810600
    # Array(334, 'unknown_70')),
    Padding(668),

    Padding(20396),

    # @831664
    'footer' / Struct(
        Const('\x01\x00\x00\x00'),
        Const('\x12\x32'),
        Const('\x50\x46'),
        Padding(8),
        Const('\xFF\xCB\xE5\x00'),
        Array(4, 'unknown_99' / Int16ul),
    ),

    Padding(4),
)

SAVSlotFormat = 'savslot' / Struct(
    Const('SAVE0001'),

    # there might be some meaning to this, but is probably specific to ps3/vita
    # maybe CRCs?
    Padding(32),
    Padding(4),

    'title' / String(64, padchar='\x00', encoding='shift-jis'),
    'progress' / String(128, padchar='\x00'),
    'status' / String(128, padchar='\x00'),

    Padding(384),

    'save_icon_path' / String(64, padchar='\x00'),
    Padding(8),

    'timestamp' / Struct(
        'year' / Int16ul,
        'month' / Int16ul,
        'day' / Int16ul,

        'hour' / Int16ul,
        'minute' / Int16ul,
        'second' / Int16ul,

        'unknown_00' / Int32ul,
    ),
)

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

# unsure of order of agi/men/luk
CharStats = Struct('stats',
    'hit_points' / Int32ul,
    Padding(4),
    'skill_points' / Int32ul,
    'strength' / Int32ul,
    'vitality' / Int32ul,
    'intelligence' / Int32ul,
    'mentality' / Int32ul,
    'agility' / Int32ul,
    'technique' / Int32ul,
    Padding(4),
    'luck' / Int32ul,
    'movement' / Int32ul,
    Padding(4),
    Struct('resist',
        'element_00' / Int32sl,
        'element_01' / Int32sl,
        'element_02' / Int32sl,
        'element_03' / Int32sl
    ),

    Pass
)

# row_size=292
ItemModel = Struct('item',
    # looks like some kind of bit field/flags
    'type' / Int32ul,
    # almost certainly some kind of id, maybe correlates to something else
    # like a foreign key
    'id' / Int32ul,
    # str offset? seems to start at 0 and increase every time
    'name_offset' / Int32ul,

    # observed as all 0x00
    Padding(134),
    # Const('\0' * 134),

    # @0x92
    # yes, 3 of the exact same values in a row
    'flags_00' / Int32ul,
    'flags_01' / Int32ul,
    'flags_02' / Int32ul,
    'flags_03' / Int32ul,

    # always 0
    Const('\x00\x00'),
    # small numbers, possibly levels
    'game_effect_00' / Int16ul,

    # only seems to be 0, 1, or 99
    'max_count' / Int16ul,
    # large numbers, buy price maybe?
    'game_effect_01' / Int16ul,

    # possibly a character/use mask, usually 0, sometimes small (odd) numbers
    'game_effect_02' / Int16ul,
    # large numbers, seems to always be less than game_effect_01
    'game_effect_03' / Int16ul,

    # observed as all 0x00
    Padding(110),
    # Const('\0' * 110),

    # seems to usually be 0, otherwise is less than 10
    'dynamic_05' / Int16ul,
    # possibly label ids
    'dynamic_06' / Int16ul,
    # possibly string offsets
    'desc_offset' / Int32ul,

    Pass
)

AbilityModel = ItemModel

CharaMonsterModel = Struct('charamonster',
    # flag field, use unknown
    'flag_00' / Int32ul,
    # this isn't certain, it seems to be unique but unconfirmed, and the rows
    # are completely in this order, it jumps around
    'id' / Int16ul,
    # use unknown, but numbers all seem to be low, generally less than 20
    'dynamic_01' / Int16ul,

    String('name', 32, padchar='\x00'),

    # always 0, except for CPUs/CPU candidate entries, where is small number
    'dynamic_10' / Int32ul,
    'flag_20' / Int16ul,
    # use unknown, numbers start small and increase slowly
    'dynamic_11' / Int16ul,
    Padding(2),
    # larger numbers, generally 300-400 ish, small variance
    'dynamic_12' / Int16ul,
    # very small numbers, less than 10
    'dynamic_13' / Int16ul,
    # usually 0, sometimes larger 200ish
    'dynamic_14' / Int16ul,

    # @56
    # observed as all 0x00
    Padding(24),

    CharStats,
    Padding(20),

    # @168
    # only cpus/candidates have these, possibly voice/event data? or something
    # with the cpu form
    'flag_10' / Int32ul,
    Array(11, 'dynamic_50' / Int32ul),

    Padding(152),

    # @368
    # this is not actually empty, just haven't decoded it yet
    Padding(116),

    # @484
    # observed as all 0x00 in ~10 samples
    Padding(736),

    # @1220
    # these always seem to be 0.07 and 0.15 respectively
    # not sure what the use is
    'fp_00' / Float32l,
    'fp_01' / Float32l,

    'dynamic_20' / Int32ul,
    'dynamic_21' / Int32ul,
    'dynamic_22' / Int32ul,
    'dynamic_23' / Int32ul,
    'stat_guard_points' / Int32ul,

    'drop_exp' / Int32ul,
    # @1252
    'drop_credits' / Int32ul,

    # these are a total guess/gut feeling, should be x/100
    'drop_chance_any' / Int32ul,
    'drop_chance_item_00' / Int32ul,
    'drop_chance_item_01' / Int32ul,
    'drop_chance_item_02' / Int32ul,

    # @0x04f8
    'drop_item_00' / Int32ul,
    'drop_item_01' / Int32ul,
    'drop_item_02' / Int32ul,
    Const('\x00' * 4),

    # Computed('v_drop_exp_bonus', lambda ctx: ctx.drop_exp * 1.3),

    Pass
)

RemakeModel = Struct('remake',
    'name_offset' / Int32ul,
    'id' / Int16ul,
    'category_id' / Int16ul,
    'plan_item_id' / Int16ul,
    'result_id' / Int16ul,

    'dynamic_00' / Int16ul,
    Padding(4),
    'dynamic_01' / Int16ul,
    'dynamic_02' / Int16ul,
    Padding(4),

    # @26
    'flag_10' / Int16ul,
    'flag_11' / Int32ul,
    Const('\x01'), Padding(3),

    'dynamic_10' / Int16ul,
    'dynamic_11' / Int16ul,
    'dynamic_12' / Int16ul,
    'dynamic_13' / Int16ul,

    # @44
    Array(3,
        Struct('components',
            'item_id' / Int16ul,
            'count' / Int16ul
        )
    ),
    Padding(8),

    # @64
    'dynamic_20' / Int32ul,
    'dynamic_21' / Int32ul,
    'dynamic_22' / Int32ul,
    'dynamic_23' / Int32ul,
    Padding(16),

    # @96
    'dynamic_30' / Int32ul,
    'dynamic_31' / Int32ul,
    'author_offset' / Int32ul,
    'desc_offset' / Int32ul,

    Pass
)

TreasureModel = Struct('treasure',
    'id' / Int32ul,
    Array(3, Struct('item',
        'id' / Int32ul,
        'drop_chance' / Int32ul,
        'flag_00' / Int32ul,
        'flag_01' / Int32ul
    )),

    Pass
)

DungeonModel = Struct('dungeon',
    'id' / Int16ul,
    # this is related to the environment of the dungeon in some way
    'env_effect_00' / Int16ul,
    Padding(6),
    # also related to the environment of the dungeon somehow, guessing the icon
    # based on what it's shared with
    'icon_id' / Int16ul,
    # the world map seems to use a coordinate system of:
    #  x=left<>right [0,~1600]
    #  y=top<>bottom [0,~1600]
    'map_pos_x' / Int32ul,
    'map_pos_y' / Int32ul,
    # always seems to be a multiple of 100
    'dynamic_02' / Int16ul,
    'dynamic_03' / Int16ul,

    # @24
    'name_offset' / Int32ul,

    'dynamic_10' / Int16ul,
    'dynamic_11' / Int16ul,
    'dynamic_12' / Int16ul,
    Padding(18),

    # @52
    Array(10, 'dynamic_41' / Int32ul),
    Array(5, Struct('treasure_boxes',
        'id' / Int32ul,
        Array(3, Struct('drops',
            'item_id' / Int32ul,
            'drop_chance' / Int32ul,
            'flag_00' / Int32ul,
            'flag_01' / Int32ul,
        ))
    )),

    # @352
    # array totals 4860 bytes
    # [0]= regular
    # [1]= +add enemies
    # [2]= +change dungeon
    Array(3, Struct('monster_spawn_sets',
        Array(15, Struct('monster_spawns',
            # always 0x01 00
            Padding(2),
            'dynamic_23' / Int16ul,
            Padding(2),

            # Array(28, ULInt16('dynamic_20')),
            Padding(56),

            Array(4, Struct('monsters',
                'id' / Int16ul,
                'dynamic_21' / Int16ul,
                'dynamic_22' / Int16ul,
                Padding(2)
            )),
            # always 0x00
            Padding(14)
        ))
    )),

    # @5212
    # array totals 2340 bytes
    Array(3, Struct('unknown_block_01',
        Array(65, 'dynamic_30' / Int32ul),
        Padding(520)
    )),
    'dynamic_99' / Int32ul,
    Padding(16),

    Pass
)

QuestModel = Struct('quest',
    'id' / Int32ul,
    'name_offset' / Int32ul,

    BitStruct('type_flags',
        # there are quite a few flags in here that i am ignoring
        Padding(5),
        Flag('non_repeatable'),
        Flag('request_kill'),
        Flag('request_item'),

        Padding(8),

        Pass
    ),
    Padding(2),

    Array(4, Struct('request_objects',
        'id' / Int32ul,
        'count' / Int32ul,

        Pass
    )),

    # @44
    'reward_credits' / Int32ul,
    # i have no idea what this is used for, at all
    'dynamic_10' / Int8ul,
    Padding(3),

    Array(3, Struct('rewards',
        'id' / Int32ul,
        'count' / Int32ul,

        Pass
    )),

    # @76
    # faction IDs:
    #   0:  Planeptune
    #   1:  Leanbox
    #   2:  Lastation
    #   3:  Lowee
    #   4:  Arfoire/Others (the bad guys)
    'rep_gain_faction_id' / Int8ul,
    'rep_loss_faction_id' / Int8ul,
    'rep_flux_value' / Int16ul,

    # this only seems to be used for colliseum quests
    'dungeon_id' / Int16ul,
    'dynamic_30' / Int16ul,
    'dynamic_31' / Int16ul,
    'dynamic_32' / Int16ul,
    Padding(8),

    # @96
    # there is more colliseum-only data in here concerning the enemy monsters
    Padding(96),

    # @192
    'sponser_offset' / Int32sl,
    'client_offset' / Int32sl,
    'comment_offset' / Int32sl,

    Pass
)

AvatarModel = Struct('avatar',
    'id' / Int16ul,

    # this seems to be an id to another table (foreign key), or maybe a
    # sprite/model id
    'dynamic_00' / Int16ul,

    'name_offset' / Int32ul,

    # these appear to be related to whether the avatar is actually a character
    # or a system thing (like "Guild", "Shop", etc)
    'dynamic_10' / Int32ul,
    'dynamic_11' / Int32ul,

    'alt_name_offset' / Int32ul,

    Pass
)

AvatarMessageModel = Struct('avtmsg',
    'id' / Int32ul,

    # this is bizzare. it's always -1, except for a single row where it is the
    # offset to a single character string ("1")
    'one_offset' / Int32sl,

    Array(5, 'message_offsets' / Int32ul),

    'dynamic_10' / Int32ul,
    Padding(16),

    # @48
    Array(3, Struct('rewards',
        # this is probably not actually the count, since it would mean multiple
        # copies of plans are given
        'count' / Int32ul,
        'item_id' / Int32ul,

        Pass
    )),

    Pass
)

AvatarDecModel = Struct('avtdec',
    Array(4, Struct('unknown_block_00',
        'dynamic_00' / Int32ul,
        'dynamic_01' / Int32ul,
        'dynamic_02' / Int32ul,
        'dynamic_03' / Int32ul,
        'dynamic_04' / Int32sl,

        Pass
    )),

    'dynamic_10' / Int32ul,
    'dynamic_11' / Int32ul,
    'dynamic_12' / Int32ul,
    # this is almost always 9 except for a few special cases
    'dynamic_13' / Int32ul,
    'avatar_id' / Int32sl,

    # this definitely seems to be some kind of ID but is probably not the
    # primary key
    'avtmsg_id' / Int32ul,
    'map_pos_x' / Int16ul,
    'map_pos_y' / Int16ul,
    'required_item_id' / Int32ul,

    Pass
)

ROW_MODELS = {
    'none':         None,
    'character':    CharStats,
    'ability':      AbilityModel,
    'item':         ItemModel,
    'charamonster': CharaMonsterModel,
    'remake':       RemakeModel,
    'treasure':     TreasureModel,
    'dungeon':      DungeonModel,
    'quest':        QuestModel,
    'avatar':       AvatarModel,
    'avtmsg':       AvatarMessageModel,
    'avtdec':       AvatarDecModel,
}

# MODEL_ID_MAP = {
#     2:          MuseumModel,
#     3:          SQStoneSkillModel,
#     4:          NepupediaModel,
#     6:          DiscCombiModel,
#     7:          AvatarModel,
#     9:          BattleAiModel,
#     12:         DiscItemModel,
#     14:         BlogModel,
#     15:         GalleryModel,
#     16:         MotionPortraitModel,
#     19:         HelpModel,
#     20:         AreaModel,
#     23:         CharaLevelUpModel,
#     28:         AvatarMessageModel,
#     45:         RemakeModel,
#     68:         QuestModel,
#     86:         SkillModel,
#     113:        AbilityModel,
#     341:        CharaMonsterModel,
#     666:        SQDungeonModel,
#     2533:       DungeonModel,
# }

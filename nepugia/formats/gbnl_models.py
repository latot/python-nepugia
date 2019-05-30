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


#Note, all strings use at end of b'\x00\x00'

from construct import *
from nepugia.common.construct import *

#Start in system_db 60

CharStats = 'stats' / Struct(
    'hit_points' / Int32sl, #HP
    'unknown_1' / Int32sl, # AP -- Maybe Ability Points
    'skill_points' / Int32sl, # SP
    'strength' / Int32sl, #STR
    'vitality' / Int32sl, #VIT
    'intelligence' / Int32sl, #INT
    'mentality' / Int32sl, #MEN
    'agility' / Int32sl, #AGI
    'technique' / Int32sl, #TEC
    'unknown_2' / Int32sl, # ADV
    'luck' / Int32sl, #LUK
    'movement' / Int32sl, #MOV
    'resist' / Struct(
        'neutral' / Int32sl,
        'fire' / Int32sl,
        'ice' / Int32sl,
        'wind' / Int32sl,
        'lightning' / Int32sl,
        'slice' / Int32sl,
        'blunt' / Int32sl,
        'pierce' / Int32sl,
        'bullet' / Int32sl,
        'beam' / Int32sl
    )
)

# row_size=292
ItemModel = 'item' / Struct(
    Peek(Array(300, 's' / Int8ul)),
    # looks like some kind of bit field/flags
    'type' / Int32ul,

    # almost certainly some kind of id, maybe correlates to something else
    # like a foreign key
    'id' / Int32ul,
    # str offset? seems to start at 0 and increase every time
    'name_offset' / Int32ul,

    # observed as all 0x00
    #Padding(134),
#    'unknown_' / Peek(RawCopy(Bytes(137))),
    Array(150, 'unknown' / Int8ul),
    # Const(b'\0' * 134),

    # @0x92
    # yes, 3 of the exact same values in a row

#    'flags_00' / Int32ul,
#    'flags_01' / Int32ul,
#    'flags_02' / Int32ul,
#    'flags_03' / Int32ul,

    # always 0
    #Const(b'\x00\x00'),
    Padding(2),

    # Start in 195 in system_db
    # Maybe '-' means Null, or the first text is excluded, 0 exclude the text options
    # type_item
    #@164
    # 0 - Unknown/Null
    # 1 - Katanas (Neptune)
    # 2 - Broadswords (Neptune)
    # 3 - Spears (Vert)
    # 4 - Short Swords (Noire)
    # 5 - Hammers (Blanc)
    # 6 - Beam Swords (Nepgear)
    # 7 - Rifles (Uni)
    # 8 - Staffs (Rom)
    # 9 - Staffs (Ram)
    # 12 - Syringes (Compa)
    # 13 - Qatars (IF)
    # 19 - Swords (Falcom)
    # 20 - Staffs (MAGES)
    # 21 - Dual Blades (CyberConnect2)
    # 22 - Gemas (Broccoli)
    # 23 - Swords (MarvelousAQL)
    # 24 - Gloves (Tekken)
    # 33 - Armor
    # 34 - Ornament
    # 35 - Costume
    # 36 - Accessory
    # 37 - Processor Unit C
    # 38 - Processor Unit H
    # 39 - Processor Unit B
    # 40 - Processor Unit S
    # 41 - Processor Unit W
    # 42 - Processor Unit L
    # 43 - Item Tools
    # 44 - Item Materials
    # 46 - Item Keys
    # 47 - Plans
    # 48 - Idea chip yellow
    # 49 - Blue
    # 50 - Red
    # 51 - Item Keys Gifts

    'type_item' / Int16ul,

    # only seems to be 0, 1, or 99
    'max_count' / Int16ul,
    'buy price' / Int32ul,
    'sell_price' / Int32ul,

    CharStats,

    # not decodded yet
    # Padding(44),
#    'unknown_44' / RawCopy(Bytes(42)),
    Array(20, 'unknown_44' / Int8ul),

    'chip_level' / Int16ul,

    # This can be:
    # Weapons - Initial Attack - Skill
    # Idea Chips - Ability
    # Consumables - Skill
    'ability' / Int16ul,

    # description offset
    'desc_offset' / Int32ul,
)

CharaMonsterModel = 'charamonster' / Struct(
    # flag field, use unknown
    'flag_00' / Int32ul,

    # this isn't certain, it seems to be unique but unconfirmed, and the rows
    # are completely in this order, it jumps around
    'id' / Int16ul,

    # Type of monster
    # Start in system_db 83
    'type' / Int16ul,

    'name' / PaddedString(32, type_strings),

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
    'unknown' / Int32ul,

    # Value('v_drop_exp_bonus', lambda ctx: ctx.drop_exp * 1.3),
)

RemakeModel = 'remake' / Struct(
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
    Padding(4),

    'dynamic_10' / Int16ul,
    'dynamic_11' / Int16ul,
    'dynamic_12' / Int16ul,
    'dynamic_13' / Int16ul,

    # @44
    Array(3,
        'components' / Struct(
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
    'desc_offset' / Int32ul
)

TreasureModel = 'treasure' / Struct(
    'id' / Int32ul,
    Array(3, 'item' / Struct(
        'id' / Int32ul,
        'drop_chance' / Int32ul,
        'flag_00' / Int32ul,
        'flag_01' / Int32ul
    )),

    Pass
)

DungeonModel = 'dungeon' / Struct(
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
    # Search this 10 in sttreasure.gbin
    Array(10, 'treasure_boxes' / Int32ul),
    Array(5, 'hidden_treasure_boxes' / TreasureModel),

    # @352
    # array totals 4860 bytes
    # [0]= regular
    # [1]= +add enemies
    # [2]= +change dungeon
    Array(3, 'monster_spawn_sets' / Struct(
        Array(15, 'monster_spawns' / Struct(
            # always 0x01 00
            Padding(2),
            'dynamic_23' / Int16ul,
            Padding(2),

            # Array(28, ULInt16('dynamic_20')),
            Padding(56),

            Array(4, 'monsters' / Struct(
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
    # Gathering with Change-Items Off
    Array(10, 'gathering_off' / TreasureModel),

    Padding(520),

    # Gathering with Change-Items On
    Array(5, 'gathering_on' / TreasureModel),

    Padding(520),

    'dynamic_99' / Int32ul,
    Padding(16),

    Pass
)

QuestModel = 'quest' / Struct(
    'id' / Int32ul,
    'name_offset' / Int32ul,

    'type_flags' / BitStruct(
        # there are quite a few flags in here that i am ignoring
        Padding(5),
        'non_repeatable' / Flag,
        'request_kill' / Flag,
        'request_item' / Flag,

        Padding(8),

        Pass
    ),
    Padding(2),

    Array(4, 'request_objects' / Struct(
        'id' / Int32ul,
        'count' / Int32ul,

        Pass
    )),

    # @44
    'reward_credits' / Int32ul,
    # i have no idea what this is used for, at all
    'dynamic_10' / Int8ul,
    Padding(3),

    Array(3, 'rewards' / Struct(
        'id' / Int32ul,
        'count' / Int32ul,

        Pass
    )),

    # @76
    # Start in 22 in system_db
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

AvatarModel = 'avatar' / Struct(
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

AvatarMessageModel = 'avtmsg' / Struct(
    'id' / Int32ul,

    # this is bizzare. it's always -1, except for a single row where it is the
    # offset to a single character string ("1")
    'one_offset' / Int32sl,

    Array(5, 'message_offsets' / Int32ul),

    'dynamic_10' / Int32ul,
    Padding(16),

    # @48
    Array(3, 'rewards' / Struct(
        # this is probably not actually the count, since it would mean multiple
        # copies of plans are given
        'count' / Int32ul,
        'item_id' / Int32ul,

        Pass
    )),

    Pass
)

AvatarDecModel = 'avtdec' / Struct(
    Array(4, 'unknown_block_00' / Struct(
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

CharaPlayerModel = 'charaplayer' / Struct(
    # flag field, use unknown
    'flag_00' / Int32ul,

    # this seems to be an id, and the level up data is constructed with it reading the file stcharalevelup + id
    'id' / Int16ul,
    'dynamic_01' / Int16ul,

    'name' / PaddedString(32, type_strings),

    # 1248 from here to end
    # Padding(40),
    Array(20, 'unknown_01' / Int16ul),
#    'unknown_01' / RawCopy(Bytes(40)),
    CharStats,
    Array(560, 'unknown_02' / Int16ul)
#    Padding(1140)
#    'unknown_02' / RawCopy(Bytes(148)),
#    'weapon' / Int16ul,
#    'unknown_03' / RawCopy(Bytes(990)),

)

## Lets think for now both have the same structure
CharaPlayerModel = CharaMonsterModel

# Sorted by row, every row seems to be the amount added to the skill from one level to the next,
# sorted from rows 0 to 97, how start at lvl 2 match from lvl 2 to 99
CharaLevelUpModel = 'charalevelup' / Struct(
    'unknown_01' / Int32ul,
    CharStats
)

SubEffect = Struct(
    'value' / Int32sl,
    #This maybe is the chance to activate the effect
    'unknown' / Int32sl
)

#size of 240
SkillModel = 'skill' / Struct(
    'id' / Int16ul,
    'unknown_01' / Int16ul,
    'name_offset' / Int32ul,
#    'unknown' / RawCopy(Bytes(228)),
    Array(4, 'unknown_02' / Int16ul),
    'sp_cost' / Int16ul,
    'exe_cost' / Int16ul,
    # Seems to be lily_rank for special skills, and cp_cost for combos
    'lily_rank' / Int16ul,
    Array(3, 'unknown_022' / Int8ul),

    # Start in 172 in system_db
    # 0 - Rush Combo
    # 1 - Power Combo
    # 2 - Break Combo
    # 3 - SP Attack
    # 4 - Defense Skill
    # 5 - Heal Skill
    # 6 - EXE Drive
    # 7 - Assist Attack
    # 8 - Support
    # 9 - Formation Skill
    # 10 - Coupling Skill
    # 11 - Special Skill
    # 12 - Item Consumable
    'type' / Int8ul,

    # Start in 186 in system_db

    # 0 - Phys. Attack
    # 1 - Mag. Attack
    # 2 - Phys. Link
    # 3 - Mag. Link
    # 4 - Heal
    # 5 - Revive
    # 6 - Assist
    # 7 - Repop (Taboo Staff, Dungeon)
    # 8 - Escape (Eject Button, Dungeon)
    'category' / Int8ul,

    # Start in 48 in system_db
    # 0 - Neutral
    # 1 - Fire
    # 2 - Ice
    # 3 - Wind
    # 4 - Lightning
    'affinity' / Int8ul,

    Array(1, 'unknown_03' / Int16ul),
    'range' / Int16ul,

    # in circular effect is radius
    # in square map location is an id (or codded data) of the affected squares
    'scope' / Int8ul,
    # 0 - Square Map Location
    # 128 (10000000) - Circular Effect (Maybe just read the first bit)
    'scope_type' / Int8ul,

    Array(2, 'unknown_04' / Int8ul),
    'hit_count' / Int16ul,
    'power' / Int16ul,
    Array(5, 'unknown_05' / Int16ul),
    'guard_damage' / Int16ul,    
    'unknown_06' / Int32ul,

    #"100: b'Poison'"
    #"101: b'Paralysis'"
    #"102: b'Seal'"
    #"103: b'Healing'"
    #"104: b'Virus'"
    #"105: b'STR'"
    #"106: b'VIT'"
    #"107: b'INT'"
    #"108: b'MEN'"
    #"109: b'AGI'"
    #"110: b'TEC'"
    #"111: b'AVD'"
    #"112: b'LUK'"
    #"113: b'MOV'"
    #"114: b'Neutral Resist'"
    #"115: b'Fire Resist'"
    #"116: b'Ice Resist'"
    #"117: b'Wind Resist'"
    #"118: b'Lightning Resist'"

    'effect' / Struct(
        'Poison' / SubEffect,
        'Paralysis' / SubEffect,
        'Seal' / SubEffect,
        'Healing' / SubEffect,
        'Virus' / SubEffect,
        'STR' / SubEffect,
        'VIT' / SubEffect,
        'INT' / SubEffect,
        'MEN' / SubEffect,
        'AGI' / SubEffect,
        'TEC' / SubEffect,
        'AVD' / SubEffect,
        'LUK' / SubEffect,
        'MOV' / SubEffect,
        'Neutral_Resist' / SubEffect,
        'Fire_Resist' / SubEffect,
        'Ice_Resist' / SubEffect,
        'Wind_Resist' / SubEffect,
        'Lightning_Resist' / SubEffect
    ),

    'player' / Int16ul,
    'level' / Int16ul,
    Array(2, 'unknown_08' / Int16ul),
    # Only with Coupling Skills, maybe has length 6, sorting the formation in Player1 Partner1 Player2 Partner2 Player3 Partner3
    Array(5, 'coupling_player' / Int16ul),
    Array(5, 'unknown_09' / Int16ul), 
    'desc_offset' / Int32ul
)

AbilityModel = ItemModel

DiscItemModel = 'diskitem' / Struct(
    'name' / PaddedString(40, type_strings),
    'id' / Int16ul,
    'yellow_chip' / Int16ul,
    'blue_chip' / Int16ul,
    'red_chip' / Int16ul,
    Array(4, 'unknown' / Int16ul),
    #Const(b'\x00' * 8),
    'desc_offset' / Int32ul
)

BlogModel = 'blog' / Struct(
    'id' / Int32ul,
    Array(13, 'unknown' / Int32ul)
)

SkillScopeModel = 'skillscope' / Struct(
    'id' / Int8ul,
#    Array(1, 'u' / Int8ul),
#    Array(28, 'unknown' / Int8ul),
#    'scope' / Bytes(31)
#    Array(2, 'v' / Int8ul)
    Array(31, ('unknown' / Int8ul))
)

BattleAIModel = 'battleai' / Struct(
    'id' / Int32ul,
    Array(8, 'unknown' / Int32ul)
)

ROW_MODELS = {
    'none':         None,
    'stats':        CharStats,
    'ability':      AbilityModel,
    'item':         ItemModel,
    'charamonster': CharaMonsterModel,
    'charaplayer':  CharaPlayerModel,
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

from enum import IntEnum


# Values should be ints for efficient lookup in sets
class TileAttribute(IntEnum):
    Road = 0
    Water = 1

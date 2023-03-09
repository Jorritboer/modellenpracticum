from enum import Enum


# Values should be ints for efficient lookup in sets
class TileAttribute(Enum):
    Road = 0
    Water = 1

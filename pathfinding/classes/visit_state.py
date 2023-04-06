from enum import IntEnum


class VisitState(IntEnum):
    Undiscovered = 0
    Discovered = 1
    Visited = 2

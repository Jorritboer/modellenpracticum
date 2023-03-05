from enum import Enum


class VisitState(Enum):
    Undiscovered = "Undiscovered"
    Discovered = "Discovered"
    Visited = "Visited"

from .grid import Grid
from .rect import Rect
from .point import Point
from .tile_data import TileData

from random import randint
from math import inf
def main(no_routes:int = 2, radius:int = 3, multiplier:int=10):
    grid = Grid(Rect(100,100))
    for i in range(100):
        for j in range(100):
            weight = 3
            grid.register_tile_at(Point(i,j),TileData(weight= 500 if i==j else randint(0,50)))
    first_route = grid.find_path(Point(0,0), Point(99,99))
    
    for point in first_route[5:len(first_route)-5]:
        tile = grid.tile_data_at(point)
        tile.weight = tile.weight * multiplier
    
    
    second_path = grid.find_path(Point(0,0), Point(99,99))
    print(second_path)
    return
main()
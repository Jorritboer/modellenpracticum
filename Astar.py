import math
import numpy as np
import queue
class Point:
    def __init__(self,x:int,y:int) -> None:
        self.x = x
        self.y = y
        pass

    def __str__(self):
        return str((self.x,self.y))

def clamp(value, min, max):
    return math.min(math.max(value, min), max)

class Tile:
    def __init__(self,weight: int, pos: Point) -> None:
        self.weight = weight
        self.pos = pos
        self.visited = False
        self.parent = None
        pass
    
    def neighbours(self, grid):
        return [grid.tiles[x, y] for x in range(max(self.pos.x-1,0),min(self.pos.x+2,grid.width)) for y in range(max(self.pos.y-1,0),min(self.pos.y+2,grid.height))]
    
    def h(self, end) -> int:
        return distsq(self.pos, end.pos)
    
    def __lt__(self, other):
        return True

    def __repr__(self):
        return str(self.pos)
    
    def __str__(self):
        return str(self.pos)



class Grid:
    def __init__(self,width: int, height:int, lengthcost: int) -> None:
        self.tiles = np.array([[Tile((i==j)*555, Point(i,j)) for i in range(width)] for j in range(height)])
        self.width = width
        self.height = height
        self.lengthcost = lengthcost #Scalar multiplied by length to increase cost for longer cables
        pass

    
    
    
def distsq(p1: Point, p2: Point) -> int:
    return (p1.x-p2.x)**2 + (p1.y-p2.y)**2

def path(tile: Tile, arr = []):
    if tile.parent == None:
        arr.insert(0,tile)
        return arr
    arr.insert(0, tile)
    return path(tile.parent, arr) 

def Astar(grid: Grid, start: Tile, end: Tile, maxLength: int):
    hinitial = start.h(end)
    to_visit = queue.PriorityQueue()
    visited = list()

    to_visit.put((start.h(end) +start.weight, start,0))
    while True:
        if len(to_visit.queue) == 0:
            print("NO PATH FOUND")
            break
        _, s_tile, length = to_visit.get()
         
        if s_tile == end:
            print(path(s_tile))
            return path(s_tile)
        if(s_tile.visited or length >= maxLength):
            continue
        s_tile.visited = True
        new_tiles = s_tile.neighbours(grid)
        for c_tile in new_tiles:
            if not c_tile.visited and c_tile not in [y for (x,y,z) in to_visit.queue]:
                c_tile.parent = s_tile
                to_visit.put((c_tile.weight+ c_tile.h(end)+(length+1)*grid.lengthcost, c_tile, length +1))
            elif c_tile in to_visit.queue:
                if c_tile.h(end) < min([x[0] for x in to_visit.queue if x[1] == c_tile]):
                    c_tile.parent = s_tile
                    to_visit.put((min([x[0] for x in to_visit.queue if x[1] == c_tile]) + grid.lengthcost, c_tile, length +1))
    
    return

def main(grid: Grid):
    Astar(grid, grid.tiles[0,0], grid.tiles[2,2],1) 
    return 0
main(Grid(20,20,3))


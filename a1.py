#!/usr/bin/env python3

"""The quick example from the README"""


from gdpc import Editor, Block
from gdpc import geometry as geo
import numpy as np

editor = Editor(buffering=True)
buildArea = editor.getBuildArea()  # BUILDAREA
STARTX, STARTY, STARTZ = buildArea.begin
LASTX, LASTY, LASTZ = buildArea.last

print(f"Start: {STARTX, STARTY, STARTZ}")
print(f"Last: {LASTX, LASTY, LASTZ}")

# Get a block
block = editor.getBlock((STARTX, STARTY, STARTZ))

# Place a block
editor.placeBlock((LASTX, STARTY, LASTZ), Block("stone"))


def buildRoof(start, end):

    #geo.placeCuboid(editor, start, (end[0],end[1]+1,end[2]), Block("stone"))

    for i in range(0, ((end[0]-start[0])//2)+1):        
        geo.placeCuboid(editor, (start[0]+i,start[1]+i, start[2]), (start[0]+i,start[1]+i,end[2]), Block("stone"))


    for i in range(0, ((end[0]-start[0])//2)+1):
        geo.placeCuboid(editor, (end[0]-i,end[1]+i, start[2]), (end[0]-i,end[1]+i,end[2]), Block("stone"))
    
    
    # for x in range(start[0], end[0]//2):
    #     for y in range(start[1], end[0]//2):
    #         if x==y:
    #             geo.placeCuboid(editor, (x,y,start[2]),(x,y,end[2]), Block("stone"))



def buildSingleFloorAndRoof(start: tuple):
    building_y = np.random.randint(5, 12)
    building_x = np.random.randint(5, 12)
    building_z = np.random.randint(5, 12)
    end = (start[0]+building_x, start[1]+building_y, start[2]+building_z)

    geo.placeCuboidHollow(editor, start, end, Block("oak_planks"))

    buildRoof(start=(start[0], start[1]+building_y+1, start[2]),
              end=(end[0], end[1]+1, end[2]))

buildSingleFloorAndRoof((STARTX, STARTY, STARTZ))





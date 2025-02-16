#!/usr/bin/env python3

"""The quick example from the README"""


from gdpc import Editor, Block
from gdpc import geometry as geo
import numpy as np
import random

editor = Editor(buffering=True)
buildArea = editor.getBuildArea()  # BUILDAREA
editor.loadWorldSlice(cache=True)
heightmap = editor.worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
print(heightmap[0,0])

STARTX, STARTY, STARTZ = buildArea.begin
LASTX, LASTY, LASTZ = buildArea.last

print(f"Start: {STARTX, STARTY, STARTZ}")
print(f"Last: {LASTX, LASTY, LASTZ}")



def solidBlock(block_coords: tuple):
    block = editor.getBlock(block_coords)
    if block.id != "minecraft:air"\
        and "leaves" not in block.id\
        and block.id not in ["minecraft:tall_grass", "minecraft:grass"]:
        return True
    else:
        return False

def getHighestOverlappingTerrainBlock(floor_start: tuple, floor_end: tuple): 
    #find colliding terrain tile with the highest y coord
    highest_terrain_block = floor_start

    for x in range((floor_end[0]+floor_start[0])//2, (floor_end[0]+floor_start[0])//2 +1):
        for z in range((floor_end[2]+floor_start[2])//2, (floor_end[2]+floor_start[2])//2):
            print(f"Checking {x,z}")
            if editor.getBlock((x, floor_start[1], z)).id != "minecraft:air"\
                and "leaves" not in editor.getBlock((x, floor_start[1], z)).id\
                and editor.getBlock((x, floor_start[1], z)).id not in ["minecraft:tall_grass", "minecraft:grass"]:
                checkAbove = True
                current_y = floor_start[1]
                while checkAbove:
                    current_y+=1
                    blockAbove = editor.getBlock((x, current_y, z))
                    if blockAbove.id == "minecraft:air"\
                        or "leaves" in editor.getBlock((x, floor_start[1], z)).id\
                        or editor.getBlock((x, floor_start[1], z)).id in ["minecraft:tall_grass", "minecraft:grass"]:
                        if current_y>highest_terrain_block[1]:
                            highest_terrain_block = (highest_terrain_block[0], current_y, highest_terrain_block[2])
                        checkAbove = False
                
    return highest_terrain_block  

def buildRoof(start, end):

    #geo.placeCuboid(editor, start, (end[0],end[1]+1,end[2]), Block("stone"))

    for i in range(0, ((end[0]-start[0])//2)+1):        
        geo.placeCuboid(editor, (start[0]+i,start[1]+i, start[2]), (start[0]+i,start[1]+i,end[2]), Block("oak_planks"))


    for i in range(0, ((end[0]-start[0])//2)+1):
        geo.placeCuboid(editor, (end[0]-i,end[1]+i, start[2]), (end[0]-i,end[1]+i,end[2]), Block("oak_planks"))
    
def buildSupportBeam(corner_block: tuple):
    check_solid_below = True
    current_y = corner_block[1]
    while check_solid_below:
        current_y-= 1
        if solidBlock((corner_block[0], current_y, corner_block[2])):
            check_solid_below = False
        else:
            editor.placeBlock((corner_block[0], current_y, corner_block[2]), Block("minecraft:birch_planks"))

def getRandomDoor():
    door_ids = ["minecraft:oak_door", "minecraft:birch_door",\
               "minecraft:jungle_door", "minecraft:dark_oak_door", \
                "minecraft:acacia_door"]
    return door_ids[np.random.randint(0, len(door_ids))]

def getRandomGlassPane():
    pane_ids = ["minecraft:lime_stained_glass_pane", "minecraft:lime_stained_glass_pane",\
               "minecraft:glass_pane", "minecraft:pink_stained_glass_pane",\
                "minecraft:blue_stained_glass_pane", "minecraft:yellow_stained_glass_pane"]
    return pane_ids[np.random.randint(0, len(pane_ids))]

def buildSingleFloorAndRoof(start: tuple):
    building_ydim = np.random.randint(5, 10)
    building_xdim = np.random.randint(4, 10)
    building_zdim = np.random.randint(4, 10)
    building_xdim, building_ydim, building_zdim = 4,4,4
    end = (start[0]+building_xdim, start[1]+building_ydim, start[2]+building_zdim)

    highest_terrain_y = getHighestOverlappingTerrainBlock(start, end)[1]
    corner1 = (start[0], highest_terrain_y, start[2])
    corner4 = (end[0], highest_terrain_y+building_ydim, end[2])
    corner2 = (corner1[0]+building_xdim, corner1[1], corner1[2])
    corner3 = (corner1[0], corner1[1], corner1[2]+ building_zdim)
    corners = [corner1, corner2, corner3, corner4]
    wall_corners_pairs = [[corner1, corner2],
                        [corner1, corner3],
                        [corner2, corner4],
                        [corner3, corner4]]

    for corner in corners:
        buildSupportBeam(corner)

    geo.placeCuboidHollow(editor, corner1, corner4, Block("stone"))

    buildRoof(start=(corner1[0], corner1[1]+building_ydim+1, corner1[2]),
              end=(corner4[0], corner4[1]+1, corner4[2]))
    
    first_door_wall = wall_corners_pairs[np.random.randint(0, len(wall_corners_pairs))]
    if first_door_wall[0][0] == first_door_wall[1][0]: #if x coords are equal, build door along z axis
        editor.placeBlock((first_door_wall[0][0], \
                           first_door_wall[0][1]+1, \
                           np.random.randint(low=min(first_door_wall[0][2], first_door_wall[1][2])+1,
                                            high=max(first_door_wall[0][2], first_door_wall[1][2]))),

                            Block(getRandomDoor()))
    
    elif first_door_wall[0][2] == first_door_wall[1][2]: #if z coords are equal, build door along x axis
        editor.placeBlock((np.random.randint(low=min(first_door_wall[0][0], first_door_wall[1][0])+1,
                                            high=max(first_door_wall[0][0], first_door_wall[1][0])),
                            first_door_wall[0][1]+1,\
                            first_door_wall[0][2]             
                                            ),

                            Block(getRandomDoor()))



#buildSingleFloorAndRoof((STARTX, STARTY, STARTZ))










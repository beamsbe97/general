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


STARTX, STARTY, STARTZ = buildArea.begin
LASTX, LASTY, LASTZ = buildArea.last

print(f"Start: {STARTX, STARTY, STARTZ}")
print(f"Last: {LASTX, LASTY, LASTZ}")

def solidBlock(block_coords: tuple): #returns True if a block is solid
    block = editor.getBlock(block_coords)
    if block.id != "minecraft:air"\
        and "leaves" not in block.id\
        and block.id not in ["minecraft:tall_grass", "minecraft:grass", "minecraft:water"]:
        return True
    else:
        return False

def floorHeight(floor_x, floor_z):
    foundation_heightmap =  heightmap[:floor_x+1,:floor_z+1]
    return foundation_heightmap.max()

def getRandomStairs():
    ids = ["minecraft:oak_stairs", 
                  "minecraft:spruce_stairs", 
                  "minecraft:jungle_stairs",
                  "minecraft:dark_oak_stairs",
                  "minecraft:purpur_stairs",
                  "minecraft:oxidized_cut_copper_stairs"]
    return ids[np.random.randint(0, len(ids))]

def getRandomWall():
    ids = ["minecraft:dark_oak_log", "minecraft:iron_block", "minecraft:red_terracotta",
            "minecraft:acacia_log","minecraft:stripped_acacia_wood", "minecraft:stripped_birch_wood"]
    return ids[np.random.randint(0, len(ids))]

def getRandomSlab():
    ids = ["minecraft:oak_slab", "minecraft:birch_slab", "minecraft:stone_slab",
           "minecraft:spruce_slab", "minecraft:jungle_slab", "minecraft:quartz_slab",
           "minecraft:dark_oak_slab", "minecraft:dark_prismarine_slab"]
    return ids[np.random.randint(0, len(ids))]

def getRandomBed():
    ids = ["minecraft:red_bed", "minecraft:lime_bed", 
           "minecraft:light_blue_bed", "minecraft:yellow_bed"]
    return ids[np.random.randint(0, len(ids))]

def getRandomDoor():
    ids = ["minecraft:oak_door", "minecraft:birch_door",\
               "minecraft:jungle_door", "minecraft:dark_oak_door", \
                "minecraft:acacia_door"]
    return ids[np.random.randint(0, len(ids))]

def getRandomGlassPane():
    ids = ["minecraft:lime_stained_glass_pane", "minecraft:lime_stained_glass_pane",\
               "minecraft:glass_pane", "minecraft:pink_stained_glass_pane",\
                "minecraft:blue_stained_glass_pane", "minecraft:yellow_stained_glass_pane"]
    return ids[np.random.randint(0, len(ids))]  

def getRandomPots():
    ids = ["minecraft:potted_blue_orchid", "minecraft:potted_oxeye_daisy",
           "minecraft:potted_crimson_roots", "minecraft:potted_red_tulip", 
           "minecraft:potted_orange_tulip", "minecraft:potted_red_mushroom",
           "minecraft:potted_lily_of_the_valley", "minecraft:potted_allium", 
           "minecraft:potted_dandelion"]
    return ids[np.random.randint(0, len(ids))]

def getInteriorCornerSidePairs(building_corners):

    building_corners= [[corner1, corner2, "south"],
                        [corner1, corner3, "east"],
                        [corner2, corner4, "west"],
                        [corner3, corner4, "north"]]
    
    return[[(building_corners[0][0][0]+1, building_corners[0][0][1], building_corners[0][0][2]+1),
            (building_corners[0][2][0]-1, building_corners[0][2][1], building_corners[0][2][2]+1),"south"],
            [(building_corners[0][0][0]+1, building_corners[0][0][1], building_corners[0][0][2]+1),
            (building_corners[0][2][0]+1, building_corners[0][2][1], building_corners[0][2][2]+1),"east"],]


    

def getOppositeCardinal(direction):
    if direction=="east":
        return "west"
    elif direction=="west":
        return "east"
    elif direction=="north":
        return "south"
    else:
        return "north"

def buildRoof(start, end):
    cardinal_pairs = [["east", "west"], ["north", "south"]]
    coord_idx = [0, 2] #start from x(0) or z(2), following the tuple order (x,y,z)
    idx = np.random.randint(0, 2)
    stair_block = getRandomStairs()

    for i in range(np.random.randint(-1,1), ((end[coord_idx[idx]]-start[coord_idx[idx]])//2)+1): 
        if idx==1:
            geo.placeCuboid(editor, 
                            (start[0],start[1]+i, start[2]+i), 
                            (end[0],start[1]+i, start[2]+i), 
                            Block(stair_block, {"facing":f"{cardinal_pairs[idx][1]}", "half":"bottom"}))
            geo.placeCuboid(editor, 
                            (start[0],end[1]+i, end[2]-i), 
                            (end[0],end[1]+i, end[2]-i), 
                            Block(stair_block, {"facing":f"{cardinal_pairs[idx][0]}", "half":"bottom"}))

        else:    
            geo.placeCuboid(editor, 
                            (start[0]+i,start[1]+i, start[2]), 
                            (start[0]+i,start[1]+i,end[2]), 
                            Block(stair_block, {"facing":f"{cardinal_pairs[idx][0]}", "half":"bottom"}))
            geo.placeCuboid(editor, 
                            (end[0]-i,end[1]+i, start[2]), 
                            (end[0]-i,end[1]+i,end[2]), 
                            Block(stair_block, {"facing":f"{cardinal_pairs[idx][1]}", "half":"bottom"}))

        if i==((end[coord_idx[idx]]-start[coord_idx[idx]])//2):
            if ((end[coord_idx[idx]]-start[coord_idx[idx]])+1)%2 != 0:
                mid = (end[coord_idx[idx]]+start[coord_idx[idx]])//2
                if idx==0:
                    geo.placeCuboid(editor,
                                    (mid, start[1]+i, start[2]),
                                    (mid, start[1]+i, end[2]),
                                    Block(getRandomSlab()))
                
                else:
                    geo.placeCuboid(editor,
                                    (start[0], start[1]+i, mid),
                                    (end[0], start[1]+i, mid),
                                    Block(getRandomSlab()))

def buildSupportBeam(corner_block: tuple, block_type="minecraft:birch_planks",direction=None):
    check_solid_below = True
    current_y = corner_block[1]
    while check_solid_below:
        current_y-= 1
        if solidBlock((corner_block[0], current_y, corner_block[2])):
            check_solid_below = False
        else:
            if direction:
                editor.placeBlock((corner_block[0], current_y, corner_block[2]), Block(block_type, direction))
            else:
                editor.placeBlock((corner_block[0], current_y, corner_block[2]), Block(block_type))

    return (corner_block[0], current_y, corner_block[2])

def buildByDirection(start, end, block_type, direction, howfar=0):
    if direction in ["north", "south"]:
        geo.placeCuboid(editor,
                        (start[0]-1, start[1], start[2]+(1 if direction=="north" else -1)),
                        (end[0]+1, end[1], end[2]+ (howfar if direction=="north" else -howfar)),
                        Block(block_type))
    
    else:
        geo.placeCuboid(editor,
                        (start[0]+(-1 if direction=="east" else 1), start[1], start[2]-1),
                        (end[0]+ (-howfar if direction=="east" else howfar), end[1], end[2]+1),
                        Block(block_type))


def buildGarden(start, end, direction, footpath_pos):
    garden_depth = np.random.randint(2, 6)
    footpath_end = ()
    ladder_start = ()
    if direction in ["north", "south"]:
        geo.placeCuboid(editor,
                        (start[0]-1, start[1], start[2]+(1 if direction=="north" else -1)),
                        (end[0]+1, end[1]+10, end[2]+ (garden_depth if direction=="north" else -garden_depth)),
                        Block("minecraft:air"))
        geo.placeCuboid(editor,
                        (start[0]-1, start[1], start[2]+(1 if direction=="north" else -1)),
                        (end[0]+1, end[1], end[2]+ (garden_depth if direction=="north" else -garden_depth)),
                        Block("minecraft:grass_block"))
        
        for i in range(start[0], end[0]+1):
            if i!= footpath_pos: #place flower pots
                geo.placeCuboid(editor,
                            (i, start[1]+1, start[2]+(1 if direction=="north" else -1)),
                            (i, end[1]+1, end[2]+ (garden_depth if direction=="north" else -garden_depth)),
                            Block(getRandomPots()))
            else: #build footpath
                footpath_end = (i, end[1], end[2]+ (garden_depth if direction=="north" else -garden_depth))
                ladder_start = (footpath_end[0], footpath_end[1], footpath_end[2]+ (1 if direction=="north" else -1))
                geo.placeCuboid(editor,
                            (i, start[1], start[2]+(1 if direction=="north" else -1)),
                            footpath_end,
                            Block("minecraft:cobblestone"))

    else:
        geo.placeCuboid(editor,
                        (start[0]+(-1 if direction=="east" else 1), start[1], start[2]-1),
                        (end[0]+ (-garden_depth if direction=="east" else garden_depth), end[1]+10, end[2]+1),
                        Block("minecraft:air"))
        geo.placeCuboid(editor,
                        (start[0]+(-1 if direction=="east" else 1), start[1], start[2]-1),
                        (end[0]+ (-garden_depth if direction=="east" else garden_depth), end[1], end[2]+1),
                        Block("minecraft:grass_block"))
           
        for i in range(start[2], end[2]+1):
            if i!= footpath_pos: #place flower pots
                geo.placeCuboid(editor,
                            (start[0]+(-1 if direction=="east" else 1), start[1]+1, i),
                            (end[0]+ (-garden_depth if direction=="east" else garden_depth), end[1]+1, i),
                            Block(getRandomPots()))
            else: #build footpath
                footpath_end = (end[0]+ (-garden_depth if direction=="east" else garden_depth), end[1], i)
                ladder_start = (footpath_end[0]+ (-1 if direction=="east" else 1), footpath_end[1], footpath_end[2])
                geo.placeCuboid(editor,
                            (start[0]+(-1 if direction=="east" else 1), start[1], i),
                            (end[0]+ (-garden_depth if direction=="east" else garden_depth), end[1], i),
                            Block("minecraft:cobblestone"))
    buildSupportBeam(footpath_end)
    
    if not solidBlock(ladder_start): #builds ladder at the end of the footpath
        editor.placeBlock(ladder_start, Block("minecraft:ladder", {"facing":getOppositeCardinal(direction)}))
        buildSupportBeam(ladder_start, "minecraft:ladder", {"facing":getOppositeCardinal(direction)})

    geo.placeCuboid(editor,
                    ladder_start, #clears space above the ladder
                    (ladder_start[0], ladder_start[1]+3, ladder_start[2]),
                    Block("minecraft:air"))

def buildRectWindow(start, end, direction, building_height):
    print(f"Start: {start}")
    print(f"End: {end}")   
    if direction in ["east", "west"]:
        window_start = (start[0], 
                        start[1]+2, 
                        np.random.randint(start[2],end[2]))

        window_end = (end[0], 
                      np.random.randint(start[1]+2,end[1]+building_height), 
                      np.random.randint(window_start[2], end[2]+1))

    else:
        window_start = (np.random.randint(start[0],end[0]), 
                        start[1]+2, 
                        start[2])

        window_end = (np.random.randint(window_start[0], end[0]+1), 
                      np.random.randint(start[1]+2,end[1]+building_height), 
                      end[2])  

    geo.placeCuboid(editor, 
                    window_start, 
                    window_end, 
                    Block(getRandomGlassPane()))

def buildBookShelf(start, end, direction, height_limit):
    height = np.random.randint(0, height_limit)
    
    if direction in ["east", "west"]:
        window_start = (start[0], 
                        start[1], 
                        np.random.randint(start[2],end[2]))

        window_end = (end[0], 
                      np.random.randint(start[1],end[1]+height+1), 
                      np.random.randint(window_start[2], end[2]+1))

    else:
        window_start = (np.random.randint(start[0],end[0]), 
                        start[1], 
                        start[2])

        window_end = (np.random.randint(window_start[0], end[0]+1), 
                      np.random.randint(start[1], end[1]+height+1), 
                      end[2])  
        
    geo.placeCuboid(editor, window_start, window_end, Block("minecraft:bookshelf"))
    

def buildSingleFloorAndRoof(start: tuple):
    building_ydim = np.random.randint(4, 7)
    building_xdim = np.random.randint(5, 8)
    building_zdim = np.random.randint(5, 8)
    #building_xdim, building_ydim, building_zdim = 4,4,4
    end = (start[0]+building_xdim, start[1]+building_ydim, start[2]+building_zdim)
    
    highest_terrain_y = floorHeight(building_xdim, building_zdim)

    # 4 corners of the floor
    corner1 = (start[0], highest_terrain_y, start[2])
    corner4 = (end[0], highest_terrain_y, end[2])
    corner2 = (corner1[0]+building_xdim, corner1[1], corner1[2])
    corner3 = (corner1[0], corner1[1], corner1[2]+ building_zdim)
    corners = [corner1, corner2, corner3, corner4]

    # corner pairs and their corresponding cardinal directions
    wall_corners_pairs = [[corner1, corner2, "south"],
                        [corner1, corner3, "east"],
                        [corner2, corner4, "west"],
                        [corner3, corner4, "north"]]
    
    interior_corners=[[(corner1[0]+1,corner1[1]+1,corner1[2]+1),(corner2[0]-1,corner2[1]+1,corner2[2]+1),"south"],
                      [(corner1[0]+1,corner1[1]+1,corner1[2]+1),(corner3[0]+1,corner3[1]+1,corner3[2]-1),"east"],
                      [(corner2[0]-1,corner2[1]+1,corner2[2]+1),(corner4[0]-1,corner4[1]+1,corner4[2]-1),"west"],
                      [(corner1[0]+1,corner1[1]+1,corner1[2]+1),(corner4[0]-1,corner4[1]+1,corner4[2]-1),"north"]]

    for corner in corners:
        buildSupportBeam(corner)

    geo.placeCuboidHollow(editor, 
                          corner1, 
                          (end[0], highest_terrain_y+building_ydim, end[2]), 
                          Block(getRandomWall()))

    buildRoof(start=(corner1[0], corner1[1]+building_ydim+1, corner1[2]),
              end=(corner4[0], corner4[1]+building_ydim+1, corner4[2]))
    
    ###Build door #####
    first_door_wall = wall_corners_pairs[np.random.randint(0, len(wall_corners_pairs))]
    

    if first_door_wall[0][0] == first_door_wall[1][0]: #if x coords are equal, build door along z axis
        door_pos_on_wall = np.random.randint(low=min(first_door_wall[0][2], first_door_wall[1][2])+1,
                                            high=max(first_door_wall[0][2], first_door_wall[1][2]))
        editor.placeBlock((first_door_wall[0][0],
                           first_door_wall[0][1]+1,
                           door_pos_on_wall),
                        Block(getRandomDoor(), {"facing":f"{first_door_wall[2]}"}))
        
        editor.placeBlock((first_door_wall[0][0],
                           first_door_wall[0][1]+1,
                           door_pos_on_wall),
                        Block(getRandomDoor()))
        
        
        editor.placeBlock((first_door_wall[0][0]+(1 if first_door_wall[2]=="east" else -1),
                           first_door_wall[0][1]+1,
                           door_pos_on_wall-1 if (door_pos_on_wall+1 == first_door_wall[1][2]) else door_pos_on_wall+1),
                        Block(getRandomBed(), {"facing":f"{first_door_wall[2]}"}))

    
    elif first_door_wall[0][2] == first_door_wall[1][2]: #if z coords are equal, build door along x axis
        door_pos_on_wall = np.random.randint(low=min(first_door_wall[0][0], first_door_wall[1][0])+1,
                                            high=max(first_door_wall[0][0], first_door_wall[1][0]))
        editor.placeBlock((door_pos_on_wall,
                            first_door_wall[0][1]+1,
                            first_door_wall[0][2]),
                        Block(getRandomDoor(), {"facing":f"{first_door_wall[2]}"}))

        editor.placeBlock(((door_pos_on_wall-1 if (door_pos_on_wall+1 == first_door_wall[1][0]) else door_pos_on_wall+1),
                        first_door_wall[0][1]+1,
                        first_door_wall[0][2]+(-1 if first_door_wall[2]=="north" else 1)),
                    Block(getRandomBed(), {"facing":f"{first_door_wall[2]}"}))
        
    buildGarden(first_door_wall[0], first_door_wall[1], first_door_wall[2], door_pos_on_wall)   

    ###Build window
    window_side = random.choice([side for side in wall_corners_pairs if side[2] != first_door_wall[2]])
    buildRectWindow(window_side[0], window_side[1], window_side[2], building_ydim)

    ###Build bookshelf
    shelf_side = random.choice([side for side in interior_corners if side[2] not in [first_door_wall[2], window_side[2]]])
    buildBookShelf(shelf_side[0], shelf_side[1], shelf_side[2], building_ydim)
buildSingleFloorAndRoof((STARTX, STARTY, STARTZ))








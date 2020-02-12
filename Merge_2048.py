# -*- coding: utf-8 -*-
"""
@author: Brock
http://www.codeskulptor.org/#user46_Z3vfYFctBzPEXOV.py"""

"""
Clone of 2048 game.
"""

import poc_2048_gui
import random

# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}


def merge(line):
    """
    Function that merges a single row or column in 2048.
    """
    moving_tiles = rem_emptys(line)
       
    moving_tiles = tile_add(moving_tiles)
 
    new_tiles = rem_emptys(moving_tiles)

    return new_tiles


## Helper functions
def rem_emptys(line):
    """
    Function removes empty lines and slides tiles then adds 
    empty tiles to the original positions.
    """
    for tile in line:
        if len(line) > 1:
            moving_tiles = [tile for tile in line if tile != 0]
            while len(moving_tiles) < len(line):
                moving_tiles.append(0) 
        else:
            return line  
    return moving_tiles

def tile_add(moving_tiles):
    """
    Function that adds the tiles together in order to get the value
    of the new-combined tile.
    """
    for num in range(len(moving_tiles) - 1):
        if moving_tiles[num] == moving_tiles[num + 1]:
            moving_tiles[num] = moving_tiles[num] + moving_tiles[num + 1]
            moving_tiles[num + 1] = 0
    return moving_tiles

def init_tiles_dict(grid_height, grid_width):
    """
    Creates a dictionary for the inital tiles, 
    which are the first tiles passed to the merge function.
    
    Keys are the directions UP, DOWN , LEFT, RIGHT
    Values are list of the initial tiles for the given direction.
    """
    init_tiles = {}
    init_tiles[UP] 	  = [(0, row) for row in range(grid_width)]
    init_tiles[DOWN]  = [(grid_height -1, row) for row in range(grid_width)]
    init_tiles[LEFT]  = [(col, 0) for col in range(grid_height)]
    init_tiles[RIGHT] = [(col, grid_width -1) for col in range(grid_height)]
    return init_tiles

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        
        self.height = grid_height
        self.width = grid_width
        self.grid = []
        self.init_list = init_tiles_dict(grid_height, grid_width)
        
        self.reset()

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self.grid = [[0 for col in range(self.width)]
                                for row in range(self.height)]
                     
        self.merged_columns = [merge(cols) for cols in self.get_columns()]
        self.new_tile()
        self.new_tile()
                
    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        grid_string = ""
        for row in self.grid:
            grid_string += '\n' + str(row) 
        return grid_string
        
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        return self.height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        return self.width
    
    def get_columns(self):
        grid_cols = []
        count = 0
        for col in range(self.width):
            columns = []
            for row in self.grid:
                if col == count:
                    columns.append(row[col])
            grid_cols.append(columns)
            count += 1
        self.grid_columns = grid_cols
        return self.grid_columns
        
    def move(self, direction):
        """
        Takes the direction - keyboard input and carries out the movement
        using the helper function move_helper()
       """
        init_list = self.init_list[direction]
        temp_list = []

        if(direction == UP):
            self.move_helper(init_list, direction, temp_list, self.height)         
        elif(direction == DOWN):
            self.move_helper(init_list, direction, temp_list, self.height)            
        elif(direction == LEFT):
            self.move_helper(init_list, direction, temp_list, self.width)            
        elif(direction == RIGHT):
            self.move_helper(init_list, direction, temp_list, self.width)
            
            
    def move_helper(self, initial_list, direction, temp_list, list):
        """
        Helps move the columns and merge the values
        If cells have moved, adds a new tile to the grid
        """
        before_grid= str(self.grid)

        for tile in initial_list:
            temp_list.append(tile)
            
            for index in range(1, list):
                temp_list.append([x + y for x, y in zip(temp_list[-1], OFFSETS[direction])])
            
            indices = []
            
            for index in temp_list:
                indices.append(self.get_tile(index[0], index[1]))
            
            merged_list = merge(indices)
            
            for index_x, index_y in zip(merged_list, temp_list):
                self.set_tile(index_y[0], index_y[1], index_x)
        
            temp_list = []
        
        if before_grid != str(self.grid):
            self.new_tile()
                
            
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """ 
        random_value = random.randrange(1, 100)
        if random_value <= 90:
            value = 2
        else:
            value = 4
        
        empty_cells = []
        for row in range(self.height):
            for col in range(self.width):
                if self.grid[row][col] == 0:
                    empty_cells.append([row, col])
        
        choice = random.choice(empty_cells)
        self.grid[choice[0]][choice[1]] = value
        
    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self.grid[row][col] = value
         
    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self.grid[row][col]


poc_2048_gui.run_gui(TwentyFortyEight(4, 4))
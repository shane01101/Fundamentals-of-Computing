"""
Shane Honanie
http://www.codeskulptor.org/#user44_DNTwwdksfS1ZEBQ_8.py
Clone of 2048 game.
"""

#import poc_2048_gui
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
    result = []
    last_added = False
    index_next_available = 0
    for idx in range(len(line)):
        if line[idx] > 0:
            result.insert(index_next_available,line[idx])
            
            if idx > 0 and  not last_added and result[index_next_available] == result[index_next_available - 1]:
                result[index_next_available - 1] *= 2
                last_added = True
                result.pop(index_next_available)
                result.insert(len(result), 0)
            else:
                index_next_available += 1
                last_added = False
        else:
            result.insert(len(result), line[idx])
    
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        self._height = grid_height
        self._width = grid_width
        self.reset()
        
        self._move_dir = {UP:[[0, col] for col in range(self._width)], \
            DOWN:[[(self._height - 1), col] for col in range(self._width)], \
            LEFT:[[row, 0] for row in range(self._height)], \
            RIGHT:[[row, (self._width - 1)] for row in range(self._height)]}

    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
        self._grid = [[0 for dummy_col in range(self._width)]
            for dummy_row in range(self._height)]
        
        self.new_tile()
        self.new_tile()
        #print self._grid
        #print 
        #for col in range(self._height):
            #print self._grid[col]

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        result = ""
        for line in list(self._grid):
            result += str(line) + "\n"
        return result
                    
    def get_grid_height(self):
        """
        Get the height of the board.
        """
        # replace with your code
        return self._height

    def get_grid_width(self):
        """
        Get the width of the board.
        """
        # replace with your code
        return self._width
    def traverse_grid_get_intital_list(self, start_cell, direction, num_steps):
        """
        Function that iterates through the cells in a grid
        in a linear direction

        Both start_cell is a tuple(row, col) denoting the
        starting cell

        direction is a tuple that contains difference between
        consecutive cells in the traversal
        """
        result = []	
    
        for step in range(num_steps):
            row = start_cell[0] + step * direction[0]
            col = start_cell[1] + step * direction[1]
            #print "Processing cell", (row, col),
            #print " with val: ", self._grid[row][col]
            result.append(self._grid[row][col])
            
        return result
    
    
    def traverse_grid_change_list(self, start_cell, direction, num_steps, value):
        """
        Function that iterates through the cells in a grid
        in a linear direction

        Both start_cell is a tuple(row, col) denoting the
        starting cell

        direction is a tuple that contains difference between
        consecutive cells in the traversal
        """
        index = 0
        for step in range(num_steps):
            row = start_cell[0] + step * direction[0]
            col = start_cell[1] + step * direction[1]
            #print "Processing cell", (row, col),
            #print " with val: ", self._grid[row][col]
            self._grid[row][col] = value[index]
            index += 1
            

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        tile_group_size = 0
        tile_grid_group_old = []
        tile_group_new = []
        
        if direction <= 2:
            tile_group_size = self._height
        else:
            tile_group_size = self._width
        
        #for each inital tile
        for cell in self._move_dir[direction]:
            tile_grid_group_old.append(self.traverse_grid_get_intital_list(cell, OFFSETS[direction], tile_group_size))
        #print tile_group_old
        
        index = 0
        for cell in self._move_dir[direction]:
            tile_group_new = merge(tile_grid_group_old[index])
            self.traverse_grid_change_list(cell, OFFSETS[direction], tile_group_size, tile_group_new)
            index += 1
        self.new_tile()
    
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        zero_squares = []
        
        for col in range(self._height):
            for row in range(self._width):
                if self._grid[col][row] == 0:
                    zero_squares.append([col,row])
        
        if len(zero_squares) > 0:
            tile = random.choice(zero_squares)
            random_num = random.randrange(0, 10)
            
            if random_num <= 8:
                self._grid[tile[0]][tile[1]] = 2
            else:
                self._grid[tile[0]][tile[1]] = 4
            

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        self._grid[row][col] = value

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        return self._grid[row][col]


#poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

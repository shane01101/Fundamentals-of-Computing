"""
Shane Honanie

http://www.codeskulptor.org/#user45_WfdDiserIYgcq0y_13.py

Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        if self.get_number(target_row, target_col) != 0:
            return False
        
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if row < target_row:
                    continue
                    
                if row == target_row and col < target_col + 1:
                    continue
                    
                if self.current_position(row, col) != (row, col):
                    return False
        return True   

    def solve_interior_tile(self, target_row, target_col):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        """
        move_str = ""
        assert target_row > 1
        assert target_col > 0
        #assert self.lower_row_invariant(target_row, target_col)
        cur_row, cur_col = self.current_position(target_row, target_col)
        move_str += self.position_tile(target_row, target_col, cur_row, cur_col)
        
        self.update_puzzle(move_str)
        temp_str = move_str
        move_str = ""
        test_row, dummy_col = self.current_position(0,0)
        #print test_row, test_col
        #print self.get_number(test_row, test_col)
        
        if self.lower_row_invariant(target_row, target_col - 1) == False and test_row < target_row:
            move_str += 'ld'
        self.update_puzzle(move_str)
        #assert self.lower_row_invariant(target_row, target_col - 1)
        return temp_str + move_str

    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        assert self.lower_row_invariant(target_row, 0)
        zero_row, zero_col = target_row, 0
        cur_row, cur_col = self.current_position(target_row, 0)
        move_str = "ur"
        width2 = self.get_width()
        
        zero_row -= 1
        zero_col += 1
        
        if zero_row == cur_row:
            cur_row += 1
        
        #tile being solved at (i,0), move zero tile to end of row i-1
        if target_row == cur_row and cur_col == 0:
            while zero_col < width2 - 1:
                zero_col += 1
                move_str += "r"
        else:    
            cur_row, cur_col = self.current_position(target_row, 0)
#            print zero_row, 1
#            print cur_row, cur_col
#            print target_row, 0
#            print move_str
            move_str += self.position_tile(zero_row, 1, cur_row, cur_col)
            move_str += 'ld' #move 0 to left of target
            move_str += 'ruldrdlurdluurddlur'
            move_str += (self.get_width() - 2) * 'r'
            
        self.update_puzzle(move_str)    
        return move_str   
            
    
    def position_tile(self, target_row, target_col, cur_row, cur_col):
        """
        Helper function for solve_col0_tile and solve_interior_tile
        """
        move_str = ""
        
        zero_row, zero_col = target_row, target_col
#        print cur_row, cur_col
#        print target_row, target_col
#        print zero_row, zero_col
        
        #already in place, no need to move
        if cur_row == target_row and cur_col == target_col:
            return move_str
        
        #move 0 left
        if zero_col > cur_col:
            while zero_col > cur_col:
                move_str += 'l'
                zero_col -= 1
                
                if zero_col == cur_col and zero_row == cur_row:
                    cur_col += 1
        else:        
            #move 0 right
            while zero_col < cur_col:
                move_str += 'r'
                zero_col += 1
            
        
        #move 0 one above cur
        while zero_row > cur_row:
            move_str += 'u'
            zero_row -= 1
            
            if zero_row == cur_row and zero_col == cur_col:
                cur_row += 1
        
        #make sure not in target cell
        if cur_row != target_row or cur_col != target_col:
            #move cur down one position (clockwise)
            while cur_row < target_row and cur_col < self.get_width() - 1:
                move_str += 'rddlu'
                zero_row += 1
                cur_row += 1
                
            #move cur down one position (counter-clockwise)
            while cur_row < target_row:
                move_str += 'lddru'
                zero_row += 1
                cur_row += 1

            #move cur right by one position
            if cur_col  < target_col + 1:
                while cur_col  < target_col + 1 and zero_col < self.get_width() - 1 and cur_col != target_col:
                    if zero_col == (cur_col-1) and zero_row == cur_row: #zero is to left, move above
                        move_str += 'ur'
                        zero_col += 1
                        zero_row -= 1
                    
                    move_str += 'rdlur'
                    zero_col += 1
                    cur_col += 1
            else:
                #move cur left by one position
                while cur_col > target_col:
                    move_str += 'ldrul'
                    zero_col -= 1
                    cur_col -= 1

                    #remove 'ur' from end of str or put 0 on left of target
                    if cur_row != target_row and cur_col != target_col and move_str[:-2] == 'ur':
                        move_str = move_str[:-2]
        #if zero_row < target_row and zero_col > 0: #and self.lower_row_invariant(target_row, target_col) == False:
        #if self.lower_row_invariant(target_row, target_col - 1) == False:
        #    move_str += 'ld'
        return move_str

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        target_row = 0
        if self.get_number(target_row, target_col) != 0:
            return False
        
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if col <= target_col and row <= target_row:
                    continue
                    
                if row == target_row + 1 and col < target_col:
                    continue

                pos = self.current_position(row, col)
                #print pos
                if pos != (row, col):
                    return False
        return True  

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        target_row = 1
        if self.get_number(target_row, target_col) != 0:
            return False
        
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if col <= target_col and row <= target_row:
                    continue

                pos = self.current_position(row, col)
                #print pos
                if pos != (row, col):
                    return False
        return True   

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row0_invariant(target_col)
        dummy_row, zero_col = 0, target_col
        cur_row, cur_col = self.current_position(0, target_col)
        #print cur_row, cur_col
        move_str = 'ld'
        
        dummy_row += 1
        zero_col -= 1
        
        if zero_col == cur_col:
            cur_col += 1
        
        #tile being solved at (0,i), move zero tile to end of row i-1
        if target_col != cur_col and cur_row != 0:
            cur_row, cur_col = self.current_position(0, target_col)
            move_str += self.position_tile(1, zero_col, cur_row, cur_col)
            
            if move_str[-2:] == 'ur':
                move_str = move_str[:-2]
            move_str += 'urdlurrdluldrruld'
            
        self.update_puzzle(move_str)    
        return move_str   

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        assert self.row1_invariant(target_col)
        cur_row, cur_col = self.current_position(1, target_col)
        move_str = self.position_tile(1, target_col, cur_row, cur_col)
        self.update_puzzle(move_str)
        assert self.row0_invariant(target_col)
        return move_str
        

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        assert self.row1_invariant(1)
        move_str = 'lu'
        self.update_puzzle(move_str)
        while self.current_position(0, 1) != (0, 1):
            print self.current_position(0, 1)
            move_str += 'rdlu'
            self.update_puzzle('rdlu')
            
        return move_str

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        move_str = ''

        if self.check_if_solved():
            return move_str
        
        for row in range(self.get_height()-1, 1, -1):
            for col in range(self.get_width()-1, 0, -1):
                #print row, col
                move_str += self.solve_interior_tile(row,col)
            move_str += self.solve_col0_tile(row)
            
        for col in range(self.get_width()-1, 1, -1):
            move_str += self.solve_row1_tile(col)
            move_str += self.solve_row0_tile(col)
        
        move_str += self.solve_2x2()
        return move_str
    
    def check_if_solved(self):
        for row in range(self.get_height()):
            for col in range(self.get_width()):
                if self.current_position(row,col) != (row,col):
                    return False
        return True           

# Start interactive simulation
#poc_fifteen_gui.FifteenGUI(Puzzle(4, 4, [[4, 13, 1, 3], [5, 10, 2, 7], [8, 12, 6, 11], [9, 0, 14, 15]]))

#puzzle = Puzzle(4, 4, [[9, 1, 2, 3], [4, 5, 6, 7], [8, 11, 10, 0], [12, 13, 14, 15]])
#puzzle2 = Puzzle(4, 5, [[15, 11, 10, 9, 8], [7, 6, 5, 4, 3], [2, 1, 0, 13, 14], [12, 16, 17, 18, 19]])
#print puzzle2.get_number(2,2)
#print puzzle2.lower_row_invariant(2,2)

#puzzle4 = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#poc_fifteen_gui.FifteenGUI(puzzle4)
#print puzzle4.solve_interior_tile(2,2)


#puzzle5 = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [7, 0, 8]])
#poc_fifteen_gui.FifteenGUI(puzzle5)
#print puzzle5.solve_interior_tile(2,1)

#puzzle6 = Puzzle(3, 2, [[2, 4], [3, 1], [0, 5]])
#poc_fifteen_gui.FifteenGUI(puzzle6)
#print puzzle5.solve_interior_tile(2,1)

#puzzle7 = Puzzle(3, 2, [[1, 2], [0, 4], [3, 5]])
#poc_fifteen_gui.FifteenGUI(puzzle7)
#print puzzle5.solve_interior_tile(2,1)

#puzzle8 = Puzzle(3, 3, [[3, 2, 1], [6, 5, 4], [0, 7, 8]])
#poc_fifteen_gui.FifteenGUI(puzzle8)
#print puzzle8.solve_col0_tile(2)
#
#puzzle9 = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(puzzle9)
#print puzzle9.solve_col0_tile(3)

#puzzle10 = Puzzle(4, 4, [[4, 6, 1, 3], [5, 2, 0, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
#poc_fifteen_gui.FifteenGUI(puzzle10)
#print puzzle10.row1_invariant(2)
#
#puzzle11 = Puzzle(4, 4, [[4, 2, 0, 3], [5, 1, 6, 7], [8, 9, 10, 11], [12, 13, 14, 15]])
#poc_fifteen_gui.FifteenGUI(puzzle11)
#print puzzle11.row0_invariant(2)

#puzzle12 = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(puzzle12)
#print puzzle12.row0_invariant(2)
##
#puzzle13 = Puzzle(4, 5, [[15, 6, 5, 3, 4], [2, 1, 0, 8, 9], [10, 11, 12, 13, 14], [7, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(puzzle13)
#print puzzle13.row1_invariant(2)

#puzzle14 = Puzzle(3, 3, [[3, 0, 2], [1, 4, 5], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(puzzle14)
#print puzzle14.row0_invariant(1)

#puzzle15 = Puzzle(3, 3, [[2, 5, 4], [1, 3, 0], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(puzzle15)
#print puzzle15.solve_row1_tile(2)

#puzzle16 = Puzzle(4, 5, [[12, 11, 10, 9, 8], [7, 6, 5, 4, 3], [2, 1, 0, 13, 14], [15, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(puzzle16)
#print puzzle16.solve_interior_tile(2, 2)

#puzzle17 = Puzzle(4, 5, [[12, 11, 10, 9, 15], [7, 6, 5, 4, 3], [2, 1, 8, 13, 14], [0, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(puzzle17)
#print puzzle17.solve_col0_tile(3)

#puzzle18 = Puzzle(4, 5, [[7, 6, 5, 3, 2], [4, 1, 9, 8, 0], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(puzzle18)
#print puzzle18.solve_row1_tile(4)

#puzzle19 = Puzzle(3, 3, [[4, 1, 0], [2, 3, 5], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(puzzle19)
#print puzzle19.solve_row0_tile(2)

#puzzle20= Puzzle(4, 5, [[1, 2, 0, 3, 4], [6, 5, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(puzzle20)
#print puzzle20.solve_row0_tile(2)

#puzzle21 = Puzzle(4, 5, [[1, 2, 0, 3, 4], [6, 5, 7, 8, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(puzzle21)
#print puzzle21.solve_row0_tile(2)

#puzzle22 = Puzzle(4, 5, [[7, 6, 5, 3, 0], [4, 8, 2, 1, 9], [10, 11, 12, 13, 14], [15, 16, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(puzzle22)
#print puzzle22.solve_row0_tile(4)

#puzzle23 = Puzzle(3, 3, [[4, 3, 2], [1, 0, 5], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(puzzle23)
#print puzzle23.solve_2x2()

#puzzle24 = Puzzle(3, 3, [[8, 7, 6], [5, 4, 3], [2, 1, 0]])
#poc_fifteen_gui.FifteenGUI(puzzle24)
#print puzzle24.solve_puzzle()

#puzzle25 = Puzzle(3, 3, [[0, 1, 2], [3, 4, 5], [6, 7, 8]])
#poc_fifteen_gui.FifteenGUI(puzzle25)
#print puzzle25.solve_puzzle()
#print puzzle25.check_if_solved()

#puzzle26 = Puzzle(4, 5, [[15, 16, 0, 3, 4], [5, 6, 7, 8, 9], [10, 11, 12, 13, 14], [1, 2, 17, 18, 19]])
#poc_fifteen_gui.FifteenGUI(puzzle26)
#print puzzle26.solve_puzzle()
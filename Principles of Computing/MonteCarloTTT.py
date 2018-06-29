"""
Shane Honanie
http://www.codeskulptor.org/#user44_OI2hr7rxQt_7.py


Monte Carlo Tic-Tac-Toe Player
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 40       # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    """
    This function takes a current board and the next player to move. The function 
    should play a game starting with the given player by making random moves, 
    alternating between players. The function should return when the game is over. 
    The modified board will contain the state of the game, so the function does not 
    return anything. In other words, the function should modify the board input.
    """
    while(board.check_win() == None):
        empty_squares = board.get_empty_squares()
        square = random.choice(empty_squares)
        #print square
        board.move(square[0], square[1], player)
        player = provided.switch_player(player)
    
       
def mc_update_scores(scores, board, player):
    """
    This function takes a grid of scores (a list of lists) with the same dimensions 
    as the Tic-Tac-Toe board, a board from a completed game, and which player the 
    machine player is. The function should score the completed board and update the 
    scores grid. As the function updates the scores grid directly, it does not return anything
    """
    winner = board.check_win() 

    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if board.square(row, col) == provided.PLAYERX and winner == provided.PLAYERX:
                scores[row][col] += SCORE_CURRENT
            elif board.square(row, col) == provided.PLAYERO and winner == provided.PLAYERO:
                scores[row][col] += SCORE_CURRENT
            elif board.square(row, col) == provided.PLAYERX and winner == provided.PLAYERO:
                scores[row][col] -= SCORE_OTHER
            elif board.square(row, col) == provided.PLAYERO and winner == provided.PLAYERX:
                scores[row][col] -= SCORE_OTHER
            

def get_best_move(board, scores):
    """
    This function takes a current board and a grid of scores. The function should find all 
    of the empty squares with the maximum score and randomly return one of them as a 
    (row,column) tuple. It is an error to call this function with a board that has 
    no empty squares (there is no possible next move), so your function may do whatever it 
    wants in that case. The case where the board is full will not be tested.
    """
    empty_squares = board.get_empty_squares()
    best_moves_list = []
    max_num = -4
    
    for square in empty_squares:
        if(scores[square[0]][square[1]] == max_num):
            best_moves_list.append(square)
        elif (scores[square[0]][square[1]] > max_num):
            max_num = scores[square[0]][square[1]]
            best_moves_list = []
            best_moves_list.append(square)
    
    #print scores
    #print best_moves_list
    #print max_num
    
    return random.choice(best_moves_list)

def mc_move(board, player, trials):
    """
    This function takes a current board, which player the machine player is, and the number 
    of trials to run. The function should use the Monte Carlo simulation described above to 
    return a move for the machine player in the form of a (row,column) tuple.
    """
    num = 0
    scores = [[0 for dummy_row in range(board.get_dim())]
            for dummy_col in range(board.get_dim())]
    #print scores

    while num < trials:
        num += 1
        board_copy = board.clone()
        mc_trial(board_copy, player)
        mc_update_scores(scores, board_copy, player)

    return get_best_move(board, scores)


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)


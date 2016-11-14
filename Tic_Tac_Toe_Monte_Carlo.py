'''
a tic tac toe game with monte carlo simulation
'''

# Constants

EMPTY = 1
PLAYERX = 2
PLAYERO = 3 
DRAW = 4

SIGNAL = {EMPTY:' ',
          PLAYERX: 'X',
          PLAYERO: 'O'}


class TTTBoard:
    """
    Class to represent a Tic-Tac-Toe board.
    """

    def __init__(self, dim, reverse = False, board = None):
        """
        Initialize the TTTBoard object with the given dimension and 
        whether or not the game should be reversed.
        """
        self._dim=dim
        self._reverse=reverse
        if board==None:
            self._board=[ [ EMPTY for dummy_col in range(dim)]
                          for dummy_row in range(dim)]
        else:
            self._board=[ [ board[row][col] for col in range(dim)]
                          for row in range(dim)]

            
            
    def __str__(self):
        """
        Human readable representation of the board.
        """
        signal = ""
        for row in range(self._dim):
            for col in range(self._dim):
                signal += SIGNAL[self._board[row][col]]
                if col == self._dim - 1:
                    signal += "\n"
                else:
                    signal += " | "
            if row != self._dim - 1:
                signal += "-" * (4 * self._dim - 3)
                signal += "\n"
        return signal

    

    def get_dim(self):
        """
        Return the dimension of the board.
        """
        return self._dim
    
    def square(self, row, col):
        """
        Returns one of the three constants EMPTY, PLAYERX, or PLAYERO 
        that correspond to the contents of the board at position (row, col).
        """
        return self._board[row][col]

    def get_empty_squares(self):
        """
        Return a list of (row, col) tuples for all empty squares
        """
        empty=[]
        for row in range(self._dim):
            for col in range(self._dim):
                if self._board[row][col]==EMPTY:
                    empty.append((row,col))

        return empty
    

    def move(self, row, col, player):
        """
        Place player on the board at position (row, col).
        player should be either the constant PLAYERX or PLAYERO.
        Does nothing if board square is not empty.
        """
        if self._board[row][col]==EMPTY:
            self._board[row][col]=player

        

    def check_win(self):
        """
        Returns a constant associated with the state of the game
            If PLAYERX wins, returns PLAYERX.
            If PLAYERO wins, returns PLAYERO.
            If game is drawn, returns DRAW.
            If game is in progress, returns None.
        """
        lines=[]
        lines.extend(self._board)

        cols=[ [ self._board[rowid][colid] for rowid in range(self._dim)]
               for colid in range(self._dim)]
        lines.extend(cols)

        diag1 = [ self._board[rowid][rowid] for rowid in range(self._dim)]
        diag2 = [ self._board[rowid][self._dim - 1 - rowid]
                  for rowid in range(self._dim)]
        lines.append(diag1)
        lines.append(diag2)

        for line in lines:
            if len(set(line))==1 and line[0]!=EMPTY:
                if self._reverse:
                    return provided.switch_player(line[0])
                else:
                    return line[0]

        #check if draw
        if len(set(self.get_empty_squares()))==0:
            return DRAW

        #still in progress
        return None
       
    def clone(self):
        """
        Return a copy of the board.
        """
        return TTTBoard(self._dim,self._reverse,self._board)
        
#end of the class TTTBoard:


#Monte Carlo Tic-Tac-Toe Player


import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 1         # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
# Add your functions here.
def mc_trial(board, player):
    '''
    takes a current board and the next player to move,
    play a game starting with the given player by making random moves, alternating between players;
    modified board will contain the state of the game, does not return anything
    '''
    player_win = board.check_win()
    while player_win == None:
        empty = board.get_empty_squares()
        next_move = empty[random.randrange(len(empty))]
        board.move(next_move[0], next_move[1], player)
        player = provided.switch_player(player)
        player_win = board.check_win()


def mc_update_scores(scores, board, player):
    '''
    takes a grid of scores (a list of lists)
    score the completed board and update the scores grid
    does not return anything
    '''
    winner=board.check_win()

    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            player = board.square(row,col)
            
            if player == PLAYERX:
                if winner == PLAYERX:
                    scores[row][col] += SCORE_CURRENT
                elif winner == PLAYERO:
                    scores[row][col] -= SCORE_OTHER
            elif player == PLAYERO:
                if winner == PLAYERX:
                    scores[row][col] -= SCORE_OTHER
                elif winner == PLAYERO:
                    scores[row][col] += SCORE_CURRENT
            else:
                #0 value
                pass
                
def get_best_move(board, scores):
    '''
    takes a current board and a grid of scores
    find all of the empty squares with the maximum score and randomly return one of them as a (row, column) tuple
    board that has no empty squares results in error
    '''
    empty_squares = board.get_empty_squares()
    if len(empty_squares)==0:
        return 
    
    vals = [scores[square[0]][square[1]] for square in empty_squares]
    max_val = max(vals)
    moves = []

    for row in range(board.get_dim()):
        for col in range(board.get_dim()):
            if scores[row][col]==max_val and (row,col) in empty_squares:
                moves.append((row, col))
                
    return random.choice( moves )


def mc_move(board, player, trials):
    '''
    takes a current board, which player the machine player is
    ,and the number of trials to run
    use the Monte Carlo simulation to return a move for the machine player in the form of a (row, column) tuple
    '''
    # creates initial score board with every values sets to 0
    initial_scores = [[0 for dummy_col in range(board.get_dim())] for dummy_row in range(board.get_dim())]

    for dummy_trial in range(trials):
        cloned = board.clone()
        mc_trial(cloned, player)
        mc_update_scores(initial_scores, cloned, player)
        
    return get_best_move(board, initial_scores)
    


# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

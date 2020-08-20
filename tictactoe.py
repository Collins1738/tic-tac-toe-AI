"""
Tic Tac Toe Player
"""
import copy
import math

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    count = 0
    for i in board:
        for j in i:
            if j:
                count+=1
    if count%2==1:
        return O
    else:
        return X


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    i = 0
    while i < 3:
        j = 0
        while j < 3:
            if not board[i][j]:
                possible_actions.add((i, j))
    return possible_actions

def previous_actions(board):
    """
    Returns set of all previously played actions (i, j) available on the board.
    """
    played_actions = set()
    i = 0
    while i < 3:
        j = 0
        while j < 3:
            if board[i][j]:
                played_actions.add((i, j))
            j+=1
        i+=1
    return played_actions


def add_move_actions(move):
    """
    Finds all possible next moves from passed in move
    """
    for i in range(0, 3):
        for j in range(0, 3):
            if (i, j) not in move.previously_played and (i, j) != move.value:
                temp = Move((i, j), move)
                temp.player = opposite(move.player)
                move.possible_actions.add(temp)
    return



def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    board = copy.deepcopy(board)
    if action:
        board[action[0]][action[1]] = player(board)
    return board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    wins = []

    for i in range(0, 3):
        wins.append([(i, 0), (i, 1), (i, 2)])
        wins.append([(0, i), (1, i), (2, i)])
    wins.append([(0, 0), (1, 1), (2, 2)])
    wins.append([(0, 2), (1, 1), (2, 0)])
    for possible_win in wins:
        a = possible_win[0]
        b = possible_win[1]
        c = possible_win[2]
        if board[a[0]][a[1]] == board[b[0]][b[1]] == board[c[0]][c[1]] and board[a[0]][a[1]]:
            return board[a[0]][a[1]]
    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    if winner(board):
        return True
    for i in board:
        for j in i:
            if not j:
                return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    the_winner = winner(board)
    if the_winner == X:
        return 1
    elif the_winner == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    # X always wants the max, O always wants the min
    head = Move(None)
    head.board = board
    head.player = opposite(player(head.board))
    head.previously_played = previous_actions(board)
    add_move_actions(head)
    
    for action in head.possible_actions:
        recurse(action, head)
    if head.player == X:
        # then optimal next move would be played by O so mini
        (head.optimal_next_move, head.score) = mini(head.possible_actions)
    elif head.player == O:
        # then optimal next move would be played by X so maxi
        (head.optimal_next_move, head.score) = maxi(head.possible_actions)
    
    return head.optimal_next_move.value


def recurse(move, parent):
    move.board = result(parent.board, move.value) # update board
    move.previously_played = parent.previously_played.copy()
    move.previously_played.add(move.value)
    add_move_actions(move)
    if terminal(move.board):
        move.score = utility(move.board)
        return
    else:
        for action in move.possible_actions:
            recurse(action, move)
    # calculate move score
    if move.player == X:
        (move.optimal_next_move, move.score) = mini(move.possible_actions)
    elif move.player == O:
        (move.optimal_next_move, move.score) = maxi(move.possible_actions)
    return


def opposite(player):
    """
    Returns O if player is X, and X if player is O
    """
    if player == X:
        return O
    elif player == O:
        return X
    else:
        print("something wrong, player invalid?")
        return None


def mini(moves):
    """
    Returns the move with the minimum score and that score
    """
    if len(moves) == 0:
        return None
    minScore = 1
    minmove = None
    for move in moves:
        if move.score <= minScore:
            minScore = move.score
            minmove = move
    return (minmove, minScore)


def maxi(moves):
    """
    Returns the move with the maximum score and that score
    """
    if len(moves) == 0:
        return None
    maxScore = -1
    maxmove = None
    for move in moves:
        if move.score >= maxScore:
            maxScore = move.score
            maxmove = move
    return (maxmove, maxScore)


def print_move(move):
    """
    Prints different values in move object. For debugging
    """
    print("move value: ", move.value)
    if move.parent_move:
        print("move's parent", move.parent_move.value)
        if move.parent_move.parent_move:
            print("move's grand parent", move.parent_move.parent_move.value)
    print("move score: ", move.score)
    print("move possible actions: ", [(i.value, i.score) for i in move.possible_actions])
    if move.optimal_next_move:
        print("move optimal nm: ", move.optimal_next_move.value, move.optimal_next_move.score)
    print("move played by: ", move.player)
    print("move board: ", move.board)

class Move:
    """
    Move object. Represents each possible player move
    The Move object would be different for the same moves but made at different times
    """
    def __init__(self, value, parent = None):
        self.value = value # The move played 
        self.score = None # The move's score. Used to find optimal move
        self.possible_actions = set() # type move[]
        self.previously_played = set() # type move[]
        self.optimal_next_move = None
        self.parent_move = parent # Move made before current Move object
        self.player = None # Player current move is played by
        self.board = initial_state() # State of the board after current move is played

# TODO
# Add a secondary score for a faster victory
# Add a secondary score for a possiblity of a victory   
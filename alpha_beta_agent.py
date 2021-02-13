import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        # Your code here
        v, action = self.max_value(brd, float('-inf'), float('inf'), None, 1)

        return action

    # TODO make a good heuristic function
    def calc_heuristic(self, board):
        return 1

    # Return the max value of a board state.
    # PARAM [board.Board] board: the current board state
    # PARAM [int] a: alpha value
    # PARAM [int] b: beta value
    # PARAM [int] old_action: action taken to get to this board
    # PARAM [int] depth: max depth of the search
    # RETURN [int, int]: max value of the board state and the action to get to it
    def max_value(self, board, a, b, old_action, depth):
        """The maxvalue function for alpha beta search algorithm."""
        # Reached a terminal node or hit the max depth
        if(board.get_outcome() != 0) or (depth == self.max_depth):
            return self.calc_heuristic(board), old_action

        v = float('-inf')
        action = None
        # Go through all possible next actions in current state
        for next_board in self.get_successors(board):
            # alpha beta pruning logic
            min, next_action = self.min_value(next_board[0], a, b, next_board[1], depth+1)
            if min > v:
                v = min
                action = next_action

            if v >= b: # prune
                return v, action
            else:
                a = max(a, v)

        return v, action

    # Return the max value of a board state.
    # PARAM [board.Board] board: the current board state
    # PARAM [int] a: alpha value
    # PARAM [int] b: beta value
    # PARAM [int] depth: max depth of the search
    # RETURN [int, int]: min value of the board state and the action to get to it
    def min_value(self, board, a, b, old_action, depth):
        """The minvalue function for alpha beta search algorithm."""
        # Reached a terminal node or hit the max depth
        if(board.get_outcome() != 0) or (depth == self.max_depth):
            return self.calc_heuristic(board), old_action

        v = float('inf')
        action = None
        # Go through all possible next actions in current state
        for next_board in self.get_successors(board):
            # alpha beta pruning logic
            max, next_action = self.max_value(next_board[0], a, b, next_board[1], depth+1)
            if max < v:
                v = max
                action = next_action

            if v <= a:
                return v, action
            else:
                b = min(b, v)

        return v, action

    # Get the successors of the given board.
    #
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ

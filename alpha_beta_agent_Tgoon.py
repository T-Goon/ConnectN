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
        self.my_token = brd.player
        v, action = self.max_value(brd, float('-inf'), float('inf'), None, 1)

        return action

    # Evaluate the current state of the board.
    # PARAM [board.Board] board: the current board state
    # PARAM [int] old_action: column that was last played
    # PARAM [int] depth: number of turns ahead the board is from when alpha beta
    #                    search was first called
    def eval_board(self, board, old_action, depth):
        return self.get_board_score(board, self.my_token)

    def get_board_score(self, board, t):
        """Caluclate a score for the entire board. """
        # Find other players token
        if(t == 1):
            other = 2
        else:
            other = 1

        # calc for both you and oponent
        sum = 0
        sum += self.count_all(board, t)
        sum -= self.count_all(board, other)

        return sum

    def count_all(self, board, t):
        """ Get the sum of all tokens on the board """

        sum = 0
        # Go through all spaces on the board
        for i in range(board.h):
            for j in range(board.w):
                # only eval for the specified token
                if(board.board[i][j] == t):
                    sum += self.tokenScore(board, j, i, t)

        return sum

    def tokenScore(self, board, x, y, t):
        """ Look in all directions for 0 tokens and t tokens """

        # Look in all directions for 0 tokens and t tokens
        sum = 0
        sum += self.countLine(board, x, y, 0, 1, t) # up
        sum += self.countLine(board, x, y, 1, 1, t) # diagonal up right
        sum += self.countLine(board, x, y, 1, 0, t) # right
        sum += self.countLine(board, x, y, 1, -1, t) # diagonal down right
        sum += self.countLine(board, x, y, 0, -1, t) # down
        sum += self.countLine(board, x, y, -1, -1, t) # diagonal down left
        sum += self.countLine(board, x, y, -1, 0, t) # left
        sum += self.countLine(board, x, y, -1, 1, t) # diagonal up left

        return sum

    def countLine(self, board, x, y, dx, dy, t):
        """ Count the score of a token in one direction """
        sum = 0

        b = board.board

        for i in range(1, board.n):
            try:
                row = y+(dy*i)
                col = x+(dx*i)
                # stop python from using negetive indexes
                if(row < 0 or col < 0):
                    return 0

                if (t == b[row][col]):
                    sum = sum + 2
                elif (0 == b[row][col]):
                    sum = sum + 1
                else:
                    # discard when you encounter a oposing token
                    return 0

            except Exception:
                # discard when you go out of bounds
                return 0

        return sum

    # Return the max value of a board state and the action to get to that board state.
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
            return self.eval_board(board, old_action, depth), old_action

        v = float('-inf')
        action = None
        # Go through all possible next actions in current state
        for next_board in self.get_successors(board):
            # alpha beta pruning logic
            min, next_action = self.min_value(next_board[0], a, b, next_board[1], depth+1)
            # print("max ",min, "depth ", depth+1)

            if min > v:
                v = min
                action = next_action

            if v >= b: # prune
                return v, action

            a = max(a, v)

        return v, action

    # Return the min value of a board state and the action to get to that state.
    # PARAM [board.Board] board: the current board state
    # PARAM [int] a: alpha value
    # PARAM [int] b: beta value
    # PARAM [int] old_action: action taken to get to this board
    # PARAM [int] depth: max depth of the search
    # RETURN [int, int]: min value of the board state and the action to get to it
    def min_value(self, board, a, b, old_action, depth):
        """The minvalue function for alpha beta search algorithm."""
        # Reached a terminal node or hit the max depth
        if(board.get_outcome() != 0) or (depth == self.max_depth):
            return self.eval_board(board, old_action, depth), old_action

        v = float('inf')
        action = None
        # Go through all possible next actions in current state
        for next_board in self.get_successors(board):
            # alpha beta pruning logic
            max, next_action = self.max_value(next_board[0], a, b, next_board[1], depth+1)
            # print("min ",max, "depth ", depth+1)

            if max < v:
                v = max
                action = next_action

            if v <= a: # prune
                return v, action

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

THE_AGENT = AlphaBetaAgent("Group20", 4)

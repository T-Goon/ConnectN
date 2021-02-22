import agent
import board

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
        self.col_order = None

    # Calculates the column order given the board width, and memoizes the result.
    # PARAM [int] width: The board width
    def cache_col_order(self, width):
        # Do not recompute if not needed
        if self.col_order != None and self.col_order == width:
            return
        self.col_order = list()
        # Count down from the middle (rounded up)
        for i in range((width + 1) >> 1, 0, -1):
            # Compute left and right values and add to list if not present.
            self.col_order.append(i - 1)
            v = (width + 1) - i - 1
            if v in self.col_order:
                continue
            self.col_order.append(v)

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        self.cache_col_order(brd.w)

        # Negamax
        v, action = self.negamax(brd, float('-inf'), float('inf'), None, 1, brd.player)

        return action

    # Gets the score of a non-terminal board.
     # PARAM [board.Board] board: The current state of the board.
     # PARAM [int] player: The value of a player's token. [1|2]
     # PARAM [int] other: The value of the opponent's token. [1|2]
     # RETURN [int]: Summed score for tokens t on the board.
    def get_board_score(self, board, player, other):
        """Caluclate a score for the entire board. """

        # calc for both you and oponent
        sum = 0
        sum += self.count_all(board, player)
        sum -= self.count_all(board, other)

        return sum

    # Gets the score of all tokens on the board.
     # PARAM [board.Board] board: The current state of the board.
     # PARAM [int] t: The value of a player's token. [1|2]
     # RETURN [int]: Summed score for tokens t on the board.
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

    # Gets the score of a token in all directions.
     # PARAM [board.Board] board: The current state of the board.
     # PARAM [int] x: The column of the token on the board.
     # PARAM [int] y: The row of the token on the board.
     # PARAM [int] t: The value of a player's token. [1|2]
     # RETURN [int]: Summed score for all 8 directions of a token.
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

    # Gets the score of a token in one direction.
     # PARAM [board.Board] board: The current state of the board.
     # PARAM [int] x: The column of the token on the board.
     # PARAM [int] y: The row of the token on the board.
     # PARAM [int] dx: The x direction to look in. [-1|0|1]
     # PARAM [int] dy: The y direction to look in. [-1|0|1]
     # PARAM [int] t: The value of a player's token. [1|2]
     # RETURN [int]: Summed score for a single direction of a token.
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

                if (t == b[row][col]): # Found your token
                    sum += 2
                elif (0 == b[row][col]): # Found no token
                    sum += 1
                else:
                    # discard when you encounter a oposing token
                    return 0

            except Exception:
                # discard when you go out of bounds
                return 0

        return sum

    # Calculates the optimal move and value of the given board for the given player.
    # PARAM [board.Board] board: The board state to check.
    # PARAM [int] a: The alpha value for pruning
    # PARAM [int] b: The beta value for pruning
    # PARAM [int] old_action: The column played to reach this board state
    # PARAM [int] player: The player to run the search for [1|2]
    def negamax(self, board, a, b, old_action, depth, player):
        # Cache board outcome, since get_outcome is somewhat expensive to calculate.
        winner = board.get_outcome()
        other_player = (player % 2) + 1
        successors = self.get_successors(board)

        # Immediate win or loss is calculated here to avoid recomputing outcome.
        # It could also be done in get_board_score.

        # Check for immediate win
        if winner == player:
            return 100 / depth, old_action
        # Check for immediate loss
        if winner == other_player:
            return -100 / depth, old_action
        # Max depth, or no successors (tie)
        if depth == self.max_depth or len(successors) == 0:
            return self.get_board_score(board, player, other_player), old_action

        # Standard negamax implementation
        value = float('-inf')
        action = None
        for next_board in self.get_successors(board):
            # It is notable that `nv` is negated every time it is used, this is a key property of negamax.
            nv, new_action = self.negamax(next_board[0], -b, -a, next_board[1], depth + 1, other_player)

            if -nv > value:
                value = -nv
                action = next_board[1]

            a = max(a, value)

            if a >= b:
                return value, new_action

        return value, action

    # Get the successors of the given board in order of middle outwards.
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions (middle favoring)
        freecols = [x for x in self.col_order if brd.board[-1][x] == 0 ]

        # Are there legal actions left?
        if not freecols:
            return []
        
        # Make a list of the new boards along with the corresponding actions
        succ = []
        # print(freecols)
        for col in freecols:
            # Clone the original board
            nb = board.Board([row[:] for row in brd.board], brd.w, brd.h, brd.n)
            nb.player = brd.player

            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ

THE_AGENT = AlphaBetaAgent("Group20", 6)

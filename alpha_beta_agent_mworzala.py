import math
import agent
import time
import board

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    node_avg = []

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.nodes = 0
        self.node_avg = []
        self.col_order = None
    
    def cache_col_order(self, width):
        if self.col_order != None and self.col_order == width:
            return
        self.col_order = list()
        for i in range((width + 1) >> 1, 0, -1):
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

        # Timing
        self.nodes = 0
        start_time = time.perf_counter()
        
        # Minimax
        v, action = self.negamax(brd, float('-inf'), float('inf'), None, 1, brd.player)

        # End Timing
        end_time = time.perf_counter()
        delta_time = end_time - start_time
        self.node_avg.append(self.nodes / delta_time)
        print(f"took {delta_time} seconds visited {self.nodes} nodes did {self.nodes / delta_time} nodes per second")
        
        return action

    def new_eval_board(self, board):
        return 0

    def negamax(self, board, a, b, old_action, depth, player):
        self.nodes += 1

        winner = board.get_outcome()
        other_player = (player % 2) + 1
        successors = self.get_successors(board)

        # Check for immediate win
        if winner == player:
            return 100 / depth, old_action #DEPENDENT ON DEPTH, FLIP!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # Check for immediate loss
        if winner == other_player:
            return -100 / depth, old_action
        # Max depth, or no successors (tie)
        if depth == self.max_depth or len(successors) == 0:
            return self.new_eval_board(board), old_action
        
        # Typical negamax
        value = float('-inf')
        action = None
        for next_board in self.get_successors(board):
            nv, new_action = self.negamax(next_board[0], -b, -a, next_board[1], depth + 1, other_player)
            # if depth == 1:
                # next_board[0].print_it()
                # print("Value:", depth, -nv, "action:", new_action, self.new_eval_board(board), len(self.get_successors(board)))

            if -nv > value:
                value = -nv
                action = next_board[1]
            
            a = max(a, value)

            if a >= b:
                return value, new_action
        
        return value, action

    # Get the successors of the given board.
    #
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

THE_AGENT = AlphaBetaAgent("Group20", 4)

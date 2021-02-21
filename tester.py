import board
import alpha_beta_agent_rs as rust

import connectn

WIDTH   = 3
HEIGHT  = 3
N       = 3

board = board.Board([[2, 2, 1], [1, 2, 2], [0, 1, 1]], WIDTH, HEIGHT, N)
agent = rust.AlphaBetaAgent("rust")


print("BEFORE MOVE")
board.print_it()

action = agent.go(board)
print("\nAFTER MOVE", action)
board.add_token(action)
board.print_it()

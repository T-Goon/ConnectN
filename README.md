# ConnectN

AI to play variable size connect 4, connect N. Both the size of the board and how many tokens are needed to be lined up to win are variable. 

More details can be found in "CS4341_2021_Project1.pdf".
The best AI can be found in "alpha_beta_agent.py".

# Approach

A negamax algorithm with alpha-beta pruning was used along with a custom non-terminal heuristic that mainly acts durring the early phases of the game.

## Non-Terminal Heuristic

The non-terminal heuristic is used to evaluate how good a board state is for the AI as long as that state does not constitute the game ending. The early game is where the negamax non-terminal heuristic does the most. For all of the AI's tokens on the board, the heuristic looks in all eight directions around each token (up, diagonals up, right, diagonals down, etc.) for N-1 spaces. N being the number of tokens you need to line up to win the game. If a free space is encountered the AI adds 1 to the current token's score. If another one of the AI's tokens is encountered 2 is added to that token's score. If the AI ever sees the edge of the game board or an oposing token then the score for that direction is discarded. The score of a board is the sum from looking at all of the AI's token's minus the score from doing the same for the oposing tokens. A diagram of this process for a single token is shown below.

![image](https://user-images.githubusercontent.com/32044950/120863986-88093c80-c559-11eb-80a3-65559fb76f85.png)

## Terminal Heuristic

The terminal heuristic is used to evaluate how good a board state is for the AI when the game has ended in either a win or a loss. If a board state is a win for the AI then its value will be 1000000 / (depth of the negamax search). The negative of that same number will be used if the board is in a losing state. The division by depth is to discount wins and loses that happen further into the future and force the AI to focus on wins and loses that are going to happen sooner. In the later stages of the game it has been observed that this is the main heuristic that determinse the AI's actions.

More details on the AI can be found in "Group20_ConnectN_Writeup.pdf".

# Usage

Edit the "run.py" file to create a game with the differnt AI or human players you want. There are already some set up the just need to be uncommented.

`python run.py`

# Files

## Any .py files that include "agent"

These are different versions of the AI that were created in the development process. The best AI can be found in "alpha_beta_agent.py".

## Other Files

Used to run the Connect N game.


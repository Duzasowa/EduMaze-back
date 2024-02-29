import random

# This code contains functions for a Tic-Tac-Toe game including logic for checking wins, detecting draws, preventing forks, and making moves for the computer. 
# The check_win function checks if a player has achieved a winning condition. The check_draw function checks for a draw by verifying if all cells are filled. 
# The prevent_fork function attempts to block the opponent's forks, where a fork is a position that creates two threats to win.
# The computer_move function encapsulates the computer's strategy to win the game, block the player's win, prevent forks, 
# or make a random move if no immediate winning or blocking move is available.

def check_win(board, player):
    # Define all possible winning conditions
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[2][0], board[1][1], board[0][2]]
    ]
    # Check if any winning condition is met by the current player
    return [player, player, player] in win_conditions

def check_draw(board):
    # Check if all cells on the board are filled, indicating a draw
    return all(cell is not None for row in board for cell in row)

def prevent_fork(board, computer, player):
    # Attempt to find and prevent potential forks by the opponent
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                # Temporarily simulate player's move
                board[i][j] = player
                winning_moves = 0
                for k in range(3):
                    for l in range(3):
                        if board[k][l] is None:
                            board[k][l] = player
                            if check_win(board, player):
                                winning_moves += 1
                            board[k][l] = None
                # If placing a player's piece here creates multiple winning opportunities, block it
                if winning_moves > 1:
                    board[i][j] = computer
                    return (i, j)
                board[i][j] = None
    return None

def computer_move(board, computer, player):
    # First, try to find a winning move for the computer
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = computer
                if check_win(board, computer):
                    return True  # A winning move was made
                board[i][j] = None  # Revert the board back if not a winning move

    # Next, try to block the player's winning move if possible
    for i in range(3):
        for j in range(3):
            if board[i][j] is None:
                board[i][j] = player
                if check_win(board, player):
                    board[i][j] = computer  # Block the player's win
                    return True
                board[i][j] = None

    # Prevent fork strategy to avoid creating a scenario where the opponent can win in multiple ways
    fork_move = prevent_fork(board, computer, player)
    if fork_move:
        board[fork_move[0]][fork_move[1]] = computer
        return True  # A move was made to prevent the fork

    # If no winning or blocking move found, choose a random empty cell
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] is None]
    if empty_cells:
        i, j = random.choice(empty_cells)
        board[i][j] = computer
        return True  # A random move was made
    
    return False  # No moves were made because the board is full, indicating a draw

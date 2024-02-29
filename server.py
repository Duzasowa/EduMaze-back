from flask import Flask, request, jsonify
from flask_cors import CORS
from Maze.MazeAlgorithms.maze_solver_BFS import bfs
from Maze.MazeAlgorithms.maze_solver_DFS import dfs
from Maze.MazeModules.maze_generator import generate_maze
from XOBoard.XOBoardAlgorithms import check_draw
from XOBoard.XOBoardAlgorithms import check_win
from XOBoard.XOBoardAlgorithms import computer_move

app = Flask(__name__)
CORS(app)

@app.route('/xo-move', methods=['POST'])
def xo_move():
    # Parse the incoming JSON data
    data = request.get_json()
    # Extract the current state of the board and the player who made the last move
    board = data['board']
    player = data['player']
    # Attempt to retrieve the move made by the player
    move = data.get('move')
    
    # If a move was specified, try to update the board accordingly
    if move:
        row, col = move
        # Check if the chosen cell is empty
        if board[row][col] is None:
            # If so, apply the player's move to the board
            board[row][col] = player
        else:
            # If the cell is already occupied, return an error
            return jsonify({'error': 'The cell is already occupied'}), 400
    
    # Initialize the game status as 'continue' for further evaluation
    game_status = "continue"
    # Check if the current move resulted in a win for the player
    if check_win(board, player):
        game_status = "win"
    # If not a win, check if the board is full and the game is a draw
    elif check_draw(board):
        game_status = "draw"
    else:
        # If the game is neither win nor draw, it's the computer's turn to make a move
        computer = "O" if player == "X" else "X"
        # Perform the computer's move
        move_made = computer_move(board, computer, player)
        # If the computer didn't make a move (board is full), the game is a draw
        if not move_made:
            game_status = "draw"
        # Otherwise, check if the computer's move resulted in a win
        elif check_win(board, computer):
            game_status = "lose"
    
    # Return the updated board and the current game status
    return jsonify({"board": board, "status": game_status})


@app.route('/get-maze', methods=['POST'])
def main_func():
    # Get data from a POST request
    data = request.get_json()
    width = data.get('width') 
    height = data.get('height')  
    algorithm = data.get('algorithm', 'bfs')  # Default to BFS if not specified

    maze = generate_maze(width, height)
    
    # Define the start and end points
    start, end = (0, 0), (height - 1,width - 1)
    
    # Depending on the algorithm specified, use BFS or DFS
    if algorithm.lower() == 'dfs':
        dfs(maze, start, end)
    else:
        bfs(maze, start, end)

    # Return the maze and path in JSON format
    return maze

if __name__ == '__main__':
    app.run(debug=True)

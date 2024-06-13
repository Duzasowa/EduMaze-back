# EduMaze Project

This project contains a Flask server that handles two main functionalities: playing a Tic-Tac-Toe game and generating/solving mazes.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
  - [POST /xo-move](#post-xo-move)
  - [POST /get-maze](#post-get-maze)
- [Modules](#modules)
  - [XOBoardAlgorithms](#xoboardalgorithms)
  - [MazeAlgorithms](#mazealgorithms)
  - [MazeModules](#mazemodules)
- [License](#license)

## Features

- **Tic-Tac-Toe Game**: Allows users to play a Tic-Tac-Toe game against the computer.
- **Maze Generation and Solving**: Generates a maze and solves it using either BFS or DFS algorithm.

## Installation

1. Install Pipenv:

   ```sh
   pip install pipenv
   ```

2. Install the dependencies:

   ```sh
   pipenv install
   ```

3. Activate the Pipenv virtual environment:

   ```sh
   pipenv shell
   ```

4. Run the Flask server:
   ```sh
   python server.py
   ```

## Usage

To get started with the Flask server:

1. **Start the Flask server:**

   ```sh
   python server.py
   ```

2. The server will run on [http://127.0.0.1:5000/](http://127.0.0.1:5000/) by default.

## API Endpoints

### POST /xo-move

This endpoint processes a move in the Tic-Tac-Toe game.

**Request:**

- **board**: The current state of the Tic-Tac-Toe board (2D array).
- **player**: The player who made the last move (`X` or `O`).
- **move** (optional): The move made by the player ([row, column]).

**Response:**

- **board**: The updated state of the board.
- **status**: The current status of the game (`win`, `draw`, `continue`, `lose`).

**Example request:**

```json
{
  "board": [
    [null, "X", null],
    [null, "O", null],
    [null, null, null]
  ],
  "player": "X",
  "move": [0, 2]
}
```

## POST /get-maze

This endpoint generates a maze and solves it using either BFS (Breadth-First Search) or DFS (Depth-First Search) algorithms.

**Request:**

- **width**: The width of the maze (integer).
- **height**: The height of the maze (integer).
- **algorithm** (optional): The algorithm to use for solving the maze (`bfs` or `dfs`). Defaults to `bfs`.

**Response:**

- A JSON object representing the generated maze with the solution path marked.

**Example request:**

```json
{
  "width": 10,
  "height": 10,
  "algorithm": "dfs"
}
```

## Modules

## XOBoardAlgorithms

This module contains functions for the Tic-Tac-Toe game:

- `check_win(board, player)`: Checks if the specified player has won.
- `check_draw(board)`: Checks if the game is a draw.
- `prevent_fork(board, computer, player)`: Attempts to block the opponent's fork.
- `computer_move(board, computer, player)`: Makes a move for the computer.

### MazeAlgorithms

This module contains functions for solving mazes:

- `dfs(maze, start, end)`: Solves the maze using Depth-First Search.
- `bfs(maze, start, end)`: Solves the maze using Breadth-First Search.

### MazeModules

This module contains functions for generating mazes:

- `generate_maze(width, height)`: Generates a maze with the specified width and height.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### License

This project is licensed under the MIT License.

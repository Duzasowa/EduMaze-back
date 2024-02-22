from flask import Flask, request
import random
from flask_cors import CORS
from collections import deque

app = Flask(__name__)
CORS(app)

def generate_maze(width, height):
    # Create a two-dimensional list (grid), where each cell has a "not visited" state and four walls
    maze = [[{'path': False, 'visited': False, 'walls': [True, True, True, True]} for _ in range(width)] for _ in range(height)]
    
    def remove_wall(x, y, direction):
        # Function for removing walls between cells
        # x, y - coordinates of the current cell, direction - direction to remove the wall
        if direction == 'N':
            # If the direction is north, remove the wall to the north and south of the neighboring cell
            maze[y][x]['walls'][0] = False
            if y > 0:
                maze[y-1][x]['walls'][2] = False
        elif direction == 'E':
            # If the direction is east, remove the wall to the east and west of the neighboring cell
            maze[y][x]['walls'][1] = False
            if x < width - 1:
                maze[y][x+1]['walls'][3] = False
        elif direction == 'S':
            # If the direction is south, remove the wall to the south and north of the neighboring cell
            maze[y][x]['walls'][2] = False
            if y < height - 1:
                maze[y+1][x]['walls'][0] = False
        elif direction == 'W':
            # If the direction is west, remove the wall to the west and east of the neighboring cell
            maze[y][x]['walls'][3] = False
            if x > 0:
                maze[y][x-1]['walls'][1] = False

    def visit_cell(x, y):
        # Mark the cell as visited and select a random order of directions to continue
        maze[y][x]['visited'] = True
        directions = ['N', 'E', 'S', 'W']  # List of possible directions of movement: north, east, south, west
        random.shuffle(directions)  # Shuffle directions for random selection
        
        # We go in every direction
        for direction in directions:
            nx, ny = x, y # nx and ny - the coordinates of the neighboring cell in the direction of direction
           # Determine the coordinates of the neighboring cell depending on the direction
            if direction == 'N':
                ny = y - 1
            elif direction == 'E':
                nx = x + 1
            elif direction == 'S':
                ny = y + 1
            elif direction == 'W':
                nx = x - 1
            
            # If an adjacent cell exists and is not visited, remove the wall and recursively visit this cell
            if 0 <= nx < width and 0 <= ny < height and not maze[ny][nx]['visited']:
                remove_wall(x, y, direction)
                visit_cell(nx, ny)

    # Choose a random starting point for generating the maze
    start_x, start_y = random.randint(0, width-1), random.randint(0, height-1)
    visit_cell(start_x, start_y)  # Start the generation process from the starting point

    return maze # Return the generated maze

# Breadth-First Search algorithm (BFS)
def bfs(maze, start, end):
    queue = deque([(start, [start])])  # Queue will store tuples of (position, path)
    visited = set([start])  # Keep track of visited nodes

    # Directions are N, E, S, W
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    while queue:
        current, path = queue.popleft()
        x, y = current

        if current == end:  # Check if we've reached the end
            for px, py in path:  # Mark the path in the maze
                maze[px][py]['path'] = True
            return maze  # Return the maze with the path marked

        # Check the directions N, E, S, W
        for i, (dx, dy) in enumerate(directions):
            # Calculate the new position based on the direction
            nx, ny = x + dx, y + dy

            # Check if new position is within the bounds of the maze and not blocked by a wall
            if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and not maze[x][y]['walls'][i] and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))  # Add the new position to the queue
                visited.add((nx, ny))  # Mark the new position as visited

    return None  # If no path is found, return None

@app.route('/get-maze', methods=['POST'])
def main_func():
    # Get data from a POST request
    data = request.get_json()
    width = data.get('width') 
    height = data.get('height')  

    maze = generate_maze(width, height)
    
    # Define the start and end points
    start, end = (0, 0), (height - 1,width - 1)
    
    # Finding a way
    path = bfs(maze, start, end)

    # Return the maze and path in JSON format
    return maze

if __name__ == '__main__':
    app.run(debug=True)

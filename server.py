from flask import Flask, request
import random
from flask_cors import CORS
from collections import deque

app = Flask(__name__)
CORS(app)

# This code creates a maze with the specified width and height parameters, where each cell initially has walls on all four sides, 
# and then paths are formed through recursive depth search and random selection of directions.
# After that, the create_additional_paths function adds additional passages to create a more complex maze with several possible paths.
def generate_maze(width, height):
    maze = [[{'path': False, 'visited': False, 'walls': [True, True, True, True]} for _ in range(width)] for _ in range(height)]
    
    def remove_wall(x, y, direction):
        if direction == 'N' and y > 0:
            maze[y][x]['walls'][0] = False
            maze[y-1][x]['walls'][2] = False
        elif direction == 'E' and x < width - 1:
            maze[y][x]['walls'][1] = False
            maze[y][x+1]['walls'][3] = False
        elif direction == 'S' and y < height - 1:
            maze[y][x]['walls'][2] = False
            maze[y+1][x]['walls'][0] = False
        elif direction == 'W' and x > 0:
            maze[y][x]['walls'][3] = False
            maze[y][x-1]['walls'][1] = False

    def visit_cell(x, y):
        maze[y][x]['visited'] = True
        directions = ['N', 'E', 'S', 'W']
        random.shuffle(directions)
        
        for direction in directions:
            nx, ny = x, y
            if direction == 'N':
                ny -= 1
            elif direction == 'E':
                nx += 1
            elif direction == 'S':
                ny += 1
            elif direction == 'W':
                nx -= 1
            
            if 0 <= nx < width and 0 <= ny < height and not maze[ny][nx]['visited']:
                remove_wall(x, y, direction)
                visit_cell(nx, ny)

    def create_additional_paths():
        for _ in range(random.randint(1, width*height//4)):  
            x, y = random.randint(0, width-1), random.randint(0, height-1)
            directions = ['N', 'E', 'S', 'W']
            random.shuffle(directions)
            for direction in directions:
                if direction == 'N' and y > 0:
                    remove_wall(x, y, 'N')
                elif direction == 'E' and x < width - 1:
                    remove_wall(x, y, 'E')
                elif direction == 'S' and y < height - 1:
                    remove_wall(x, y, 'S')
                elif direction == 'W' and x > 0:
                    remove_wall(x, y, 'W')

    start_x, start_y = random.randint(0, width-1), random.randint(0, height-1)
    visit_cell(start_x, start_y)
    create_additional_paths()

    return maze

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

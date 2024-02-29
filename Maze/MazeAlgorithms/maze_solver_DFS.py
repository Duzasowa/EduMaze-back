# This version of the function uses a stack instead of a queue to store the nodes to be visited. 
# This allows the algorithm to move to the most recently added node, facilitating depth-first search.

def dfs(maze, start, end):
    stack = [(start, [start])]  # Stack will store tuples of (position, path)
    visited = set([start])  # Keep track of visited nodes

    # Directions are N, E, S, W
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]

    while stack:
        current, path = stack.pop()  # Use pop to take the last element (LIFO order)
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
                stack.append(((nx, ny), path + [(nx, ny)]))  # Add the new position to the stack
                visited.add((nx, ny))  # Mark the new position as visited

    return None  # If no path is found, return None

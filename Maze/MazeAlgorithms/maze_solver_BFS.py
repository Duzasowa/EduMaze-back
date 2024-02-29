from collections import deque

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
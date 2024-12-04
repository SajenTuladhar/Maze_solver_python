from collections import deque

def bfs(maze, start, end):
    rows = len(maze)
    columns = len(maze[0])
    queue = deque([start])
    visited = set([start])
    parents = {start: None}

    print(f"Starting BFS from {start} to {end}")

    while queue:
        x, y = queue.popleft()
        print(f"Exploring: {x}, {y}")  # Debugging the current cell

        # If we reach the end, reconstruct the path
        if (x, y) == end:
            path = []
            while (x, y) is not None:
                path.append((x, y))
                x, y = parents[(x, y)]
            path = path[::-1]  # Reverse the path
            print(f"Path found: {path}")  # Debug path
            return path

        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < columns and maze[nx][ny] == 0 and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))
                parents[(nx, ny)] = (x, y)

    print("No path found!")  # Debug no path case
    return None

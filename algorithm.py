from collections import deque

def bfs(maze, start, end):
    rows= len(maze)
    colums = len(maze[0])
    queue =deque([start])
    visited = set([start])
    parents= {start: None}  
    
    while queue:
        x,y = queue.popleft()
        
        if(x,y) == end:
            path = []
            while (x, y) is not None:
                path.append((x,y))
                x,y = parents[(x,y)]
            return path[::-1]

        for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
            nx, ny = x + dx , y + dy
            if 0 <= nx < rows and 0 <= ny< colums and maze[nx][ny]==0 and (nx, ny) not in visited:
                queue.append((nx,ny))
                visited.add((nx,ny))
                parents[(nx,ny)] = (x,y)    
        
    return None
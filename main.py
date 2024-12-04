import pygame
import json
from collections import deque

# Constants
GRID_SIZE = 20
CELL_SIZE = 30
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + 90  # Extra space for buttons

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Drawer and Solver")
font = pygame.font.SysFont(None, 30)

# Create the maze grid
maze = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
start, end = (0, 0), (GRID_SIZE - 1, GRID_SIZE - 1)
current_mode = None  # Modes: "start", "end", or None

def draw_grid():
    """Draw the grid and the cells."""
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

    # Highlight start and end
    pygame.draw.rect(screen, BLUE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

def draw_buttons():
    """Draw control buttons."""
    save_button = pygame.Rect(10, GRID_SIZE * CELL_SIZE + 10, 80, 30)
    solve_button = pygame.Rect(100, GRID_SIZE * CELL_SIZE + 10, 80, 30)
    reset_button = pygame.Rect(190, GRID_SIZE * CELL_SIZE + 10, 80, 30)
    start_button = pygame.Rect(280, GRID_SIZE * CELL_SIZE + 10, 100, 30)
    end_button = pygame.Rect(390, GRID_SIZE * CELL_SIZE + 10, 100, 30)

    pygame.draw.rect(screen, BLUE, save_button)
    pygame.draw.rect(screen, GREEN, solve_button)
    pygame.draw.rect(screen, RED, reset_button)
    pygame.draw.rect(screen, YELLOW, start_button)
    pygame.draw.rect(screen, YELLOW, end_button)

    screen.blit(font.render("Save", True, WHITE), (25, GRID_SIZE * CELL_SIZE + 15))
    screen.blit(font.render("Solve", True, WHITE), (115, GRID_SIZE * CELL_SIZE + 15))
    screen.blit(font.render("Reset", True, WHITE), (205, GRID_SIZE * CELL_SIZE + 15))
    screen.blit(font.render("Set Start", True, BLACK), (290, GRID_SIZE * CELL_SIZE + 15))
    screen.blit(font.render("Set End", True, BLACK), (400, GRID_SIZE * CELL_SIZE + 15))

    return save_button, solve_button, reset_button, start_button, end_button

def draw_mode_label():
    """Display the current mode on the screen."""
    mode_label = f"Mode: {'Set Start' if current_mode == 'start' else 'Set End' if current_mode == 'end' else 'Draw Walls'}"
    label_surface = font.render(mode_label, True, BLACK)
    screen.blit(label_surface, (10, GRID_SIZE * CELL_SIZE + 50))

def bfs(start, end):
    """Perform BFS to find the shortest path."""
    queue = deque([start])
    visited = {start}
    parent = {}

    while queue:
        current = queue.popleft()
        if current == end:
            path = []
            while current in parent:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = current[0] + dx, current[1] + dy
            if 0 <= nx < GRID_SIZE and 0 <= ny < GRID_SIZE and (nx, ny) not in visited and maze[nx][ny] == 0:
                queue.append((nx, ny))
                visited.add((nx, ny))
                parent[(nx, ny)] = current

        # Visualization step
        draw_grid()
        pygame.draw.rect(screen, GREEN, (current[1] * CELL_SIZE, current[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(30)
    return None

# Main game loop
running = True
solving = False
while running:
    screen.fill(WHITE)
    draw_grid()
    save_btn, solve_btn, reset_btn, start_btn, end_btn = draw_buttons()
    draw_mode_label()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE

            if y < GRID_SIZE * CELL_SIZE:  # Clicked inside the grid
                if current_mode == "start":
                    start = (grid_y, grid_x)
                    current_mode = None  # Exit Set Start mode
                elif current_mode == "end":
                    end = (grid_y, grid_x)
                    current_mode = None  # Exit Set End mode
                else:
                    maze[grid_y][grid_x] = 1 - maze[grid_y][grid_x]

            elif save_btn.collidepoint(x, y):  # Save button clicked
                with open("maze.json", "w") as f:
                    json.dump(maze, f)
                print("Maze saved!")

            elif solve_btn.collidepoint(x, y):  # Solve button clicked
                solving = True

            elif reset_btn.collidepoint(x, y):  # Reset button clicked
                maze = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
                start, end = (0, 0), (GRID_SIZE - 1, GRID_SIZE - 1)
                solving = False

            elif start_btn.collidepoint(x, y):  # Set Start button clicked
                current_mode = "start"

            elif end_btn.collidepoint(x, y):  # Set End button clicked
                current_mode = "end"

    if solving:
        path = bfs(start, end)
        if path:
            for x, y in path:
                pygame.draw.rect(screen, GREEN, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.display.flip()
                pygame.time.delay(50)
        else:
            print("No path found!")
        solving = False

    pygame.display.flip()

pygame.quit()

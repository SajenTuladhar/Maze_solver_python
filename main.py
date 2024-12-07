import pygame
import random
from collections import deque
from tkinter import filedialog, Tk
from PIL import Image

# Constants
GRID_SIZE = 30
CELL_SIZE = 20
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE
WINDOW_HEIGHT = GRID_SIZE * CELL_SIZE + 130  # Extra space for buttons

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)

solved_path = []

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Maze Solver")
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

    # Highlight the solved path
    if solved_path:
        for x, y in solved_path:
            pygame.draw.rect(screen, GREEN, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Highlight start and end
    pygame.draw.rect(screen, BLUE, (start[1] * CELL_SIZE, start[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, RED, (end[1] * CELL_SIZE, end[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_buttons():
    """Draw control buttons."""
    save_button = pygame.Rect(10, GRID_SIZE * CELL_SIZE + 10, 80, 30)
    solve_button = pygame.Rect(100, GRID_SIZE * CELL_SIZE + 10, 80, 30)
    reset_button = pygame.Rect(190, GRID_SIZE * CELL_SIZE + 10, 80, 30)
    upload_button = pygame.Rect(280, GRID_SIZE * CELL_SIZE + 10, 100, 30)
    random_button = pygame.Rect(390, GRID_SIZE * CELL_SIZE + 10, 180, 30)
    start_button = pygame.Rect(10, GRID_SIZE * CELL_SIZE + 50, 100, 30)
    end_button = pygame.Rect(120, GRID_SIZE * CELL_SIZE + 50, 100, 30)

    pygame.draw.rect(screen, BLACK, save_button)
    pygame.draw.rect(screen, BLACK, solve_button)
    pygame.draw.rect(screen, RED, reset_button)
    pygame.draw.rect(screen, BLACK, upload_button)
    pygame.draw.rect(screen, BLACK, random_button)
    pygame.draw.rect(screen, BLACK, start_button)
    pygame.draw.rect(screen, BLACK, end_button)

    screen.blit(font.render("Save", True, WHITE), (25, GRID_SIZE * CELL_SIZE + 15))
    screen.blit(font.render("Solve", True, WHITE), (115, GRID_SIZE * CELL_SIZE + 15))
    screen.blit(font.render("Reset", True, WHITE), (205, GRID_SIZE * CELL_SIZE + 15))
    screen.blit(font.render("Upload", True, WHITE), (295, GRID_SIZE * CELL_SIZE + 15))
    screen.blit(font.render("Random Maze", True, WHITE), (405, GRID_SIZE * CELL_SIZE + 15))
    screen.blit(font.render("Set Start", True, WHITE), (20, GRID_SIZE * CELL_SIZE + 55))
    screen.blit(font.render("Set End", True, WHITE), (130, GRID_SIZE * CELL_SIZE + 55))

    return save_button, solve_button, reset_button, upload_button, random_button, start_button, end_button

def upload_image():
    """Upload and process an image into the maze grid."""
    Tk().withdraw()  # Hide the Tkinter root window
    filepath = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

    if not filepath:
        print("No file selected!")
        return

    try:
        # Load the image and convert it to grayscale
        img = Image.open(filepath).convert("L")
        print("Image loaded successfully:", filepath)

        # Resize the image to match the grid size
        img = img.resize((GRID_SIZE, GRID_SIZE))
        img_data = img.load()

        # Map the grayscale pixels to the maze grid
        for y in range(GRID_SIZE):
            for x in range(GRID_SIZE):
                pixel = img_data[x, y]
                maze[y][x] = 1 if pixel < 128 else 0  # Threshold for binarization

        # Debug: Print the maze grid to verify the conversion
        print("Maze grid (1 = wall, 0 = path):")
        for row in maze:
            print(row)

        print("Maze updated from image.")
    except Exception as e:
        print("Error processing image:", e)
        
def generate_random_maze():
    """Generate a random maze with random start and end points."""
    global maze, start, end

    # Reset the maze and randomly fill cells
    maze = [[random.choice([0, 1]) for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    # Ensure the start and end are walkable
    start = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    end = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    maze[start[0]][start[1]] = 0
    maze[end[0]][end[1]] = 0

def save_maze_as_image():
    """Save the maze as a PNG image."""
    img = Image.new("RGB", (GRID_SIZE, GRID_SIZE), WHITE)
    pixels = img.load()

    # Map the maze grid to the image pixels
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pixels[x, y] = BLACK if maze[y][x] == 1 else WHITE

    # Highlight start and end points
    pixels[start[1], start[0]] = (0, 0, 255)  # Blue for start
    pixels[end[1], end[0]] = (255, 0, 0)  # Red for end

    # Resize the image for better visibility and save
    img = img.resize((GRID_SIZE * CELL_SIZE, GRID_SIZE * CELL_SIZE), Image.NEAREST)
    save_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png")],
        title="Save Maze As Image"
    )
    if save_path:
        img.save(save_path)
        print(f"Maze saved as: {save_path}")


def bfs(start, end):
    """Perform BFS to find the shortest path with visualization."""
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

        # Visualization step: Draw each cell as it's visited
        draw_grid()
        pygame.draw.rect(screen, GREEN, (current[1] * CELL_SIZE, current[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.display.flip()
        pygame.time.delay(100)  # Adjust the delay for speed
    return None


# Main game loop
running = True
solving = False
while running:
    screen.fill(WHITE)
    draw_grid()
    save_btn, solve_btn, reset_btn, upload_btn, random_btn, start_btn, end_btn = draw_buttons()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x, grid_y = x // CELL_SIZE, y // CELL_SIZE

            if save_btn.collidepoint(x, y):  # Save button clicked
                save_maze_as_image()

            elif solve_btn.collidepoint(x, y):  # Solve button clicked
                solving = True

            elif reset_btn.collidepoint(x, y):  # Reset button clicked
                maze = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
                start, end = (0, 0), (GRID_SIZE - 1, GRID_SIZE - 1)
                solved_path.clear()
                solving = False

            elif upload_btn.collidepoint(x, y):  # Upload button clicked
                upload_image()

            elif random_btn.collidepoint(x, y):  # Random Maze button clicked
                generate_random_maze()

            elif start_btn.collidepoint(x, y):  # Set Start button clicked
                current_mode = "start"
                start = (grid_y, grid_x)

            elif end_btn.collidepoint(x, y):  # Set End button clicked
                current_mode = "end"
                end = (grid_y, grid_x)

            else:
                if current_mode == "start":
                    start = (grid_y, grid_x)
                    current_mode = None
                elif current_mode == "end":
                    end = (grid_y, grid_x)
                    current_mode = None
                else:
                    maze[grid_y][grid_x] = 1 - maze[grid_y][grid_x]

    if solving:
        path = bfs(start, end)
        if path:
            solved_path[:] = path
            for x, y in path:
                pygame.draw.rect(screen, GREEN, (y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE))
                pygame.display.flip()
                pygame.time.delay(80)
        else:
            print("No path found!")
        solving = False

    pygame.display.flip()

pygame.quit()

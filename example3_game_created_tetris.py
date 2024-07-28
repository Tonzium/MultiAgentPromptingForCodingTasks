import random
import pygame
import sys

# Initialize Pygame
pygame.init()

# Set the dimensions of the game window
window_width = 200
window_height = 400
window = pygame.display.set_mode((window_width, window_height))

# Set the title of the game window
pygame.display.set_caption("Tetris")

# Define the colors for the game
colors = {
    "I": (0, 0, 255),     # blue
    "J": (255, 0, 0),     # red
    "L": (0, 255, 0),     # green
    "O": (255, 255, 0),   # yellow
    "S": (255, 0, 255),   # purple
    "T": (255, 128, 0)    # orange
}

# Define the shapes for the game
shape_templates = {
    "I": [[1, 1, 1, 1]],
    "J": [[1, 0, 0], [1, 1, 1]],
    "L": [[0, 0, 1], [1, 1, 1]],
    "O": [[1, 1], [1, 1]],
    "S": [[0, 1, 1], [1, 1, 0]],
    "T": [[0, 1, 0], [1, 1, 1]]
}

# Define the playfield
playfield = [[0 for _ in range(window_width // 20)] for _ in range(window_height // 20)]

# Function to draw the playfield and shapes
def draw_playfield():
    for y in range(window_height // 20):
        for x in range(window_width // 20):
            if playfield[y][x]:
                color = playfield[y][x]
                pygame.draw.rect(window, color, (x * 20, y * 20, 20, 20))

# Function to add shape to the playfield
def add_shape_to_playfield(shape, offset, color):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                playfield[y + off_y][x + off_x] = color

# Function to check collision
def check_collision(shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if y + off_y >= window_height // 20 or x + off_x < 0 or x + off_x >= window_width // 20:
                    return True
                if playfield[y + off_y][x + off_x]:
                    return True
    return False

# Function to clear lines
def clear_lines():
    global playfield
    new_playfield = [row for row in playfield if any(cell == 0 for cell in row)]
    lines_cleared = len(playfield) - len(new_playfield)
    while len(new_playfield) < len(playfield):
        new_playfield.insert(0, [0 for _ in range(window_width // 20)])
    playfield = new_playfield
    return lines_cleared

# Function to rotate the block
def rotate_block(block):
    return [list(row) for row in zip(*block[::-1])]

# Main game loop
clock = pygame.time.Clock()
active_shape_name = random.choice(list(shape_templates.keys()))
active_shape = shape_templates[active_shape_name]
active_color = colors[active_shape_name]
shape_offset = (3, 0)  # Starting position

while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                new_offset = (shape_offset[0] - 1, shape_offset[1])
                if not check_collision(active_shape, new_offset):
                    shape_offset = new_offset
            if event.key == pygame.K_RIGHT:
                new_offset = (shape_offset[0] + 1, shape_offset[1])
                if not check_collision(active_shape, new_offset):
                    shape_offset = new_offset
            if event.key == pygame.K_DOWN:
                new_offset = (shape_offset[0], shape_offset[1] + 1)
                if not check_collision(active_shape, new_offset):
                    shape_offset = new_offset
            if event.key == pygame.K_UP:
                rotated_block = rotate_block(active_shape)
                if not check_collision(rotated_block, shape_offset):
                    active_shape = rotated_block

    # Move shape down
    new_offset = (shape_offset[0], shape_offset[1] + 1)
    if not check_collision(active_shape, new_offset):
        shape_offset = new_offset
    else:
        add_shape_to_playfield(active_shape, shape_offset, active_color)
        if shape_offset[1] <= 1:
            print("Game Over!")
            pygame.quit()
            sys.exit()
        lines_cleared = clear_lines()
        active_shape_name = random.choice(list(shape_templates.keys()))
        active_shape = shape_templates[active_shape_name]
        active_color = colors[active_shape_name]
        shape_offset = (3, 0)

    # Clear the game window
    window.fill((0, 0, 0))

    # Draw the shapes
    draw_playfield()
    for y, row in enumerate(active_shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(window, active_color, ((shape_offset[0] + x) * 20, (shape_offset[1] + y) * 20, 20, 20))

    # Update the game window
    pygame.display.update()

    # Control the speed of the game
    clock.tick(10)
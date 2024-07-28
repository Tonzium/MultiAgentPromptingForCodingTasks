import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Set the screen dimensions
screen_width = 300
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption("Tetris")

# Define the colors
colors = {
    "background": (255, 255, 255),
    "block": (0, 0, 0),
    "line": (255, 0, 0)
}

# Define the block shapes
block_shapes = [
    [[1, 1, 1, 1]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
    [[1, 1, 1], [0, 0, 1]],
    [[1, 1], [1, 1]]
]

# Define the game state
game_state = {
    "score": 0,
    "level": 1,
    "lines_cleared": 0,
    "game_over": False
}

# Define the playfield
playfield = [[0 for _ in range(screen_width // 20)] for _ in range(screen_height // 20)]

# Function to check collision
def check_collision(block, offset):
    off_x, off_y = offset
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= screen_width // 20 or y + off_y >= screen_height // 20:
                    return True
                if playfield[y + off_y][x + off_x]:
                    return True
    return False

# Function to merge block with playfield
def merge_block(block, offset):
    off_x, off_y = offset
    for y, row in enumerate(block):
        for x, cell in enumerate(row):
            if cell:
                playfield[y + off_y][x + off_x] = cell

# Function to clear lines
def clear_lines():
    global playfield, game_state
    new_playfield = [row for row in playfield if any(cell == 0 for cell in row)]
    lines_cleared = len(playfield) - len(new_playfield)
    game_state["lines_cleared"] += lines_cleared
    game_state["score"] += lines_cleared * 100
    while len(new_playfield) < len(playfield):
        new_playfield.insert(0, [0 for _ in range(screen_width // 20)])
    playfield = new_playfield

# Function to rotate block
def rotate_block(block):
    return [list(row) for row in zip(*block[::-1])]

# Define the active block
active_block = random.choice(block_shapes)
block_x, block_y = screen_width // 40 - len(active_block[0]) // 2, 0  # Starting position

# Main game loop
clock = pygame.time.Clock()
while True:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if not check_collision(active_block, (block_x - 1, block_y)):
                    block_x -= 1
            if event.key == pygame.K_RIGHT:
                if not check_collision(active_block, (block_x + 1, block_y)):
                    block_x += 1
            if event.key == pygame.K_DOWN:
                if not check_collision(active_block, (block_x, block_y + 1)):
                    block_y += 1
            if event.key == pygame.K_UP:
                rotated_block = rotate_block(active_block)
                if not check_collision(rotated_block, (block_x, block_y)):
                    active_block = rotated_block

    if not game_state["game_over"]:
        # Move block down
        if not check_collision(active_block, (block_x, block_y + 1)):
            block_y += 1
        else:
            merge_block(active_block, (block_x, block_y))
            clear_lines()
            active_block = random.choice(block_shapes)
            block_x, block_y = screen_width // 40 - len(active_block[0]) // 2, 0
            if check_collision(active_block, (block_x, block_y)):
                game_state["game_over"] = True

        # Draw the game screen
        screen.fill(colors["background"])
        for y, row in enumerate(playfield):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, colors["block"], (x * 20, y * 20, 20, 20))
        for y, row in enumerate(active_block):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, colors["block"], ((block_x + x) * 20, (block_y + y) * 20, 20, 20))
        pygame.display.flip()

        # Wait for a short period of time
        clock.tick(10)  # Control the speed of the game
    else:
        # Draw the game over screen
        screen.fill(colors["background"])
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over!", True, colors["line"])
        screen.blit(text, (screen_width // 4, screen_height // 2))
        pygame.display.flip()
        pygame.time.delay(2000)
        pygame.quit()
        sys.exit()
import pygame
import time
import random

# Initialize the pygame library.
# This sets up everything we need for the game window and graphics.
pygame.init()

# Set the size of the game window (width x height).
window_x = 720
window_y = 480

# Define some colours using RGB values.
black = pygame.Color(0, 0, 0)       # Background colour
white = pygame.Color(255, 255, 255) # Snake and text colour
red = pygame.Color(255, 0, 0)       # Game over text colour
green = pygame.Color(0, 255, 0)     # Snake colour (optional)
blue = pygame.Color(0, 0, 255)      # Food colour

# Create the game window where everything will be displayed.
pygame.display.set_caption('Snake Game')
game_window = pygame.display.set_mode((window_x, window_y))

# Control how fast the snake moves.
fps = pygame.time.Clock()

# Define the initial position of the snake.
snake_position = [100, 50]

# Define the snake's body as a list of segments.
# At the beginning, the snake has 3 blocks (head + 2 parts).
snake_body = [
    [100, 50],
    [90, 50],
    [80, 50]
]

# Set the first position of the food.
food_position = [random.randrange(1, (window_x//10)) * 10,
                 random.randrange(1, (window_y//10)) * 10]
food_spawn = True

# The snake will start moving to the right.
direction = 'RIGHT'
change_to = direction

# Starting score.
score = 0

# Function to display the score in the top-left corner.
def show_score(choice, color, font, size):
    # Choose the font and size for the text.
    score_font = pygame.font.SysFont(font, size)

    # Render the text showing the score value.
    score_surface = score_font.render('Score : ' + str(score), True, color)

    # Get the rectangular area for placing the text.
    score_rect = score_surface.get_rect()

    # Place the score at the top-left corner of the screen.
    game_window.blit(score_surface, score_rect)

# Function to handle "Game Over" situation.
def game_over():
    # Create font for the message.
    my_font = pygame.font.SysFont('times new roman', 50)

    # Render the "Game Over" message.
    game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)

    # Center the message on the screen.
    game_over_rect = game_over_surface.get_rect()
    game_over_rect.midtop = (window_x/2, window_y/4)

    # Draw the message on the screen.
    game_window.blit(game_over_surface, game_over_rect)
    pygame.display.flip()

    # Pause for 2 seconds so the player can read the score.
    time.sleep(2)

    # Quit the game and close the window.
    pygame.quit()
    quit()

# Main game loop: this keeps the game running until the player quits.
while True:
    # Listen for keyboard events (such as arrow keys).
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                change_to = 'UP'
            if event.key == pygame.K_DOWN:
                change_to = 'DOWN'
            if event.key == pygame.K_LEFT:
                change_to = 'LEFT'
            if event.key == pygame.K_RIGHT:
                change_to = 'RIGHT'

    # Ensure the snake cannot immediately move in the opposite direction.
    if change_to == 'UP' and not direction == 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and not direction == 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and not direction == 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and not direction == 'LEFT':
        direction = 'RIGHT'

    # Move the snake in the current direction.
    if direction == 'UP':
        snake_position[1] -= 10
    if direction == 'DOWN':
        snake_position[1] += 10
    if direction == 'LEFT':
        snake_position[0] -= 10
    if direction == 'RIGHT':
        snake_position[0] += 10

    # Add a new head to the snake's body at the updated position.
    snake_body.insert(0, list(snake_position))

    # Check if the snake has eaten the food.
    if snake_position[0] == food_position[0] and snake_position[1] == food_position[1]:
        score += 10   # Increase score by 10.
        food_spawn = False
    else:
        # If the snake didn’t eat food, remove the last segment (so it "moves").
        snake_body.pop()

    # If the food was eaten, generate a new food position.
    if not food_spawn:
        food_position = [random.randrange(1, (window_x//10)) * 10,
                         random.randrange(1, (window_y//10)) * 10]
    food_spawn = True

    # Fill the background with black colour.
    game_window.fill(black)

    # Draw the snake’s body.
    for pos in snake_body:
        pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))

    # Draw the food.
    pygame.draw.rect(game_window, blue, pygame.Rect(food_position[0], food_position[1], 10, 10))

    # Check if the snake touches the boundaries of the window (game over).
    if snake_position[0] < 0 or snake_position[0] > (window_x-10):
        game_over()
    if snake_position[1] < 0 or snake_position[1] > (window_y-10):
        game_over()

    # Check if the snake touches itself (game over).
    for block in snake_body[1:]:
        if snake_position[0] == block[0] and snake_position[1] == block[1]:
            game_over()

    # Display the score.
    show_score(1, white, 'times new roman', 20)

    # Refresh the game screen.
    pygame.display.update()

    # Control the speed of the snake.
    fps.tick(25)
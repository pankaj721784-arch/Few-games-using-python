import tkinter as tk
import random

# Constants
WIDTH = 600
HEIGHT = 400
BALL_SIZE = 20
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
BRICK_ROWS = 5
BRICK_COLS = 8
BRICK_WIDTH = WIDTH // BRICK_COLS
BRICK_HEIGHT = 20

# Globals
ball = None
paddle = None
bricks = []
ball_dx = 4
ball_dy = -4
score = 0
high_score = 0
score_text = None
high_score_text = None
play_again_button = None
game_active = True

# Window and Canvas setup
win = tk.Tk()
win.title("Breakout Game - with High Score and Play Again")

canvas = tk.Canvas(win, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# --- Functions ---

def setup_game():
    global ball, paddle, bricks, ball_dx, ball_dy, score, score_text, game_active, play_again_button

    canvas.delete("all")
    if play_again_button:
        play_again_button.destroy()

    ball_dx = 4
    ball_dy = -4
    score = 0
    game_active = True

    # Create ball
    ball = canvas.create_oval(290, 290, 290 + BALL_SIZE, 290 + BALL_SIZE, fill="white")

    # Create paddle
    paddle = canvas.create_rectangle(250, HEIGHT - 20, 250 + PADDLE_WIDTH, HEIGHT - 10, fill="cyan")

    # Create bricks
    bricks.clear()
    colors = ["red", "orange", "yellow", "green", "blue"]
    for row in range(BRICK_ROWS):
        for col in range(BRICK_COLS):
            x1 = col * BRICK_WIDTH
            y1 = row * BRICK_HEIGHT
            x2 = x1 + BRICK_WIDTH - 2
            y2 = y1 + BRICK_HEIGHT - 2
            brick = canvas.create_rectangle(x1, y1, x2, y2, fill=colors[row % len(colors)], width=1)
            bricks.append(brick)

    # Score and high score text
    score_text = canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 16), text=f"Score: {score}")
    canvas.create_text(10, 30, anchor="nw", fill="white", font=("Arial", 16), text=f"High Score:")
    update_high_score_display()

    game_loop()

def update_high_score_display():
    global high_score_text
    if high_score_text:
        canvas.delete(high_score_text)
    high_score_text = canvas.create_text(100, 30, anchor="nw", fill="lime", font=("Arial", 16), text=f"{high_score}")

def move_left(event):
    if game_active:
        canvas.move(paddle, -20, 0)

def move_right(event):
    if game_active:
        canvas.move(paddle, 20, 0)

def check_collision():
    global ball_dx, ball_dy, score, high_score

    ball_coords = canvas.coords(ball)
    paddle_coords = canvas.coords(paddle)

    # Wall collisions
    if ball_coords[0] <= 0 or ball_coords[2] >= WIDTH:
        ball_dx *= -1
    if ball_coords[1] <= 0:
        ball_dy *= -1

    # Paddle collision
    if (paddle_coords[0] < ball_coords[2] and paddle_coords[2] > ball_coords[0] and
        paddle_coords[1] < ball_coords[3] and paddle_coords[3] > ball_coords[1]):
        ball_dy *= -1

    # Brick collision
    for brick in bricks[:]:
        brick_coords = canvas.coords(brick)
        if (brick_coords[0] < ball_coords[2] and brick_coords[2] > ball_coords[0] and
            brick_coords[1] < ball_coords[3] and brick_coords[3] > ball_coords[1]):
            canvas.delete(brick)
            bricks.remove(brick)
            ball_dy *= -1
            score += 10
            canvas.itemconfig(score_text, text=f"Score: {score}")
            if score > high_score:
                high_score = score
                update_high_score_display()
            break

def end_game(message):
    global game_active, play_again_button
    game_active = False
    canvas.create_text(WIDTH // 2, HEIGHT // 2 - 20, text=message, fill="white", font=("Arial", 30))
    play_again_button = tk.Button(win, text="Play Again", font=("Arial", 14), command=setup_game)
    canvas.create_window(WIDTH // 2, HEIGHT // 2 + 20, window=play_again_button)

def game_loop():
    global game_active

    if not game_active:
        return

    canvas.move(ball, ball_dx, ball_dy)
    check_collision()

    ball_coords = canvas.coords(ball)
    if ball_coords[3] >= HEIGHT:
        end_game("GAME OVER")
        return

    if not bricks:
        end_game("YOU WIN!")
        return

    win.after(20, game_loop)

# --- Key Bindings ---
win.bind("<Left>", move_left)
win.bind("<Right>", move_right)

# --- Start Game ---
setup_game()
win.mainloop()

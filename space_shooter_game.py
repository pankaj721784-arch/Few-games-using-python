import tkinter as tk
import random

# Constants
WIDTH, HEIGHT = 600, 800
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 30
PLAYER_SPEED = 20

# Set up window
win = tk.Tk()
win.title("Space Shooter - Tkinter Edition")

canvas = tk.Canvas(win, width=WIDTH, height=HEIGHT, bg="black")
canvas.pack()

# Game state variables
player = None
bullets = []
enemies = []
score = 0
score_text = None
game_running = True
game_over_text = None
play_again_btn = None

# Functions
def setup_game():
    global player, bullets, enemies, score, score_text, game_running, game_over_text, play_again_btn

    canvas.delete("all")
    bullets.clear()
    enemies.clear()
    score = 0
    game_running = True

    # Create player
    player = canvas.create_rectangle(WIDTH//2 - PLAYER_WIDTH//2, HEIGHT - 60,
                                     WIDTH//2 + PLAYER_WIDTH//2, HEIGHT - 30,
                                     fill="cyan")

    # Create score display
    score_text = canvas.create_text(10, 10, anchor="nw", fill="white", font=("Arial", 20), text="Score: 0")

    # Start game loop and enemy spawn
    spawn_enemy()
    update()

def move_left(event=None):
    if game_running:
        canvas.move(player, -PLAYER_SPEED, 0)

def move_right(event=None):
    if game_running:
        canvas.move(player, PLAYER_SPEED, 0)

def shoot(event=None):
    if not game_running:
        return
    x1, y1, x2, _ = canvas.coords(player)
    bullet = canvas.create_rectangle((x1 + x2)//2 - 2, y1 - 10, (x1 + x2)//2 + 2, y1, fill="yellow")
    bullets.append(bullet)

def spawn_enemy():
    if game_running:
        x = random.randint(0, WIDTH - 40)
        enemy = canvas.create_rectangle(x, 0, x+40, 30, fill="red")
        enemies.append(enemy)
        win.after(1000, spawn_enemy)

def update():
    global score, game_running, game_over_text, play_again_btn

    if not game_running:
        return

    # Move bullets
    for bullet in bullets[:]:
        canvas.move(bullet, 0, -10)
        if canvas.coords(bullet)[1] < 0:
            canvas.delete(bullet)
            bullets.remove(bullet)

    # Move enemies
    for enemy in enemies[:]:
        canvas.move(enemy, 0, 5)
        if canvas.coords(enemy)[3] > HEIGHT:
            canvas.delete(enemy)
            enemies.remove(enemy)

    # Check collisions
    for bullet in bullets[:]:
        for enemy in enemies[:]:
            if is_collision(bullet, enemy):
                canvas.delete(bullet)
                canvas.delete(enemy)
                bullets.remove(bullet)
                enemies.remove(enemy)
                score += 1
                canvas.itemconfig(score_text, text=f"Score: {score}")
                break

    # Check if any enemy hits the player
    px1, py1, px2, py2 = canvas.coords(player)
    for enemy in enemies:
        ex1, ey1, ex2, ey2 = canvas.coords(enemy)
        if not (ex2 < px1 or ex1 > px2 or ey2 < py1 or ey1 > py2):
            game_running = False
            game_over_text = canvas.create_text(WIDTH//2, HEIGHT//2 - 40,
                                                text="GAME OVER", fill="white", font=("Arial", 40))
            play_again_btn = tk.Button(win, text="Play Again", font=("Arial", 16),
                                       command=play_again)
            canvas.create_window(WIDTH//2, HEIGHT//2 + 20, window=play_again_btn)
            return

    win.after(30, update)

def is_collision(a, b):
    ax1, ay1, ax2, ay2 = canvas.coords(a)
    bx1, by1, bx2, by2 = canvas.coords(b)
    return not (ax2 < bx1 or ax1 > bx2 or ay2 < by1 or ay1 > by2)

def play_again():
    global play_again_btn
    if play_again_btn:
        play_again_btn.destroy()
    setup_game()

# Key bindings
win.bind("<Left>", move_left)
win.bind("<Right>", move_right)
win.bind("<space>", shoot)

# Start the first game
setup_game()

# Run the window
win.mainloop()

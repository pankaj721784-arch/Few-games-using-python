import tkinter as tk
import random

# Window settings
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
BIRD_SIZE = 30
PIPE_WIDTH = 60
PIPE_GAP = 150
GRAVITY = 1
JUMP_STRENGTH = -15
UPDATE_DELAY = 30

class FlappyBirdGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird with Tkinter")

        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg='skyblue')
        self.canvas.pack()

        self.bird = self.canvas.create_oval(50, 250, 50 + BIRD_SIZE, 250 + BIRD_SIZE, fill='yellow')

        self.pipes = []
        self.score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor="nw", text="Score: 0", font=("Arial", 18), fill="white")

        self.bird_velocity = 0
        self.game_running = True

        self.root.bind("<space>", self.flap)
        self.root.bind("<r>", self.restart)

        self.spawn_pipe()
        self.update()

    def flap(self, event=None):
        if self.game_running:
            self.bird_velocity = JUMP_STRENGTH

    def restart(self, event=None):
        if not self.game_running:
            self.canvas.delete("all")
            self.bird = self.canvas.create_oval(50, 250, 50 + BIRD_SIZE, 250 + BIRD_SIZE, fill='yellow')
            self.pipes = []
            self.bird_velocity = 0
            self.score = 0
            self.score_text = self.canvas.create_text(10, 10, anchor="nw", text="Score: 0", font=("Arial", 18), fill="white")
            self.game_running = True
            self.spawn_pipe()
            self.update()

    def spawn_pipe(self):
        if not self.game_running:
            return
        top_height = random.randint(50, WINDOW_HEIGHT - PIPE_GAP - 100)
        bottom_y = top_height + PIPE_GAP

        top_pipe = self.canvas.create_rectangle(WINDOW_WIDTH, 0, WINDOW_WIDTH + PIPE_WIDTH, top_height, fill='green')
        bottom_pipe = self.canvas.create_rectangle(WINDOW_WIDTH, bottom_y, WINDOW_WIDTH + PIPE_WIDTH, WINDOW_HEIGHT, fill='green')
        self.pipes.append((top_pipe, bottom_pipe))

        self.root.after(2000, self.spawn_pipe)

    def update(self):
        if not self.game_running:
            return

        # Bird physics
        self.bird_velocity += GRAVITY
        self.canvas.move(self.bird, 0, self.bird_velocity)

        # Bird position
        bird_coords = self.canvas.coords(self.bird)
        bird_x1, bird_y1, bird_x2, bird_y2 = bird_coords

        # Move and check pipes
        new_pipes = []
        for top_pipe, bottom_pipe in self.pipes:
            self.canvas.move(top_pipe, -5, 0)
            self.canvas.move(bottom_pipe, -5, 0)

            top_coords = self.canvas.coords(top_pipe)
            bottom_coords = self.canvas.coords(bottom_pipe)

            # Check for collision
            if (bird_x2 > top_coords[0] and bird_x1 < top_coords[2] and
                (bird_y1 < top_coords[3] or bird_y2 > bottom_coords[1])):
                self.game_over()

            # Check if bird has passed the pipe
            if top_coords[2] < bird_x1 and not self.canvas.gettags(top_pipe):
                self.score += 1
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")
                self.canvas.addtag_withtag("counted", top_pipe)

            # Keep pipe if still on screen
            if top_coords[2] > 0:
                new_pipes.append((top_pipe, bottom_pipe))
            else:
                self.canvas.delete(top_pipe)
                self.canvas.delete(bottom_pipe)

        self.pipes = new_pipes

        # Check if bird hits ground or flies too high
        if bird_y2 >= WINDOW_HEIGHT or bird_y1 <= 0:
            self.game_over()

        if self.game_running:
            self.root.after(UPDATE_DELAY, self.update)

    def game_over(self):
        self.game_running = False
        self.canvas.create_text(WINDOW_WIDTH//2, WINDOW_HEIGHT//2, text="Game Over\nPress 'R' to restart", 
                                font=("Arial", 24), fill="red", justify="center")

# Run game
if __name__ == "__main__":
    root = tk.Tk()
    game = FlappyBirdGame(root)
    root.mainloop()

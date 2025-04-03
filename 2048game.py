import tkinter as tk
import random

# Board size and possible new tile values
SIZE = 4
NEW_TILE_VALUE = [2, 4]

# Core game logic class
class Game2048:
    def __init__(self):
        self.board = [[0] * SIZE for _ in range(SIZE)]  # Initialize 4x4 board
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def reset(self):
        # Reset the board and score
        self.board = [[0] * SIZE for _ in range(SIZE)]
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        # Add a new tile (2 or 4) to a random empty cell
        empty = [(i, j) for i in range(SIZE) for j in range(SIZE) if self.board[i][j] == 0]
        if empty:
            i, j = random.choice(empty)
            self.board[i][j] = random.choice(NEW_TILE_VALUE)

    def compress(self, row):
        # Move all non-zero values to the left and fill the rest with zeros
        new_row = [num for num in row if num != 0]
        new_row += [0] * (SIZE - len(new_row))
        return new_row

    def merge(self, row):
        # Merge identical adjacent tiles
        for i in range(SIZE - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] *= 2
                self.score += row[i]
                row[i + 1] = 0
        return self.compress(row)

    def move_left(self):
        # Handle left move for all rows
        moved = False
        for i in range(SIZE):
            original = list(self.board[i])
            compressed = self.compress(self.board[i])
            merged = self.merge(compressed)
            self.board[i] = merged
            if original != merged:
                moved = True
        if moved:
            self.add_new_tile()
        return moved

    def move_right(self):
        # Reverse each row, move left, then reverse again
        self.board = [row[::-1] for row in self.board]
        moved = self.move_left()
        self.board = [row[::-1] for row in self.board]
        return moved

    def transpose(self):
        # Transpose the board (rows <-> columns)
        self.board = [list(row) for row in zip(*self.board)]

    def move_up(self):
        # Transpose -> move left -> transpose back
        self.transpose()
        moved = self.move_left()
        self.transpose()
        return moved

    def move_down(self):
        # Transpose -> move right -> transpose back
        self.transpose()
        moved = self.move_right()
        self.transpose()
        return moved

    def is_game_over(self):
        # Check if there are no possible moves left
        for i in range(SIZE):
            for j in range(SIZE):
                if self.board[i][j] == 0:
                    return False
                if j < SIZE - 1 and self.board[i][j] == self.board[i][j + 1]:
                    return False
                if i < SIZE - 1 and self.board[i][j] == self.board[i + 1][j]:
                    return False
        return True

# GUI class using tkinter
class GameGUI:
    def __init__(self, root):
        self.root = root
        self.game = Game2048()
        self.cells = []  # 2D list for label references
        self.root.title("2048 Game")
        self.root.bind("<Key>", self.key_handler)  # Bind keyboard arrows
        self.build_interface()
        self.update_grid()

    def build_interface(self):
        # Score display
        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.game.score}",
            font=("Helvetica", 18, "bold"),
            bg="#eee4da",
            fg="#776e65",
            padx=20,
            pady=10,
            relief="groove",
            bd=2
        )
        self.score_label.pack(pady=10)

        # Restart button
        self.restart_button = tk.Button(
            self.root,
            text="Restart",
            command=self.restart_game,
            font=("Helvetica", 14, "bold"),
            bg="#ffa94d",
            fg="white",
            activebackground="#ff922b",
            activeforeground="white",
            bd=0,
            relief="flat",
            padx=10,
            pady=5,
            cursor="hand2"
        )
        self.restart_button.pack(pady=5)

        # Game board frame
        self.background = tk.Frame(self.root, bg="#bbada0")
        self.background.pack(padx=10, pady=10)

        # Create cell labels
        for i in range(SIZE):
            row = []
            for j in range(SIZE):
                cell = tk.Label(self.background, text="", width=4, height=2, font=("Helvetica", 32), bg="#cdc1b4", fg="#776e65")
                cell.grid(row=i, column=j, padx=5, pady=5)
                row.append(cell)
            self.cells.append(row)

    def update_grid(self):
        # Update tile values and score
        self.score_label.config(text=f"Score: {self.game.score}")
        for i in range(SIZE):
            for j in range(SIZE):
                value = self.game.board[i][j]
                self.cells[i][j].config(text=str(value) if value != 0 else "", bg=self.get_color(value))
        if self.game.is_game_over():
            self.show_game_over()

    def restart_game(self):
        # Reset game state and update display
        self.game.reset()
        self.update_grid()
        if hasattr(self, 'game_over_label'):
            self.game_over_label.destroy()

    def key_handler(self, event):
        # Handle key press events
        key = event.keysym
        moved = False
        if key == 'Up':
            moved = self.game.move_up()
        elif key == 'Down':
            moved = self.game.move_down()
        elif key == 'Left':
            moved = self.game.move_left()
        elif key == 'Right':
            moved = self.game.move_right()
        if moved:
            self.update_grid()

    def get_color(self, value):
        # Return background color based on tile value
        colors = {
            0: "#cdc1b4", 2: "#eee4da", 4: "#ede0c8", 8: "#f2b179",
            16: "#f59563", 32: "#f67c5f", 64: "#f65e3b",
            128: "#edcf72", 256: "#edcc61", 512: "#edc850",
            1024: "#edc53f", 2048: "#edc22e"
        }
        return colors.get(value, "#3c3a32")

    def show_game_over(self):
        # Display game over message
        self.game_over_label = tk.Label(self.root, text="Game Over!", font=("Helvetica", 32), bg="#bbada0", fg="white")
        self.game_over_label.place(relx=0.5, rely=0.5, anchor="center")

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game_gui = GameGUI(root)
    root.mainloop()
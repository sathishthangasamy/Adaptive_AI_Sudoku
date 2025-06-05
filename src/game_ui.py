import tkinter as tk
from tkinter import messagebox, font as tkFont
import time # For timer display

class SudokuGUI:
    def __init__(self, master, game_manager):
        self.master = master
        self.game_manager = game_manager
        self.master.title("Adaptive AI Sudoku")
        self.master.geometry("600x700") # Increased height for controls

        self.cells = {} # Dictionary to store Entry widgets
        self.initial_board_values = {} # To store the fixed numbers from the puzzle

        self.create_widgets()
        self.update_timer_label()

    def create_widgets(self):
        # --- Top Frame for Info ---
        self.info_frame = tk.Frame(self.master, pady=5)
        self.info_frame.pack(side=tk.TOP, fill=tk.X)

        self.difficulty_label = tk.Label(self.info_frame, text="Difficulty: Easy", font=("Arial", 12))
        self.difficulty_label.pack(side=tk.LEFT, padx=10)

        self.timer_label = tk.Label(self.info_frame, text="Time: 00:00", font=("Arial", 12))
        self.timer_label.pack(side=tk.RIGHT, padx=10)

        # --- Sudoku Grid Frame ---
        self.grid_frame = tk.Frame(self.master, bg="black", bd=5)
        self.grid_frame.pack(pady=10)

        self.cell_font = tkFont.Font(family="Arial", size=18, weight="bold")
        self.fixed_font = tkFont.Font(family="Arial", size=18, weight="bold")


        for r in range(9):
            for c in range(9):
                bg_color = "#E0E0E0" if ((r // 3) % 2 == (c // 3) % 2) else "#FFFFFF"
                border_width = 1
                relief_style = "solid"

                cell_frame = tk.Frame(self.grid_frame, width=50, height=50, bg=bg_color,
                                       borderwidth=border_width, relief=relief_style)
                cell_frame.grid(row=r, column=c, padx=0, pady=0, sticky="nsew")
                cell_frame.grid_propagate(False) # Prevent cell from resizing based on content

                entry = tk.Entry(cell_frame, width=2, font=self.cell_font, justify='center',
                                 bg=bg_color, bd=0, insertbackground=bg_color,
                                 highlightthickness=0) # No border for entry itself
                entry.pack(expand=True, fill="both")
                entry.bind("<KeyRelease>", lambda event, r=r, c=c: self.on_key_release(event, r, c))
                entry.bind("<FocusOut>", lambda event, r=r, c=c: self.on_focus_out(event, r, c))
                entry.bind("<Button-1>", lambda event, r=r, c=c: self.on_cell_click(event, r, c))
                self.cells[(r, c)] = entry

        # Configure grid to expand equally
        for i in range(9):
            self.grid_frame.grid_rowconfigure(i, weight=1)
            self.grid_frame.grid_columnconfigure(i, weight=1)

        # --- Button Frame ---
        self.button_frame = tk.Frame(self.master, pady=10)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.new_game_button = tk.Button(self.button_frame, text="New Game", command=self.game_manager.new_game, font=("Arial", 12))
        self.new_game_button.pack(side=tk.LEFT, padx=10)

        self.hint_button = tk.Button(self.button_frame, text="Hint", command=self.on_hint, font=("Arial", 12))
        self.hint_button.pack(side=tk.LEFT, padx=10)

        self.solve_button = tk.Button(self.button_frame, text="Solve", command=self.on_solve, font=("Arial", 12))
        self.solve_button.pack(side=tk.LEFT, padx=10)

        self.exit_button = tk.Button(self.button_frame, text="Exit", command=self.master.quit, font=("Arial", 12))
        self.exit_button.pack(side=tk.RIGHT, padx=10)

    def load_board(self, board, initial_board):
        self.initial_board_values.clear()
        for r in range(9):
            for c in range(9):
                entry = self.cells[(r, c)]
                entry.config(state='normal', fg='black') # Ensure editable and default color
                entry.delete(0, tk.END) # Clear previous content

                if initial_board[r][c] != 0:
                    entry.insert(0, str(initial_board[r][c]))
                    entry.config(state='readonly', fg='blue', font=self.fixed_font) # Fixed numbers in blue
                    self.initial_board_values[(r, c)] = initial_board[r][c]
                else:
                    self.initial_board_values[(r, c)] = 0
                    if board[r][c] != 0: # If it's a user-entered number from previous state
                        entry.insert(0, str(board[r][c]))
                        entry.config(fg='black', font=self.cell_font) # User entered in black

    def update_difficulty_label(self, difficulty_str):
        self.difficulty_label.config(text=f"Difficulty: {difficulty_str.capitalize()}")

    def update_timer_label(self):
        elapsed_time = self.game_manager.ai_controller.get_game_time()
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        self.timer_label.config(text=f"Time: {minutes:02d}:{seconds:02d}")
        if not self.game_manager.is_game_over:
            self.master.after(1000, self.update_timer_label)

    def on_key_release(self, event, r, c):
        entry = self.cells[(r, c)]
        current_value = entry.get().strip()

        # Allow empty or single digit 1-9
        if not current_value:
            self.game_manager.update_cell(r, c, 0) # Set to 0 if empty
            entry.config(fg='black') # Reset color if user deletes content
            return

        if len(current_value) > 1 or not current_value.isdigit() or not (1 <= int(current_value) <= 9):
            entry.delete(0, tk.END) # Clear invalid input
            entry.insert(0, "")
            self.game_manager.update_cell(r, c, 0)
            return

        num = int(current_value)
        if not self.game_manager.is_valid_user_move(r, c, num):
            entry.config(fg='red') # Invalid move in red
            self.game_manager.ai_controller.increment_incorrect_attempt()
        else:
            entry.config(fg='black') # Valid move in black

        self.game_manager.update_cell(r, c, num)
        self.check_game_completion()

    def on_focus_out(self, event, r, c):
        # When user clicks out of cell, if it's empty, reset it.
        entry = self.cells[(r, c)]
        if not entry.get().strip():
            self.game_manager.update_cell(r, c, 0)
            entry.config(fg='black') # Ensure color is normal if empty

    def on_cell_click(self, event, r, c):
        # If it's a fixed cell, prevent cursor from appearing (visually)
        if self.initial_board_values[(r, c)] != 0:
            return "break" # Prevents default Tkinter behavior (like showing cursor)

    def check_game_completion(self):
        if self.game_manager.sudoku_board.is_board_full(self.game_manager.sudoku_board.get_board()):
            if self.game_manager.sudoku_board.is_board_solved():
                self.game_manager.game_over(True)
                messagebox.showinfo("Sudoku", "Congratulations! You solved the puzzle!")
            # else:
            #     # Optional: Provide feedback if full but incorrect
            #     messagebox.showerror("Sudoku", "Board is full but not solved. Keep trying!")

    def on_hint(self):
        r, c, num = self.game_manager.get_hint()
        if r is not None:
            entry = self.cells[(r, c)]
            entry.delete(0, tk.END)
            entry.insert(0, str(num))
            entry.config(fg='purple') # Hinted number in purple
            self.game_manager.update_cell(r, c, num)
            self.check_game_completion()
        else:
            messagebox.showinfo("Hint", "No immediate hint available or board is full.")

    def on_solve(self):
        if messagebox.askyesno("Solve", "Are you sure you want to reveal the solution? This will end the current game."):
            self.game_manager.solve_board()
            self.game_manager.game_over(False) # Game over if solved by AI
            messagebox.showinfo("Sudoku", "Puzzle solved by AI!")

    def show_solution(self, solved_board):
        for r in range(9):
            for c in range(9):
                entry = self.cells[(r, c)]
                entry.config(state='normal') # Enable all to show solution
                entry.delete(0, tk.END)
                entry.insert(0, str(solved_board[r][c]))
                if self.initial_board_values[(r,c)] == 0:
                    entry.config(fg='green', font=self.cell_font) # AI-filled in green
                else:
                    entry.config(fg='blue', font=self.fixed_font) # Fixed numbers remain blue
                entry.config(state='readonly') # Make all cells read-only after solving
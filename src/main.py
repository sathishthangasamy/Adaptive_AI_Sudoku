import tkinter as tk
from tkinter import messagebox
from src.sudoku_board import SudokuBoard
from src.sudoku_generator import SudokuGenerator
from src.ai_controller import AIController
from src.sudoku_solver import SudokuSolver # For solving full board
from src.game_ui import SudokuGUI

class GameManager:
    def __init__(self, master):
        self.master = master
        self.sudoku_board = SudokuBoard()
        self.sudoku_generator = SudokuGenerator()
        self.ai_controller = AIController()
        self.sudoku_solver = SudokuSolver() # For full solutions

        self.is_game_over = False         # <--- MOVED THIS LINE UP!
        self.ui = SudokuGUI(master, self)

        self.new_game() # Start a new game automatically

    def new_game(self):
        self.is_game_over = False
        current_difficulty = self.ai_controller.get_current_difficulty()
        new_puzzle = self.sudoku_generator.generate_puzzle(current_difficulty)
        self.sudoku_board.set_board(new_puzzle) # Sets both board and initial_board
        self.ui.load_board(self.sudoku_board.get_board(), self.sudoku_board.get_initial_board())
        self.ai_controller.start_game_timer()
        self.ai_controller.set_initial_puzzle_difficulty(current_difficulty)
        self.ui.update_difficulty_label(current_difficulty)
        self.ui.update_timer_label() # Reset timer display

    def update_cell(self, row, col, num):
        if not self.is_game_over and self.sudoku_board.get_initial_board()[row][col] == 0:
            self.sudoku_board.place_number(row, col, num)
            # Validation handled in UI, but could also be here for console/logic validation

    def is_valid_user_move(self, row, col, num):
        """Checks if a user's entered number is valid at that position."""
        current_board_state = self.sudoku_board.get_board()
        # Temporarily place the number to check its validity
        original_val = current_board_state[row][col]
        current_board_state[row][col] = num
        is_valid = self.sudoku_board.is_valid_move(current_board_state, row, col, num)
        current_board_state[row][col] = original_val # Put back original value
        return is_valid

    def get_hint(self):
        if self.is_game_over:
            return None, None, None

        current_board = self.sudoku_board.get_board()
        initial_board = self.sudoku_board.get_initial_board()
        r, c, num = self.ai_controller.get_hint(current_board, initial_board)
        return r, c, num

    def solve_board(self):
        if self.is_game_over:
            return

        current_board = self.sudoku_board.get_board()
        solved_board_copy = [row[:] for row in current_board]
        if self.sudoku_solver.solve(solved_board_copy):
            self.ui.show_solution(solved_board_copy)
            self.sudoku_board.set_board(solved_board_copy) # Update internal board state
        else:
            messagebox.showerror("Error", "Could not find a solution for the current board.")
    def game_over(self, solved_by_user):
        self.is_game_over = True
        elapsed_time = self.ai_controller.get_game_time()
        empty_cells = sum(row.count(0) for row in self.sudoku_board.get_initial_board()) # Difficulty measure

        if solved_by_user:
            self.ai_controller.adjust_difficulty(elapsed_time, empty_cells)
        # else: if user asks for solve, don't adjust difficulty, maybe penalize score slightly

        # Disable all entry cells
        for r in range(9):
            for c in range(9):
                self.ui.cells[(r, c)].config(state='readonly') # Make all cells read-only

def main():
    root = tk.Tk()
    game = GameManager(root)
    root.mainloop()
if __name__ == "__main__":
    main()
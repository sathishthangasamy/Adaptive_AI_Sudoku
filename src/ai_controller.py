import time
from src.sudoku_solver import SudokuSolver

class AIController:
    def __init__(self):
        self.solver = SudokuSolver()
        # Initialize user's adaptive score and difficulty level
        self.user_difficulty_score = 0
        self.difficulty_levels = ["easy", "medium", "hard"]
        self.current_difficulty_index = 0 # Starts at "easy" (index 0)

        # Game session statistics (reset per game)
        self.start_time = 0
        self.hints_used = 0
        self.incorrect_attempts = 0
        self.initial_puzzle_difficulty = "" # Stores the difficulty of the puzzle generated for the current game

    def start_game_timer(self):
        """Resets and starts the timer and game-specific stats for a new game."""
        self.start_time = time.time()
        self.hints_used = 0
        self.incorrect_attempts = 0

    def get_game_time(self):
        """Returns the elapsed time for the current game."""
        if self.start_time == 0:
            return 0
        return time.time() - self.start_time

    def increment_hint_count(self):
        """Increments the count of hints used in the current game."""
        self.hints_used += 1

    def increment_incorrect_attempt(self):
        """Increments the count of incorrect moves made in the current game."""
        self.incorrect_attempts += 1

    def get_current_difficulty(self):
        """Returns the current target difficulty string."""
        return self.difficulty_levels[self.current_difficulty_index]

    def set_initial_puzzle_difficulty(self, difficulty):
        """Sets the difficulty string of the puzzle that was just generated."""
        self.initial_puzzle_difficulty = difficulty

    def adjust_difficulty(self, game_solved_time_seconds, puzzle_empty_cells):
        """
        Adjusts the user_difficulty_score and current_difficulty_index based on the player's performance
        in the completed game. This uses a heuristic scoring system.
        """
        performance_score = 0

        # --- Time Factor: Reward faster completion, penalize slower times ---
        # Adjusted thresholds to be more sensitive for "easy" games
        if game_solved_time_seconds < 60:  # Solved very quickly (under 1 minute)
            performance_score += 5
        elif game_solved_time_seconds < 180: # Solved decently (under 3 minutes)
            performance_score += 3
        elif game_solved_time_seconds < 480: # Still solved (under 8 minutes)
            performance_score += 1
        else: # Took a long time
            performance_score -= 2

        # --- Hint Factor: Penalize using hints ---
        # Slightly reduced penalty for hints
        performance_score -= self.hints_used * 1.5

        # --- Incorrect Attempts Factor: Penalize wrong inputs ---
        # Slightly reduced penalty for incorrect attempts
        performance_score -= self.incorrect_attempts * 2

        # --- Puzzle Difficulty Bonus: Reward completing harder puzzles ---
        # Increased bonus to encourage progression
        if self.initial_puzzle_difficulty == "easy":
            performance_score += 2
        elif self.initial_puzzle_difficulty == "medium":
            performance_score += 4
        elif self.initial_puzzle_difficulty == "hard":
            performance_score += 6

        # Accumulate the performance score
        self.user_difficulty_score += performance_score

        # --- DEBUGGING OUTPUT (Keep these for testing!) ---
        print(f"\n--- Game Performance Summary ---")
        print(f"Puzzle Difficulty (Generated): {self.initial_puzzle_difficulty.capitalize()}")
        print(f"Time Taken: {game_solved_time_seconds:.2f} seconds")
        print(f"Hints Used: {self.hints_used}")
        print(f"Incorrect Attempts: {self.incorrect_attempts}")
        print(f"Performance Score for this game: {performance_score}")
        print(f"Total User Difficulty Score (Accumulated): {self.user_difficulty_score}")
        print(f"Current Global Difficulty Level (Before Adjustment): {self.get_current_difficulty()}")


        # --- Logic to change global difficulty level ---
        # Lowered the threshold to increase difficulty faster
        if self.user_difficulty_score >= 7 and self.current_difficulty_index < len(self.difficulty_levels) - 1:
            self.current_difficulty_index += 1
            self.user_difficulty_score = 0 # Reset score for new level
            print(f"*** Difficulty INCREASED to {self.get_current_difficulty().upper()}! ***")
        # Slightly adjusted negative threshold to decrease difficulty faster if struggling
        elif self.user_difficulty_score <= -3 and self.current_difficulty_index > 0:
            self.current_difficulty_index -= 1
            self.user_difficulty_score = 0 # Reset score for new level
            print(f"*** Difficulty DECREASED to {self.get_current_difficulty().upper()}! ***")
        elif self.user_difficulty_score < 0:
            # Cap the score at 0 if it goes slightly negative but doesn't warrant a difficulty decrease
            self.user_difficulty_score = 0

        print(f"New Global Difficulty Level (After Adjustment): {self.get_current_difficulty()}")
        print(f"----------------------------------\n")


    def get_hint(self, current_board, initial_board):
        """
        Provides a hint by solving the board and finding the next logical step.
        This is a basic hint system that just finds the first empty cell the solver would fill.
        """
        # Create a solvable copy of the board to find the next valid number
        solvable_board = [row[:] for row in current_board]
        if not self.solver.solve(solvable_board):
            # This should ideally not happen if the puzzle generator ensures unique solutions
            # and the board state is valid up to this point.
            return None, None, None

        # Find the first empty cell that was filled by the solver
        for r in range(9):
            for c in range(9):
                # An empty cell in the current board that was originally empty (not a fixed number)
                # and has been filled by the solver in the solved_board_copy
                if initial_board[r][c] == 0 and current_board[r][c] == 0 and solvable_board[r][c] != 0:
                    self.increment_hint_count()
                    return r, c, solvable_board[r][c]

        return None, None, None # No empty cells or no hint found (e.g., board is already full)
import random
from src.sudoku_solver import SudokuSolver

class SudokuGenerator:
    def __init__(self):
        self.solver = SudokuSolver()

    def generate_full_board(self):
        """Generates a random, valid, solved Sudoku board using backtracking."""
        board = [[0 for _ in range(9)] for _ in range(9)]
        # Recursively fill the board. It needs a starting point, find_empty handles this.
        self._fill_board(board)
        return board

    def _fill_board(self, board):
        """
        Recursive helper function to fill a 9x9 Sudoku board.
        It attempts to place numbers randomly until a full, valid board is achieved.
        """
        find = self.solver.find_empty(board)
        if not find:
            return True  # Board is full

        row, col = find
        nums = list(range(1, 10))
        random.shuffle(nums) # Randomize numbers to get different puzzles each time

        for num in nums:
            if self.solver.is_valid(board, row, col, num):
                board[row][col] = num
                if self._fill_board(board):
                    return True
                board[row][col] = 0  # Backtrack if the current path doesn't lead to a solution

        return False

    def generate_puzzle(self, difficulty_level="medium"):
        """
        Generates a Sudoku puzzle with a unique solution for the player.
        Difficulty levels influence the number of cells removed.

        Args:
            difficulty_level (str): "easy", "medium", or "hard".

        Returns:
            tuple: A tuple containing (puzzle_board, solved_board).
                   puzzle_board is the game board with empty cells (0s).
                   solved_board is the uniquely solved version of the puzzle.
        """
        # First, generate a complete and solved Sudoku board
        solved_board = self.generate_full_board()
        # Create a copy to remove numbers from for the puzzle
        puzzle_board = [row[:] for row in solved_board] 

        # Define the target number of cells to remove based on difficulty
        # These numbers are approximate and can be fine-tuned
        if difficulty_level == "easy":
            cells_to_remove = random.randint(30, 35) # Fewer empty cells, easier to solve
        elif difficulty_level == "medium":
            cells_to_remove = random.randint(45, 50) # Moderate number of empty cells
        elif difficulty_level == "hard":
            cells_to_remove = random.randint(55, 60) # Many empty cells, harder deductions needed
        else: # Default to medium if an unknown level is passed
            cells_to_remove = random.randint(45, 50)

        removed_count = 0
        
        # Create a list of all (row, col) coordinates and shuffle them
        cells_to_consider = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells_to_consider)

        # Iterate through cells and attempt to remove numbers
        for r, c in cells_to_consider:
            if removed_count >= cells_to_remove:
                break # Stop if enough cells have been removed

            original_value = puzzle_board[r][c]
            if original_value == 0: # Skip if already empty
                continue

            # Temporarily remove the number
            puzzle_board[r][c] = 0

            # Check if removing this number maintains a unique solution
            # Create a deep copy to not modify the current puzzle_board during solution counting
            temp_puzzle_copy = [row[:] for row in puzzle_board]
            
            # Count solutions for the board after potential removal
            solutions = self.solver.count_solutions(temp_puzzle_copy)

            if solutions == 1:
                # If a unique solution still exists, keep the cell empty
                removed_count += 1
            else:
                # If not unique (0 or >1 solutions), revert the change
                puzzle_board[r][c] = original_value
        
        # Return both the generated puzzle and its unique solution
        return puzzle_board, solved_board 

if __name__ == '__main__':
    # This block allows you to test the generator independently
    generator = SudokuGenerator()
    test_solver = SudokuSolver()

    print("--- Generating Easy Puzzle ---")
    easy_puzzle, easy_solved = generator.generate_puzzle("easy")
    print("Puzzle:")
    for row in easy_puzzle:
        print(row)
    print(f"Empty cells: {sum(row.count(0) for row in easy_puzzle)}")
    print(f"Solutions (should be 1): {test_solver.count_solutions([row[:] for row in easy_puzzle])}")
    print("\nSolved Version:")
    for row in easy_solved:
        print(row)

    print("\n--- Generating Medium Puzzle ---")
    medium_puzzle, medium_solved = generator.generate_puzzle("medium")
    print("Puzzle:")
    for row in medium_puzzle:
        print(row)
    print(f"Empty cells: {sum(row.count(0) for row in medium_puzzle)}")
    print(f"Solutions (should be 1): {test_solver.count_solutions([row[:] for row in medium_puzzle])}")
    print("\nSolved Version:")
    for row in medium_solved:
        print(row)

    print("\n--- Generating Hard Puzzle ---")
    hard_puzzle, hard_solved = generator.generate_puzzle("hard")
    print("Puzzle:")
    for row in hard_puzzle:
        print(row)
    print(f"Empty cells: {sum(row.count(0) for row in hard_puzzle)}")
    print(f"Solutions (should be 1): {test_solver.count_solutions([row[:] for row in hard_puzzle])}")
    print("\nSolved Version:")
    for row in hard_solved:
        print(row)
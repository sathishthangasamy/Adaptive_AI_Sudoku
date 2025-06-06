import random
from src.sudoku_solver import SudokuSolver

class SudokuGenerator:
    def __init__(self):
        self.solver = SudokuSolver()

    def generate_full_board(self):
        """Generates a random, valid, solved Sudoku board."""
        board = [[0 for _ in range(9)] for _ in range(9)]
        self._fill_board(board)
        return board

    def _fill_board(self, board):
        """Recursively fills the board to create a solved Sudoku."""
        find = self.solver.find_empty(board)
        if not find:
            return True

        row, col = find
        nums = list(range(1, 10))
        random.shuffle(nums) # Randomize numbers for different puzzles

        for num in nums:
            if self.solver.is_valid(board, row, col, num):
                board[row][col] = num
                if self._fill_board(board):
                    return True
                board[row][col] = 0 # Backtrack

        return False

    def generate_puzzle(self, difficulty_level="medium"):
    """
    Generates a Sudoku puzzle with a unique solution.
    Difficulty levels: "easy", "medium", "hard".
    """
    solved_board = self.generate_full_board() # This is the full solved board
    puzzle_board = [row[:] for row in solved_board] # Copy for puzzle creation

        # Define number of cells to remove based on difficulty
        if difficulty_level == "easy":
            cells_to_remove = random.randint(35, 40) # Roughly 41-46 cells remain filled
        elif difficulty_level == "medium":
            cells_to_remove = random.randint(45, 50) # Roughly 31-36 cells remain filled
        elif difficulty_level == "hard":
            cells_to_remove = random.randint(55, 60) # Roughly 21-26 cells remain filled
        else: # Default to medium
            cells_to_remove = random.randint(45, 50)

        # Attempt to remove numbers while ensuring unique solution
        removed_count = 0
        attempts = 0
        max_attempts_per_cell = 100 # Prevent infinite loops for very hard puzzles

        cells = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(cells) # Randomize removal order

        for r, c in cells:
            if removed_count >= cells_to_remove:
                break

            original_value = puzzle_board[r][c]
            if original_value == 0: # Already empty
                continue

            puzzle_board[r][c] = 0 # Temporarily remove

            # Check if removing this number maintains a unique solution
            temp_board_copy = [row[:] for row in puzzle_board]
            if self.solver.count_solutions(temp_board_copy) == 1:
                removed_count += 1
            else:
                puzzle_board[r][c] = original_value # If not unique, put it back

        return puzzle_board, solved_board

if __name__ == '__main__':
    generator = SudokuGenerator()

    print("Generating Easy Puzzle:")
    easy_puzzle = generator.generate_puzzle("easy")
    for r in easy_puzzle:
        print(r)
    print(f"Empty cells: {sum(row.count(0) for row in easy_puzzle)}")
    solver_test = SudokuSolver()
    print(f"Solutions: {solver_test.count_solutions([row[:] for row in easy_puzzle])}")


    print("\nGenerating Medium Puzzle:")
    medium_puzzle = generator.generate_puzzle("medium")
    for r in medium_puzzle:
        print(r)
    print(f"Empty cells: {sum(row.count(0) for row in medium_puzzle)}")
    print(f"Solutions: {solver_test.count_solutions([row[:] for row in medium_puzzle])}")

    print("\nGenerating Hard Puzzle:")
    hard_puzzle = generator.generate_puzzle("hard")
    for r in hard_puzzle:
        print(r)
    print(f"Empty cells: {sum(row.count(0) for row in hard_puzzle)}")
    print(f"Solutions: {solver_test.count_solutions([row[:] for row in hard_puzzle])}")
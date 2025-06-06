import streamlit as st
import time
import random # For potential future enhancements or shuffling lists

# Import your core game logic classes
from src.sudoku_board import SudokuBoard
from src.sudoku_generator import SudokuGenerator
from src.ai_controller import AIController
from src.sudoku_solver import SudokuSolver # Used for validation and hints

# --- Custom CSS for Sudoku Grid Styling ---
# This makes the grid look more like a traditional Sudoku board
st.markdown("""
<style>
.stTextInput > div > div > input {
    font-size: 20px !important;
    text-align: center !important;
    padding: 0 !important;
    margin: 0 !important;
    height: 40px !important; /* Adjust cell height */
    width: 40px !important;  /* Adjust cell width */
    border-radius: 5px;
    border: 1px solid #ccc;
    background-color: white; /* Default background */
    color: black; /* Default text color */
}

/* Style for fixed/initial numbers (read-only cells) */
.fixed-cell {
    background-color: #e0e0e0 !important; /* Light grey */
    font-weight: bold !important;
    color: #4A4A4A !important; /* Darker grey for fixed numbers */
}

/* Borders for 3x3 blocks */
.cell-border-right { border-right: 3px solid black !important; }
.cell-border-bottom { border-bottom: 3px solid black !important; }

/* Remove default Streamlit input padding/margin */
.stTextInput {
    padding: 0;
    margin: 0;
}
.stTextInput label {
    display: none; /* Hide default labels for each cell */
}

/* General layout adjustments */
div.stButton > button {
    font-size: 16px;
    padding: 10px 20px;
    border-radius: 8px;
    box-shadow: 2px 2px 5px rgba(0,0,0,0.2);
}
</style>
""", unsafe_allow_html=True)


# --- Initialize Session State Variables ---
# st.session_state is crucial in Streamlit to persist data across reruns
# It acts like a global dictionary for your app's state.
if 'sudoku_board_obj' not in st.session_state:
    st.session_state.sudoku_board_obj = SudokuBoard()
    st.session_state.sudoku_generator_obj = SudokuGenerator()
    st.session_state.ai_controller_obj = AIController()
    st.session_state.sudoku_solver_obj = SudokuSolver()

    # Board states
    st.session_state.current_board = [[0 for _ in range(9)] for _ in range(9)]
    st.session_state.initial_puzzle = [[0 for _ in range(9)] for _ in range(9)]
    st.session_state.solved_board = [[0 for _ in range(9)] for _ in range(9)] # Full solution for checking

    # Game state
    st.session_state.game_over = False
    st.session_state.timer_running = False
    st.session_state.start_time = 0
    st.session_state.time_elapsed_display = "00:00" # For display
    st.session_state.messages = [] # For user feedback messages

    # Start a new game immediately on first load
    new_game_logic()


# --- Game Logic Functions ---
# These functions will manage the game state and interact with your core logic classes

def new_game_logic():
    """Starts a new game, generates a puzzle, and resets state."""
    st.session_state.game_over = False
    st.session_state.timer_running = True
    st.session_state.start_time = time.time()
    st.session_state.messages = [] # Clear previous messages

    current_difficulty = st.session_state.ai_controller_obj.get_current_difficulty()
    
    # Generate a solved board first, then derive a puzzle from it
    full_solved_board = st.session_state.sudoku_generator_obj.generate_full_board()
    
    # Generate puzzle by removing numbers from the solved board
    # The generate_puzzle method needs to be updated to return the full solved board too.
    # For now, let's just make sure the generator generates a unique solvable puzzle.
    new_puzzle = st.session_state.sudoku_generator_obj.generate_puzzle(current_difficulty)
    
    # A quick way to get the solved board for verification and hints
    temp_solved_for_check = [row[:] for row in new_puzzle]
    st.session_state.sudoku_solver_obj.solve(temp_solved_for_check)
    st.session_state.solved_board = temp_solved_for_check # Store the unique solution

    st.session_state.sudoku_board_obj.set_board(new_puzzle) # Sets current_board and initial_board inside the object
    st.session_state.current_board = st.session_state.sudoku_board_obj.get_board()
    st.session_state.initial_puzzle = st.session_state.sudoku_board_obj.get_initial_board()

    st.session_state.ai_controller_obj.start_game_timer() # Resets timer and stats in AI controller
    st.session_state.ai_controller_obj.set_initial_puzzle_difficulty(current_difficulty)

    st.session_state.messages.append(f"New game started! Difficulty: **{current_difficulty.capitalize()}**")

def update_cell_logic(row, col, value):
    """Handles updating a cell in the game board."""
    if st.session_state.game_over:
        return

    # Only allow updates to cells that were initially empty
    if st.session_state.initial_puzzle[row][col] == 0:
        if value is None or value == "":
            st.session_state.current_board[row][col] = 0
            # No message needed for clearing
        else:
            try:
                num = int(value)
                if 1 <= num <= 9:
                    st.session_state.current_board[row][col] = num
                    # We don't immediately validate here, check_win will do full validation
                else:
                    st.session_state.messages.append("Please enter a digit between 1 and 9.")
                    st.session_state.current_board[row][col] = 0 # Clear invalid input
            except ValueError:
                st.session_state.messages.append("Invalid input. Please enter a number.")
                st.session_state.current_board[row][col] = 0 # Clear non-numeric input
    
    # After any update, re-check for win
    check_win_logic()


def check_win_logic():
    """Checks if the current board is solved and handles game over."""
    current_board_state = st.session_state.current_board
    
    # First, check if the board is full
    if not st.session_state.sudoku_board_obj.is_board_full(current_board_state):
        return False # Not full, game continues

    # If full, check if it's correctly solved against the known solution
    if current_board_state == st.session_state.solved_board:
        st.session_state.game_over = True
        st.session_state.timer_running = False
        
        elapsed_time = time.time() - st.session_state.start_time
        
        # Adjust difficulty based on user's performance
        st.session_state.ai_controller_obj.adjust_difficulty(
            elapsed_time,
            sum(row.count(0) for row in st.session_state.initial_puzzle) # Number of empty cells as a proxy for original difficulty
        )
        
        st.session_state.messages.append(
            f"🎉 Congratulations! You solved the puzzle in {st.session_state.time_elapsed_display}! 🎉"
        )
        # Immediately start a new game after a brief pause
        time.sleep(2) # Give user time to read message
        new_game_logic() # Automatically start next game
        st.experimental_rerun() # Force rerun to show new game
        return True
    else:
        st.session_state.messages.append("Board is full but not solved correctly. Keep trying!")
        return False

def get_hint_logic():
    """Gets a hint from the AI controller and applies it."""
    if st.session_state.game_over:
        st.session_state.messages.append("Game is over. Start a new game for a hint.")
        return

    r, c, num = st.session_state.ai_controller_obj.get_hint(
        st.session_state.current_board,
        st.session_state.initial_puzzle
    )
    
    if r is not None:
        st.session_state.current_board[r][c] = num
        st.session_state.messages.append(f"💡 Hint: Try putting **{num}** at row **{r+1}**, column **{c+1}**.")
        # Mark the cell as hinted if you want special styling
        # st.session_state.hinted_cells.add((r, c)) # Example if you store hinted cells
        st.experimental_rerun() # Force rerun to update the board immediately
    else:
        st.session_state.messages.append("No immediate hint available or board is already complete.")

def solve_board_logic():
    """Fills the board with the solved solution."""
    if st.session_state.game_over:
        st.session_state.messages.append("Game is already over. Start a new game to solve.")
        return

    st.session_state.current_board = [row[:] for row in st.session_state.solved_board]
    st.session_state.game_over = True
    st.session_state.timer_running = False
    st.session_state.messages.append("🤖 Puzzle solved by AI!")
    st.experimental_rerun() # Force rerun to show solved board


# --- Streamlit UI Layout ---
st.set_page_config(layout="wide", page_title="Adaptive AI Sudoku")

st.title("🧠 Adaptive AI Sudoku Game")

# Create two columns for layout: one for the game, one for controls
col_game, col_controls = st.columns([2, 1])

with col_game:
    st.subheader("The Puzzle")

    # Sudoku Grid rendering
    for r in range(9):
        # Create columns for each cell in the row
        cols = st.columns(9)
        for c in range(9):
            current_value = st.session_state.current_board[r][c]
            initial_value = st.session_state.initial_puzzle[r][c]

            is_fixed = (initial_value != 0)
            cell_display_value = str(current_value) if current_value != 0 else ""
            
            # Apply CSS classes for borders
            cell_class = ""
            if (c + 1) % 3 == 0 and c != 8: # Vertical border after 3rd and 6th column
                cell_class += "cell-border-right "
            if (r + 1) % 3 == 0 and r != 8: # Horizontal border after 3rd and 6th row
                cell_class += "cell-border-bottom "
            
            if is_fixed:
                cell_class += "fixed-cell "
            
            # Text input for each cell
            # Using unique keys is essential for Streamlit inputs
            key = f"cell_{r}_{c}_{st.session_state.start_time}" # Add start_time to ensure unique key across games
            
            # The input field itself
            with cols[c]: # Place input in its respective column
                # Using a custom div to apply styling easily
                st.markdown(f'<div class="{cell_class}">', unsafe_allow_html=True)
                new_val = st.text_input(
                    label=f"cell_{r}_{c}", # Label is hidden by CSS
                    value=cell_display_value,
                    max_chars=1,
                    key=key,
                    disabled=is_fixed or st.session_state.game_over,
                    label_visibility="collapsed",
                    # Add on_change to trigger update_cell_logic
                    on_change=update_cell_logic,
                    args=(r, c, st.session_state[key]) # Pass the value from the input field
                )
                st.markdown('</div>', unsafe_allow_html=True)


with col_controls:
    st.subheader("Game Controls & Info")

    # Display Difficulty
    st.write(f"**Current Difficulty:** {st.session_state.ai_controller_obj.get_current_difficulty().capitalize()}")

    # Display Timer
    st.write(f"**Time:** {st.session_state.time_elapsed_display}")

    st.write("---")

    # Buttons
    if st.button("🎲 New Game", use_container_width=True):
        new_game_logic()
        # st.experimental_rerun() # Force rerun to re-render the entire page and refresh inputs

    if st.button("🤔 Get Hint", use_container_width=True, disabled=st.session_state.game_over):
        get_hint_logic()

    if st.button("🤖 Solve Puzzle", use_container_width=True, disabled=st.session_state.game_over):
        if st.session_state.game_over or not st.session_state.timer_running:
            # Game is already over or not started, prevent solving
            st.session_state.messages.append("No active game to solve.")
        else:
            # Confirm dialog (Streamlit doesn't have native confirm, so simulate with buttons)
            confirm_solve = st.empty()
            if confirm_solve.button("Are you sure? This will end the game.", key="confirm_solve"):
                solve_board_logic()
                confirm_solve.empty() # Clear the confirmation button
            else:
                st.session_state.messages.append("Solve cancelled.")
            

    st.write("---")
    st.subheader("Game Messages")
    for msg in st.session_state.messages:
        st.info(msg)

# --- Timer Update Logic ---
# This loop runs constantly while the timer is active to update the display
if st.session_state.timer_running and not st.session_state.game_over:
    elapsed_time = time.time() - st.session_state.start_time
    minutes = int(elapsed_time // 60)
    seconds = int(elapsed_time % 60)
    st.session_state.time_elapsed_display = f"{minutes:02d}:{seconds:02d}"
    
    # Rerun the app every second to update the timer display
    time.sleep(1)
    st.experimental_rerun()
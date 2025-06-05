Adaptive AI Sudoku Game
This is an AI-powered Sudoku game built using Python and Tkinter. It's designed to provide a truly personalized and continuously engaging experience by dynamically adjusting puzzle difficulty based on your performance. No more getting bored by easy puzzles or frustrated by ones that are too hard!

✨ Features
AI-Powered Puzzle Generation: The game intelligently generates unique and solvable Sudoku puzzles for every new game.
Adaptive Difficulty: An integrated AI system tracks your performance (time taken, hints used, incorrect attempts) and seamlessly adjusts the difficulty of the next puzzle. Whether you're a beginner or a Sudoku master, the game evolves with you.
Continuous Gameplay: Enjoy endless challenges! After solving a puzzle, a new one is automatically generated, perfectly calibrated to your current skill level.
Interactive GUI: A user-friendly graphical interface built with Python's Tkinter library, allowing for easy number entry and clear visual feedback.
Hint System: Stuck on a tricky spot? The AI can provide a hint to guide you toward the solution.
Solve Function: Need to see the answer? You can opt to have the AI solve the entire puzzle for you.
🚀 How to Run
Clone the repository:

Bash

git clone https://github.com/YourUsername/sudoku-ai-game.git
cd sudoku-ai-game
(Remember to replace YourUsername with your actual GitHub username and the repository name if it's different!)

Navigate to the src directory:

Bash

cd src
Run the main application:

Bash

python main.py
This will launch the Sudoku game window.

🛠️ Project Structure
The project is modularly designed for clarity and maintainability:

src/sudoku_board.py: Manages the Sudoku board's state, including placing numbers and validating moves.
src/sudoku_solver.py: Implements the core backtracking algorithm used to solve Sudoku puzzles and count unique solutions.
src/sudoku_generator.py: Responsible for creating full, valid Sudoku boards and generating puzzles of varying difficulties by strategically removing numbers.
src/ai_controller.py: The "brain" of the adaptive difficulty system. It tracks player performance, adjusts the internal difficulty score, and determines the next puzzle's challenge level. It also provides hints.
src/game_ui.py: Handles the graphical user interface using Tkinter, rendering the board, accepting user input, and displaying game information.
src/main.py: The central game manager that orchestrates interactions between all other components, managing the overall game flow.
🧠 How the AI Adapts
The AIController continuously evaluates your gameplay based on:

Time taken: How quickly you complete a puzzle.
Hints used: The number of times you request assistance.
Incorrect attempts: How many invalid numbers you try to place.
Based on these metrics, your personal "difficulty score" is adjusted. If you perform well, the next puzzle generated will lean towards a harder setting. If you struggle, the game will offer an easier puzzle to help you get back on track. This creates a truly personalized and dynamic challenge!

💻 Technologies Used
Python 3: The primary programming language.
Tkinter: Python's standard GUI toolkit, used for building the interactive game interface.
💡 Future Enhancements
I'm always looking for ways to improve! Here are some ideas for future development:

Implement a more sophisticated hint system that can explain the logic behind specific solving techniques (e.g., Naked Pairs, Hidden Singles).
Add the ability to save and load game progress.
Introduce different puzzle generation algorithms for even greater variety.
Enhance visual feedback for invalid moves or current active cells.
Customizable themes and styling for the GUI.
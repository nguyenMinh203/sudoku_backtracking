from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont, QColor
from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QGridLayout, QLineEdit, QPushButton, QMessageBox, \
    QHBoxLayout

from sudoku_generator import SudokuGenerator
from sudoku_solver import SudokuSolver


class SudokuGUI(QMainWindow):
    def __init__(self, difficulty, back_to_menu_callback):
        super().__init__()
        self.setWindowTitle("Sudoku")
        self.setGeometry(100, 100, 500, 600)

        self.back_to_menu_callback = back_to_menu_callback

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(5)
        self.main_layout.addLayout(self.grid_layout)

        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                cell = QLineEdit()
                cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
                cell.setFont(QFont("Arial", 18))
                cell.setMaxLength(1)
                cell.setStyleSheet("background-color: white; border: 2px solid #000; border-radius: 5px;")
                self.grid_layout.addWidget(cell, i, j)
                row.append(cell)
            self.cells.append(row)

        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)

        self.check_button = QPushButton("Check")
        self.check_button.setFont(QFont("Arial", 14))
        self.check_button.setStyleSheet("background-color: #FFA500; color: white; border-radius: 5px; padding: 10px;")
        self.check_button.clicked.connect(self.check_solution)
        self.button_layout.addWidget(self.check_button)

        self.solve_button = QPushButton("Solve")
        self.solve_button.setFont(QFont("Arial", 14))
        self.solve_button.setStyleSheet("background-color: #FF6347; color: white; border-radius: 5px; padding: 10px;")
        self.solve_button.clicked.connect(self.solve_sudoku)
        self.button_layout.addWidget(self.solve_button)

        self.new_game_button = QPushButton("New Game")
        self.new_game_button.setFont(QFont("Arial", 14))
        self.new_game_button.setStyleSheet(
            "background-color: #1E90FF; color: white; border-radius: 5px; padding: 10px;")
        self.new_game_button.clicked.connect(self.new_game)
        self.button_layout.addWidget(self.new_game_button)

        self.exit_button = QPushButton("Exit to Menu")
        self.exit_button.setFont(QFont("Arial", 14))
        self.exit_button.setStyleSheet("background-color: #808080; color: white; border-radius: 5px; padding: 10px;")
        self.exit_button.clicked.connect(self.exit_to_menu)
        self.button_layout.addWidget(self.exit_button)

        self.difficulty = difficulty
        self.new_game()

    def new_game(self):
        generator = SudokuGenerator()
        self.grid = generator.generate_puzzle(self.difficulty)
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.cells[i][j].setText(str(self.grid[i][j]))
                    self.cells[i][j].setReadOnly(True)
                    self.cells[i][j].setStyleSheet(
                        "background-color: lightgray; border: 2px solid #000; border-radius: 5px;")
                else:
                    self.cells[i][j].setText("")
                    self.cells[i][j].setReadOnly(False)
                    self.cells[i][j].setStyleSheet(
                        "background-color: white; border: 2px solid #000; border-radius: 5px;")

    def check_solution(self):
        # Reset all cells to their original color
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] != 0:
                    self.cells[i][j].setStyleSheet(
                        "background-color: lightgray; border: 2px solid #000; border-radius: 5px;")
                else:
                    self.cells[i][j].setStyleSheet(
                        "background-color: white; border: 2px solid #000; border-radius: 5px;")

        user_solution = []
        is_complete = True
        incorrect_cells = []

        for i in range(9):
            row = []
            for j in range(9):
                try:
                    val = int(self.cells[i][j].text())
                except ValueError:
                    val = 0
                row.append(val)
                if val == 0:  # Check if there's any empty cell
                    is_complete = False
            user_solution.append(row)

        solver = SudokuSolver(self.grid)
        if solver.solve():
            correct_solution = solver.grid
            incorrect_found = False
            for i in range(9):
                for j in range(9):
                    if user_solution[i][j] != correct_solution[i][j]:
                        self.cells[i][j].setStyleSheet(
                            "background-color: red; border: 2px solid #000; border-radius: 5px;")
                        incorrect_cells.append((i, j))  # Save incorrect cell positions
                        incorrect_found = True

            if incorrect_found:
                QMessageBox.warning(self, "Oops!", "Some cells are incorrect. Please try again.")

                # Restore the incorrect cells to their original state
                for i, j in incorrect_cells:
                    self.cells[i][j].setStyleSheet(
                        "background-color: white; border: 2px solid #000; border-radius: 5px;")
            elif not is_complete:
                QMessageBox.information(self, "Incomplete", "The puzzle is incomplete. Please fill in all the cells.")
            else:
                QMessageBox.information(self, "Congratulations!", "You solved the puzzle correctly!")
        else:
            QMessageBox.warning(self, "Error", "Could not solve the puzzle. Please check your input.")

    def solve_sudoku(self):
        solver = SudokuSolver(self.grid)
        self.solve_steps = solver.solve()
        self.step_index = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.show_next_step)
        self.timer.start(10)  # Thay đổi thời gian (ms) nếu cần

    def show_next_step(self):
        if self.step_index < len(self.solve_steps):
            row, col, num = self.solve_steps[self.step_index]
            if num == 0:
                self.cells[row][col].setText("")
                self.cells[row][col].setStyleSheet(
                    "background-color: white; border: 2px solid #000; border-radius: 5px;")
            else:
                self.cells[row][col].setText(str(num))
                self.cells[row][col].setStyleSheet(
                    "background-color: lightgreen; border: 2px solid #000; border-radius: 5px;")
            self.step_index += 1
        else:
            self.timer.stop()
            QMessageBox.information(self, "Solved", "The puzzle was solved successfully.")

    def exit_to_menu(self):
        self.close()
        self.back_to_menu_callback()

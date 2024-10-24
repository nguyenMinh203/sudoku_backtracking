from PyQt6.QtWidgets import QApplication
from ui.start_screen import StartScreen
from ui.sudoku_gui import SudokuGUI
import sys

class SudokuApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.start_screen = StartScreen(self.start_game)
        self.start_screen.show()

    def start_game(self, difficulty):
        self.sudoku_gui = SudokuGUI(difficulty, self.back_to_menu)
        self.start_screen.close()
        self.sudoku_gui.show()

    def back_to_menu(self):
        self.sudoku_gui.close()
        self.start_screen = StartScreen(self.start_game)
        self.start_screen.show()

if __name__ == "__main__":
    app = SudokuApp(sys.argv)
    sys.exit(app.exec())

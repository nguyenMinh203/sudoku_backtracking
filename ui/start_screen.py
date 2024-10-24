from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QComboBox
from PyQt6.QtGui import QFont, QColor, QPalette
from PyQt6.QtCore import Qt

class StartScreen(QWidget):
    def __init__(self, start_game_callback):
        super().__init__()
        self.start_game_callback = start_game_callback

        self.setWindowTitle("Sudoku Start Screen")
        self.setGeometry(100, 100, 400, 300)

        # Set background color
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, QColor('#f0f8ff'))  # Alice Blue background
        self.setPalette(palette)

        self.layout = QVBoxLayout(self)
        self.layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.setSpacing(20)  # Add spacing between widgets

        self.title_label = QLabel("Welcome to Sudoku!")
        self.title_label.setFont(QFont("Arial", 26, QFont.Weight.Bold))
        self.title_label.setStyleSheet("color: #1e90ff;")  # Dodger Blue color
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.title_label)

        self.difficulty_selector = QComboBox()
        self.difficulty_selector.addItems(["Easy", "Medium", "Hard"])
        self.difficulty_selector.setFont(QFont("Arial", 18))
        self.difficulty_selector.setStyleSheet(
            "background-color: #ffffff; border: 2px solid #1e90ff; border-radius: 5px; padding: 5px;"
        )
        self.layout.addWidget(self.difficulty_selector)

        self.start_button = QPushButton("Start Game")
        self.start_button.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        self.start_button.setStyleSheet(
            "background-color: #32cd32; color: white; border-radius: 5px; padding: 10px;"
        )
        self.start_button.clicked.connect(self.start_game)
        self.layout.addWidget(self.start_button)

    def start_game(self):
        difficulty = self.difficulty_selector.currentText().lower()
        self.start_game_callback(difficulty)

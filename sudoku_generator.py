import random

class SudokuGenerator:
    def __init__(self):
        self.grid = [[0] * 9 for _ in range(9)]

    def fill_grid(self):
        self.fill_diagonal()
        self.fill_remaining(0, 3)

    def fill_diagonal(self):
        for i in range(0, 9, 3):
            self.fill_box(i, i)

    def fill_box(self, row, col):
        num_list = list(range(1, 10))
        random.shuffle(num_list)
        for i in range(3):
            for j in range(3):
                self.grid[row + i][col + j] = num_list.pop()

    def check_if_safe(self, i, j, num):
        return (self.unused_in_row(i, num) and
                self.unused_in_col(j, num) and
                self.unused_in_box(i - i % 3, j - j % 3, num))

    def unused_in_row(self, i, num):
        for j in range(9):
            if self.grid[i][j] == num:
                return False
        return True

    def unused_in_col(self, j, num):
        for i in range(9):
            if self.grid[i][j] == num:
                return False
        return True

    def unused_in_box(self, row_start, col_start, num):
        for i in range(3):
            for j in range(3):
                if self.grid[row_start + i][col_start + j] == num:
                    return False
        return True

    def fill_remaining(self, i, j):
        if j >= 9 and i < 8:
            i += 1
            j = 0
        if i >= 9 and j >= 9:
            return True

        if i < 3:
            if j < 3:
                j = 3
        elif i < 6:
            if j == (i // 3) * 3:
                j += 3
        else:
            if j == 6:
                i += 1
                j = 0
                if i >= 9:
                    return True

        for num in random.sample(range(1, 10), 9):
            if self.check_if_safe(i, j, num):
                self.grid[i][j] = num
                if self.fill_remaining(i, j + 1):
                    return True
                self.grid[i][j] = 0

        return False

    def remove_digits(self, difficulty):
        # Adjust number of cells to remove based on difficulty
        if difficulty == 'easy':
            cells_to_remove = 40
        elif difficulty == 'medium':
            cells_to_remove = 50
        else:  # 'hard'
            cells_to_remove = 60

        while cells_to_remove > 0:
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            if self.grid[i][j] != 0:
                self.grid[i][j] = 0
                cells_to_remove -= 1

    def generate_puzzle(self, difficulty):
        self.fill_grid()
        self.remove_digits(difficulty)
        return self.grid

class SudokuSolver:
    def __init__(self, grid):
        self.grid = grid
        self.solve_steps = []  # To store steps

    def is_valid(self, row, col, num):
        # Kiểm tra hàng
        for x in range(9):
            if self.grid[row][x] == num:
                return False

        # Kiểm tra cột
        for x in range(9):
            if self.grid[x][col] == num:
                return False

        # Kiểm tra ô 3x3
        start_row = row - row % 3
        start_col = col - col % 3
        for i in range(3):
            for j in range(3):
                if self.grid[i + start_row][j + start_col] == num:
                    return False

        return True

    def solve(self):
        self.solve_steps = []  # Clear previous steps
        self._solve()
        return self.solve_steps

    def _solve(self):
        empty = self.find_empty_location()
        if not empty:
            return True

        row, col = empty

        for num in range(1, 10):
            if self.is_valid(row, col, num):
                self.grid[row][col] = num
                self.solve_steps.append((row, col, num))  # Store step
                if self._solve():
                    return True
                self.grid[row][col] = 0
                self.solve_steps.append((row, col, 0))  # Remove step

        return False

    def find_empty_location(self):
        for i in range(9):
            for j in range(9):
                if self.grid[i][j] == 0:
                    return (i, j)
        return None

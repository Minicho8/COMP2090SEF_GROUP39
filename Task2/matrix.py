class Matrix:
    def __init__(self, mrows, ncols):
        self.mrows = mrows
        self.ncols = ncols
        self.grid = [[0 for _ in range(ncols)] for _ in range(mrows)]
    
# Get value of rows and column
    def get_value(self, r, c):
        return self.grid[r][c]
# Set item at rows and column    
    def set_value(self, r, c, s):
        if 0 <= r < self.mrows and 0 <= c < self.ncols:
            self.grid[r][c] = s
# Transpose of matrix
    def transpose(self):
        new_matrix = Matrix(self.ncols, self.mrows)
        for r in range(self.mrows):
            for c in range(self.ncols):
                new_matrix.set_value(c, r, self.grid[r][c])
        return new_matrix
# Create a matrix
my_matrix = Matrix(2, 3)
# Fill it with some values
my_matrix.set_value(0, 0, 1)
my_matrix.set_value(0, 1, 2)
my_matrix.set_value(0, 2, 3)
my_matrix.set_value(1, 0, 4)
my_matrix.set_value(1, 1, 5)
my_matrix.set_value(1, 2, 6)
#transpose
transposed = my_matrix.transpose()

#output
print("Original Matrix:")
for row in my_matrix.grid:
    print(row)
print("\nTransposed Matrix (3x2):")
for row in transposed.grid:
    print(row)

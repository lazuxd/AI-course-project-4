class Sudoku:
    def __init__(self, initial_config: str):
        self.board = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(int(initial_config[9*i+j]))
            self.board.append(row)
    
    def __repr__(self):
        s = ''
        for i in range(9):
            for j in range(9):
                s += str(self.board[i][j])
        return s
    
    def __str__(self):
        s = ''
        for i in range(9):
            if i % 3 == 0:
                s += ('-'*25)+'\n'
                s += (' '*25)+'\n'
            l = ''
            for j in range(9):
                if j % 3 == 0:
                    l += '| '
                l += str(self.board[i][j]) + ' '
            l += '|\n'
            s += l
            s += (' '*25)+'\n'
        s += ('-'*25)+'\n'
        
        return s
    
    def get_copy(self):
        return Sudoku(repr(self))
    
    def get_box(self, i, j):
        x1 = (j//3)*3
        x2 = x1+3
        y1 = (i//3)*3
        y2 = y1+3
        return (x1, y1, x2, y2)
    
    def get_box_index(self, i, j):
        x = (j//3)*3
        y = (i//3)*3
        return y*3+x
    
    def is_digit_in_row(self, digit, row):
        for i in range(9):
            if digit == self.board[row][i]:
                return True
        return False
    
    def is_digit_in_column(self, digit, column):
        for i in range(9):
            if digit == self.board[i][column]:
                return True
        return False
    
    def is_digit_in_box(self, digit, i, j):
        (x1, y1, x2, y2) = self.get_box(i, j)
        for k in range(x1, x2):
            for l in range(y1, y2):
                if digit == self.board[l][k]:
                    return True
        return False
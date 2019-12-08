from Sudoku import Sudoku
from ac3 import ac3
from bts import bts
from sys import argv

def solve_sudoku(board: str):
    sudoku = Sudoku(board)
    result = ac3(sudoku)
    if result == None:
        result = bts(sudoku)
        return f'{repr(result)} BTS'
    else:
        return f'{repr(result)} AC3'

if __name__ == '__main__':
    if len(argv) < 2:
        print('You forgot the command line argument!')
        exit()
    print(solve_sudoku(argv[1]))

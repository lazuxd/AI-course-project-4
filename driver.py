from Sudoku import Sudoku
from ac3 import ac3
from bts import bts


if __name__ == '__main__':
    sudoku = Sudoku('000000000302540000050301070000000004409006005023054790000000050700810000080060009')
    print('Representation: ' + repr(sudoku))
    print('Readable string:\n' + str(sudoku))
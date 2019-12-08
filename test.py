from driver import solve_sudoku


if __name__ == '__main__':
    i = 1
    with open('sudokus_start.txt', 'r') as fin:
        with open('sudokus_output.txt', 'w') as fout:
            for line in fin:
                print(f'{i} / 400')
                fout.write(f'{solve_sudoku(line.rstrip())}\n')
                i += 1

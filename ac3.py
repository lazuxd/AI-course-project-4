from typing import Union
from collections import deque
from Sudoku import Sudoku

def ac3(sudoku: Sudoku) -> Union[Sudoku, None]:
    sudoku = sudoku.get_copy()
    queue = deque()
    sudoku.fill_queue_with_arcs(queue)

    while len(queue) != 0:
        (xi, xj) = queue.pop()
        if revise(sudoku, xi, xj):
            if sudoku.get_size_of_domain(xi) == 0:
                return None
            for xk in sudoku.get_neighbors(xi):
                if (xk, xi) not in queue:
                    queue.appendleft((xk, xi))
    
    if sudoku.are_all_domains_single_valued():
        sudoku.do_assignment_from_domains()
        return sudoku
    else:
        return None

def revise(sudoku: Sudoku, xi: int, xj: int) -> bool:
    revised = False

    for x in sudoku.get_domain(xi):
        if not sudoku.is_x_valid(x, xi, xj):
            sudoku.remove_from_domain(x, xi)
            revised = True
    
    return revised
from typing import Union
from Sudoku import Sudoku

def bts(sudoku: Sudoku) -> Union[Sudoku, None]:
    sudoku = sudoku.get_copy()
    return backtrack(sudoku)

def backtrack(sudoku: Sudoku) -> Union[Sudoku, None]:
    if sudoku.is_assignment_complete():
        return sudoku
    
    old_domains = sudoku.get_domains()

    var = sudoku.select_unassigned_variable()
    for val in sudoku.get_domain(var):
        if sudoku.is_assignment_consistent(var, val):
            sudoku.add_to_assignments(var, val)
            result = backtrack(sudoku)
            if result != None:
                return result
            sudoku.remove_from_assignments(var, val, old_domains)
    
    return None
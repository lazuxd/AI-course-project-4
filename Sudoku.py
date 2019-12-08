from typing import List, Set
from collections import deque
from copy import deepcopy
from heapq import heappush, heappop, heapify

class Sudoku:
    def __init__(self, initial_config: str):
        self.board = []
        for i in range(9):
            row = []
            for j in range(9):
                row.append(int(initial_config[9*i+j]))
            self.board.append(row)
        
        self.domains: List[Set] = []
        for k in range(81):
            i = k // 9
            j = k % 9
            if self.board[i][j] != 0:
                self.domains.append(set([self.board[i][j]]))
            else:
                self.domains.append(set([i for i in range(1, 10)]))
        
        for i in range(9):
            for j in range(9):
                if self.board[i][j] != 0:
                    for k in range(9):
                        if j != k and self.board[i][j] in self.domains[i*9+k]:
                            self.domains[i*9+k].remove(self.board[i][j])
                        if i != k and self.board[i][j] in self.domains[k*9+j]:
                            self.domains[k*9+j].remove(self.board[i][j])
                    (x1, y1, x2, y2) = self.get_box(i, j)
                    for k in range(y1, y2):
                        for l in range(x1, x2):
                            if i != k and j != l and self.board[i][j] in self.domains[k*9+l]:
                                self.domains[k*9+l].remove(self.board[i][j])
        
        self.assignable_variables = []
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    heappush(self.assignable_variables, (len(self.domains[i*9+j]), i*9+j))
    
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
    
    def get_domains(self):
        return deepcopy(self.domains)
    
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
    
    def fill_queue_with_arcs(self, queue: deque):
        for i in range(9):
            for j in range(9):
                xi = i*9+j
                for nb in self.get_neighbors(xi):
                    queue.appendleft((xi, nb))

    def get_size_of_domain(self, xi):
        return len(self.domains[xi])
    
    def get_neighbors(self, xi) -> List[int]:
        i = xi // 9
        j = xi % 9
        neighbors = []

        for k in range(9):
            if j != k:
                neighbors.append(i*9+k)
        for k in range(9):
            if i != k:
                neighbors.append(k*9+j)
        (x1, y1, x2, y2) = self.get_box(i, j)
        for l in range(y1, y2):
            for k in range(x1, x2):
                if i != l and j != k:
                    neighbors.append(l*9+k)
        
        return neighbors
    
    def get_domain(self, xi):
        return deepcopy(self.domains[xi])
    
    def is_row_valid(self, row):
        for j in range(9):
            if self.board[row][j] == 0:
                continue
            for k in range(j+1, 9):
                if self.board[row][j] == self.board[row][k]:
                    return False
        return True
    
    def is_col_valid(self, col):
        for i in range(9):
            if self.board[i][col] == 0:
                continue
            for k in range(i+1, 9):
                if self.board[i][col] == self.board[k][col]:
                    return False
        return True
    
    def is_box_valid(self, i, j):
        (x1, y1, x2, y2) = self.get_box(i, j)

        for k in range(y1, y2):
            for l in range(x1, x2):
                if self.board[k][l] == 0:
                    continue
                for u in range(y1, y2):
                    for v in range(x1, x2):
                        if u*9+v <= k*9+l:
                            continue
                        if self.board[k][l] == self.board[u][v]:
                            return False
        
        return True
    
    def is_valid(self, i, j):
        return self.is_row_valid(i) and self.is_col_valid(j) and self.is_box_valid(i, j)
    
    def is_x_valid(self, x, xi, xj):
        dj = self.domains[xj]
        i1 = xi // 9
        j1 = xi % 9
        i2 = xj // 9
        j2 = xj % 9

        for y in dj:
            old_x = self.board[i1][j1]
            old_y = self.board[i2][j2]
            self.board[i1][j1] = x
            self.board[i2][j2] = y
            if self.is_valid(i1, j1) and self.is_valid(i2, j2):
                self.board[i1][j1] = old_x
                self.board[i2][j2] = old_y
                return True
            self.board[i1][j1] = old_x
            self.board[i2][j2] = old_y
        
        return False
    
    def remove_from_domain(self, val, xi):
        if val in self.domains[xi]:
            self.domains[xi].remove(val)
    
    def are_all_domains_single_valued(self):
        for i in range(81):
            if len(self.domains[i]) != 1:
                return False
        return True
    
    def do_assignment_from_domains(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    val = self.domains[i*9+j].pop()
                    self.domains[i*9+j].add(val)
                    self.board[i][j] = val

    def get_number_of_assignable_variables(self):
        return len(self.assignable_variables)

    def is_assignment_complete(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return False
        return True
    
    def select_unassigned_variable(self) -> int:
        return self.assignable_variables[0][1]
    
    def is_assignment_consistent(self, var, val):
        
        for nb in self.get_neighbors(var):

            if self.board[nb//9][nb%9] == val:
                return False

            # Forward Checking
            if len(self.domains[nb]) == 1 and val in self.domains[nb]:
                return False
        
        return True
    
    def add_to_assignments(self, var, val):
        self.board[var//9][var%9] = val
        heappop(self.assignable_variables)
        self.domains[var] = set([val])
        for nb in self.get_neighbors(var):
            if val in self.domains[nb]:
                idx = self.assignable_variables.index((len(self.domains[nb]), nb))
                self.domains[nb].remove(val)
                self.assignable_variables[idx] = (len(self.domains[nb]), nb)

        heapify(self.assignable_variables)
    
    def remove_from_assignments(self, var, val, old_domains: List[Set]):
        self.board[var//9][var%9] = 0
        self.domains[var] = deepcopy(old_domains[var])
        heappush(self.assignable_variables, (len(self.domains[var]), var))

        for nb in self.get_neighbors(var):
            if val in old_domains[nb]:
                idx = self.assignable_variables.index((len(self.domains[nb]), nb))
                self.domains[nb].add(val)
                self.assignable_variables[idx] = (len(self.domains[nb]), nb)

        heapify(self.assignable_variables)

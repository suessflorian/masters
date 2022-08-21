import sys
import time
sys.path.insert(0, "./aipython")
from aipython.searchGeneric import *
from aipython.searchProblem import *
from aipython.cspProblem import *
from aipython.cspSearch import *

grid = [[9, 5, 0, 8, 2, 7, 3, 0, 0], #A
        [0, 8, 0, 1, 4, 0, 0, 5, 0], #B
        [0, 1, 0, 5, 9, 0, 0, 0, 0], #C
        [8, 3, 0, 0, 0, 0, 0, 7, 5], #D
        [1, 6, 9, 7, 5, 2, 4, 3, 0], #E
        [0, 7, 0, 0, 8, 0, 0, 6, 0], #F
        [0, 9, 1, 0, 6, 0, 8, 4, 0], #G
        [7, 0, 8, 0, 3, 1, 0, 0, 6], #H
        [6, 2, 0, 4, 7, 8, 0, 9, 0]] #I
    #    1  2  3  4  5  6  7  8  9

def grid_to_csp(grid):
    """returns a soduko constraint satisfaction problem"""
    rows, cols = 'ABCDEFGHI', '123456789'
    
    domain = {}
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            square_index = rows[row_index] + cols[col_index]
            if value == 0: # we interpret zero's as being anything
                  domain[square_index] = Variable(square_index, {1, 2, 3, 4, 5, 6, 7, 8, 9})
                  continue
            # anything else is the starter value hence reducing the domain to just that value
            domain[square_index] = Variable(square_index, {value})

    def cross_product(Rows,Cols): return [a + b for a in Rows for b in Cols]
    def variable_groups_in_same_col(): return [map(lambda square: domain[square], cross_product(rows, col)) for col in cols]
    def variable_groups_in_same_row(): return [map(lambda square: domain[square], cross_product(row, cols)) for row in rows]
    def variable_groups_in_same_box(): return [map(lambda square: domain[square], cross_product(box_rows, box_cols)) for box_rows in ('ABC','DEF','GHI') for box_cols in ('123','456','789')]

    variable_groups = variable_groups_in_same_col() + variable_groups_in_same_row() + variable_groups_in_same_box() 

    constraints = []
    def not_equal(x,y): return x != y
    for variable_group in variable_groups:
        variables = list(variable_group)
        for i in range(0, len(variables)):
            for j in range(i+1, len(variables)):
                constraints.append(Constraint([variables[i], variables[j]], not_equal))

    return CSP("soduku", {variable for _, variable in domain.items()}, constraints)

class Backtracking_Search_from_CSP(Search_problem):
    def __init__(self, csp):
        self.csp=csp
        self.variables = list(csp.variables)
        self.variables.sort(key=lambda variable: len(variable.domain))

    def is_goal(self, node):
        return len(node)==len(self.csp.variables)
    
    def start_node(self):
        return {}
    
    def neighbors(self, node):
        var = self.variables[len(node)]
        neighbours: list[Arc] = []
        for val in var.domain:
            
            new_assignment = dict_union(node, {var:val})
            if self.csp.consistent(new_assignment):
                neighbours.append(Arc(node, new_assignment))
        return neighbours


csp_problem = grid_to_csp(grid)
variables = list(csp_problem.variables)
variables.sort(key=lambda variable: len(variable.domain))

# search_problem = Search_from_CSP(csp_problem, variables)
search_problem = Backtracking_Search_from_CSP(csp_problem)
dfs = Searcher(search_problem)

start = time.process_time()
dfs.search()
print(f"Time taken: {time.process_time() - start}s")

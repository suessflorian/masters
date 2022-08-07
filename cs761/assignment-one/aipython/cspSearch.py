# cspSearch.py - Representations of a Search Problem from a CSP.
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from cspProblem import CSP, Constraint
from searchProblem import Arc, Search_problem
from utilities import dict_union

class Search_from_CSP(Search_problem):
    """A search problem directly from the CSP.

    A node is a variable:value dictionary"""
    def __init__(self, csp, variable_order=None):
        self.csp=csp
        if variable_order:
            assert set(variable_order) == set(csp.variables)
            assert len(variable_order) == len(csp.variables)
            self.variables = variable_order
        else:
            self.variables = list(csp.variables)

    def is_goal(self, node):
        """returns whether the current node is a goal for the search
        """
        return len(node)==len(self.csp.variables)
    
    def start_node(self):
        """returns the start node for the search
        """
        return {}
    
    def neighbors(self, node):
        """returns a list of the neighboring nodes of node.
        """
        var = self.variables[len(node)] # the next variable
        res = []
        for val in var.domain:
            new_env = dict_union(node,{var:val})  #dictionary union
            if self.csp.consistent(new_env):
                res.append(Arc(node,new_env))
        return res

from cspExamples import csp1,csp2,test_csp, crossword1, crossword1d
from searchGeneric import Searcher

def solver_from_searcher(csp):
    """depth-first search solver"""
    path = Searcher(Search_from_CSP(csp)).search()
    if path is not None:
        return path.end()
    else:
        return None

if __name__ == "__main__":
    test_csp(solver_from_searcher)

## Test Solving CSPs with Search:
searcher1 = Searcher(Search_from_CSP(csp1))
#print(searcher1.search())  # get next solution
searcher2 = Searcher(Search_from_CSP(csp2))
#print(searcher2.search())  # get next solution
searcher3 = Searcher(Search_from_CSP(crossword1))
#print(searcher3.search())  # get next solution
searcher4 = Searcher(Search_from_CSP(crossword1d))
#print(searcher4.search())  # get next solution (warning: slow)


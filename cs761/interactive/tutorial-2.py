from aipython import searchGeneric
from aipython import searchProblem

searcher = searchGeneric.Searcher(searchProblem.acyclic_delivery_problem)
print("Path found: ", searcher.search(), "costs=", searcher.solution.cost)

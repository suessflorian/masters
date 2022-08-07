# cspExamples.py - Example CSPs
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from cspProblem import Variable, CSP, Constraint        
from operator import lt,ne,eq,gt

def ne_(val):
    """not equal value"""
    # nev = lambda x: x != val   # alternative definition
    # nev = partial(neq,val)     # another alternative definition
    def nev(x):
        return val != x
    nev.__name__ = str(val)+"!="      # name of the function 
    return nev

def is_(val):
    """is a value"""
    # isv = lambda x: x == val   # alternative definition
    # isv = partial(eq,val)      # another alternative definition
    def isv(x):
        return val == x
    isv.__name__ = str(val)+"=="
    return isv

X = Variable('X', {1,2,3})
Y = Variable('Y', {1,2,3})
Z = Variable('Z', {1,2,3})
csp0 = CSP("csp0", {X,Y,Z},
           [ Constraint([X,Y],lt),
             Constraint([Y,Z],lt)])

A = Variable('A', {1,2,3,4}, position=(0.2,0.9))
B = Variable('B', {1,2,3,4}, position=(0.8,0.9))
C = Variable('C', {1,2,3,4}, position=(1,0.4))
C0 = Constraint([A,B], lt, "A < B", position=(0.4,0.3))
C1 = Constraint([B], ne_(2), "B != 2", position=(1,0.9))
C2 = Constraint([B,C], lt, "B < C", position=(0.6,0.1))
csp1 = CSP("csp1", {A, B, C},
           [C0, C1, C2])

D = Variable('D', {1,2,3,4}, position=(0,0.4))
E = Variable('E', {1,2,3,4}, position=(0.5,0))
csp2 = CSP("csp2", {A,B,C,D,E},
           [ Constraint([B], ne_(3), "B != 3", position=(1,0.9)),
            Constraint([C], ne_(2), "C != 2", position=(1,0.2)),
            Constraint([A,B], ne, "A != B"),
            Constraint([B,C], ne, "A != C"),
            Constraint([C,D], lt, "C < D"),
            Constraint([A,D], eq, "A = D"),
            Constraint([A,E], gt, "A > E"),
            Constraint([B,E], gt, "B > E"),
            Constraint([C,E], gt, "C > E"),
            Constraint([D,E], gt, "D > E"),
            Constraint([B,D], ne, "B != D")])

csp3 = CSP("csp3", {A,B,C,D,E},
           [Constraint([A,B], ne, "A != B"),
            Constraint([A,D], lt, "A < D"),
            Constraint([A,E], lambda a,e: (a-e)%2 == 1, "A-E is odd"), # A-E is odd
            Constraint([B,E], lt, "B < E"),
            Constraint([D,C], lt, "D < C"),
            Constraint([C,E], ne, "C != E"),
            Constraint([D,E], ne, "D != E")])

def adjacent(x,y):
   """True when x and y are adjacent numbers"""
   return abs(x-y) == 1

csp4 = CSP("csp4", {A,B,C,D,E},
           [Constraint([A,B], adjacent, "adjacent(A,B)"),
            Constraint([B,C], adjacent, "adjacent(B,C)"),
            Constraint([C,D], adjacent, "adjacent(C,D)"),
            Constraint([D,E], adjacent, "adjacent(D,E)"),
            Constraint([A,C], ne, "A != C"),
            Constraint([B,D], ne, "B != D"),
            Constraint([C,E], ne, "C != E")])

def meet_at(p1,p2):
    """returns a function of two words that is true 
                 when the words intersect at postions p1, p2.
    The positions are relative to the words; starting at position 0.
    meet_at(p1,p2)(w1,w2) is true if the same letter is at position p1 of word w1 
         and at position p2 of word w2.
    """
    def meets(w1,w2):
        return w1[p1] == w2[p2]
    meets.__name__ = "meet_at("+str(p1)+','+str(p2)+')'
    return meets

one_across = Variable('one_across', {'ant', 'big', 'bus', 'car', 'has'}, position=(0.3,0.9))
one_down = Variable('one_down', {'book', 'buys', 'hold', 'lane', 'year'}, position=(0.1,0.7))
two_down = Variable('two_down', {'ginger', 'search', 'symbol', 'syntax'}, position=(0.9,0.8))
three_across = Variable('three_across', {'book', 'buys', 'hold', 'land', 'year'}, position=(0.1,0.3))
four_across = Variable('four_across',{'ant', 'big', 'bus', 'car', 'has'}, position=(0.7,0.0))
crossword1 = CSP("crossword1",
                  {one_across, one_down, two_down, three_across, four_across},
                  [Constraint([one_across,one_down], meet_at(0,0)),
                   Constraint([one_across,two_down], meet_at(2,0)),
                   Constraint([three_across,two_down], meet_at(2,2)),
                   Constraint([three_across,one_down], meet_at(0,2)),
                   Constraint([four_across,two_down], meet_at(0,4))])

words = {'ant', 'big', 'bus', 'car', 'has','book', 'buys', 'hold',
         'lane', 'year', 'ginger', 'search', 'symbol', 'syntax'}
           
def is_word(*letters, words=words):
    """is true if the letters concatenated form a word in words"""
    return "".join(letters) in words

letters = {"a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
  "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y",
  "z"}

# pij is the variable representing the letter i from the left and j down (starting from 0)
p00 = Variable('p00',  letters, position=(0.1,0.85))
p10 = Variable('p10',  letters, position=(0.3,0.85))
p20 = Variable('p20',  letters, position=(0.5,0.85))
p01 = Variable('p01',  letters, position=(0.1,0.7))
p21 = Variable('p21',  letters, position=(0.5,0.7))
p02 = Variable('p02',  letters, position=(0.1,0.55))
p12 = Variable('p12',  letters, position=(0.3,0.55))
p22 = Variable('p22',  letters, position=(0.5,0.55))
p32 = Variable('p32',  letters, position=(0.7,0.55))
p03 = Variable('p03',  letters, position=(0.1,0.4))
p23 = Variable('p23',  letters, position=(0.5,0.4))
p24 = Variable('p24',  letters, position=(0.5,0.25))
p34 = Variable('p34',  letters, position=(0.7,0.25))
p44 = Variable('p44',  letters, position=(0.9,0.25))
p25 = Variable('p25',  letters, position=(0.5,0.1))

crossword1d = CSP("crossword1d",
                  {p00, p10, p20, # first row
                   p01, p21,  # second row
                   p02, p12, p22, p32, # third row
                   p03, p23, #fourth row
                   p24, p34, p44, # fifth row
                   p25 # sixth row
                   },
                  [Constraint([p00, p10, p20], is_word, position=(0.3,0.95)), #1-across
                   Constraint([p00, p01, p02, p03], is_word, position=(0,0.625)), # 1-down
                   Constraint([p02, p12, p22, p32], is_word, position=(0.3,0.625)), # 3-across
                   Constraint([p20, p21, p22, p23, p24, p25], is_word, position=(0.45,0.475)), # 2-down
                   Constraint([p24, p34, p44], is_word, position=(0.7,0.325)) # 4-across
                   ])
               
def queens(ri,rj):
    """ri and rj are different rows, return the condition that the queens cannot take each other"""
    def no_take(ci,cj):
        """is true if queen at (ri,ci) cannot take a queen at (rj,cj)"""
        return ci != cj and abs(ri-ci) != abs(rj-cj)
    return no_take

def n_queens(n):
    """returns a CSP for n-queens"""
    columns = list(range(n))
    variables = [Variable(f"R{i}",columns) for i in range(n)]
    return CSP("n-queens",
               variables,
                [Constraint([variables[i], variables[j]], queens(i,j))
                     for i in range(n) for j in range(n) if i != j])

# try the CSP  n_queens(8) in one of the solvers.
# What is the smallest n for which there is a solution?

def test_csp(CSP_solver, csp=csp1,
             solutions=[{A: 1, B: 3, C: 4}, {A: 2, B: 3, C: 4}]):
    """CSP_solver is a solver that takes a csp and returns a solution
    csp is a constraint satisfaction problem
    solutions is the list of all solutions to csp
    This tests whether the solution returned by CSP_solver is a solution.
    """
    print("Testing csp with",CSP_solver.__doc__)
    sol0 = CSP_solver(csp)
    print("Solution found:",sol0)
    assert sol0 in solutions, "Solution not correct for "+str(csp)
    print("Passed unit test")


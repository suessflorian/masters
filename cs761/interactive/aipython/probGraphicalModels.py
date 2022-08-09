# probGraphicalModels.py - Graphical Models and Belief Networks
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from display import Displayable
from probFactors import CPD
import matplotlib.pyplot as plt

class GraphicalModel(Displayable):
    """The class of graphical models. 
    A graphical model consists of a title, a set of variables and a set of factors.

    vars is a set of variables
    factors is a set of factors
    """
    def __init__(self, title, variables=None, factors=None):
        self.title = title
        self.variables = variables
        self.factors = factors

class BeliefNetwork(GraphicalModel):
    """The class of belief networks."""

    def __init__(self, title, variables, factors):
        """vars is a set of variables
        factors is a set of factors. All of the factors are instances of CPD (e.g., Prob).
        """
        GraphicalModel.__init__(self, title, variables, factors)
        assert all(isinstance(f,CPD) for f in factors)
        self.var2cpt = {f.child:f for f in factors}
        self.var2parents = {f.child:f.parents for f in factors}
        self.children = {n:[] for n in self.variables}
        for v in self.var2parents:
            for par in self.var2parents[v]:
                self.children[par].append(v)
        self.topological_sort_saved = None

    def topological_sort(self):
        """creates a topological ordering of variables such that the parents of 
        a node are before the node.
        """
        if self.topological_sort_saved:
            return self.topological_sort_saved
        next_vars = {n for n in self.var2parents if not self.var2parents[n] }
        self.display(3,'topological_sort: next_vars',next_vars)
        top_order=[]
        while next_vars:
            var = next_vars.pop()
            self.display(3,'select variable',var)
            top_order.append(var)
            next_vars |= {ch for ch in self.children[var]
                              if all(p in top_order for p in self.var2parents[ch])}
            self.display(3,'var_with_no_parents_left',next_vars)
        self.display(3,"top_order",top_order)
        assert set(top_order)==set(self.var2parents),(top_order,self.var2parents)
        self.topologicalsort_saved=top_order
        return top_order
    
    def show(self):
        plt.ion()   # interactive
        ax = plt.figure().gca()
        ax.set_axis_off()
        plt.title(self.title)
        bbox = dict(boxstyle="round4,pad=1.0,rounding_size=0.5")
        for var in reversed(self.topological_sort()):
            if self.var2parents[var]:
                for par in self.var2parents[var]:
                    ax.annotate(var.name, par.position, xytext=var.position,
                                    arrowprops={'arrowstyle':'<-'},bbox=bbox,
                                    ha='center')
            else:
                x,y = var.position
                plt.text(x,y,var.name,bbox=bbox,ha='center')

from probVariables import Variable
from probFactors import Prob, LogisticRegression, NoisyOR

boolean = [False, True]
A = Variable("A", boolean, position=(0,0.8))
B = Variable("B", boolean, position=(0.333,0.6))
C = Variable("C", boolean, position=(0.666,0.4))
D = Variable("D", boolean, position=(1,0.2))

f_a = Prob(A,[],[0.4,0.6])
f_b = Prob(B,[A],[[0.9,0.1],[0.2,0.8]])
f_c = Prob(C,[B],[[0.6,0.4],[0.3,0.7]])
f_d = Prob(D,[C],[[0.1,0.9],[0.75,0.25]])

bn_4ch = BeliefNetwork("4-chain", {A,B,C,D}, {f_a,f_b,f_c,f_d})

# Belief network report-of-leaving example (Example 8.15 shown in Figure 8.3) of
# Poole and Mackworth, Artificial Intelligence, 2017 http://artint.info

Alarm =   Variable("Alarm",   boolean,  position=(0.366,0.633))
Fire =    Variable("Fire",    boolean,  position=(0.633,0.9))
Leaving = Variable("Leaving", boolean,  position=(0.366,0.366))
Report =  Variable("Report",  boolean,  position=(0.366,0.1))
Smoke =   Variable("Smoke",   boolean,  position=(0.9,0.633))
Tamper =  Variable("Tamper",  boolean,  position=(0.1,0.9))

f_ta = Prob(Tamper,[],[0.98,0.02])
f_fi = Prob(Fire,[],[0.99,0.01])
f_sm = Prob(Smoke,[Fire],[[0.99,0.01],[0.1,0.9]])
f_al = Prob(Alarm,[Fire,Tamper],[[[0.9999, 0.0001], [0.15, 0.85]], [[0.01, 0.99], [0.5, 0.5]]])
f_lv = Prob(Leaving,[Alarm],[[0.999, 0.001], [0.12, 0.88]])
f_re = Prob(Report,[Leaving],[[0.99, 0.01], [0.25, 0.75]])

bn_report = BeliefNetwork("Report-of-leaving", {Tamper,Fire,Smoke,Alarm,Leaving,Report},
                              {f_ta,f_fi,f_sm,f_al,f_lv,f_re})

Season = Variable("Season", ["summer","winter"],  position=(0.5,0.9))
Sprinkler = Variable("Sprinkler", ["on","off"],  position=(0.9,0.6))
Rained = Variable("Rained", boolean,  position=(0.1,0.6))
Grass_wet = Variable("Grass wet", boolean,  position=(0.5,0.3))
Grass_shiny = Variable("Grass shiny", boolean,  position=(0.1,0))
Shoes_wet = Variable("Shoes wet", boolean,  position=(0.9,0))

f_season = Prob(Season,[],{'summer':0.5, 'winter':0.5})
f_sprinkler = Prob(Sprinkler,[Season],{'summer':{'on':0.9,'off':0.1},
                                       'winter':{'on':0.01,'off':0.99}})
f_rained = Prob(Rained,[Season],{'summer':[0.9,0.1], 'winter': [0.2,0.8]})
f_wet = Prob(Grass_wet,[Sprinkler,Rained], {'on': [[0.1,0.9],[0.01,0.99]],
                                            'off':[[0.99,0.01],[0.3,0.7]]})
f_shiny = Prob(Grass_shiny, [Grass_wet], [[0.95,0.05], [0.3,0.7]])
f_shoes = Prob(Shoes_wet, [Grass_wet], [[0.98,0.02], [0.35,0.65]])

bn_sprinkler = BeliefNetwork("Pearl's Sprinkler Example",
                         {Season, Sprinkler, Rained, Grass_wet, Grass_shiny, Shoes_wet},
                         {f_season, f_sprinkler, f_rained, f_wet, f_shiny, f_shoes})

bn_sprinkler_soff = BeliefNetwork("Pearl's Sprinkler Example (do(Sprinkler=off))",
                         {Season, Sprinkler, Rained, Grass_wet, Grass_shiny, Shoes_wet},
                         {f_season, f_rained, f_wet, f_shiny, f_shoes,
                              Prob(Sprinkler,[],{'on':0,'off':1})})

Cough = Variable("Cough", boolean, (0.1,0.1))
Fever = Variable("Fever", boolean, (0.5,0.1))
Sneeze = Variable("Sneeze", boolean, (0.9,0.1))
Cold = Variable("Cold",boolean, (0.1,0.9))
Flu = Variable("Flu",boolean, (0.5,0.9))
Covid = Variable("Covid",boolean, (0.9,0.9))

p_cold_no = Prob(Cold,[],[0.9,0.1])
p_flu_no = Prob(Flu,[],[0.95,0.05])
p_covid_no = Prob(Covid,[],[0.99,0.01])

p_cough_no = NoisyOR(Cough,   [Cold,Flu,Covid], [0.1,  0.3,  0.2,  0.7])
p_fever_no = NoisyOR(Fever,   [     Flu,Covid], [0.01,       0.6,  0.7])
p_sneeze_no = NoisyOR(Sneeze, [Cold,Flu      ], [0.05,  0.5,  0.2    ])

bn_no1 = BeliefNetwork("Bipartite Diagnostic Network (noisy-or)",
                         {Cough, Fever, Sneeze, Cold, Flu, Covid},
                          {p_cold_no, p_flu_no, p_covid_no, p_cough_no, p_fever_no, p_sneeze_no})  

# to see the conditional probability of Noisy-or do:
# print(p_cough_no.to_table())

# example from box "Noisy-or compared to logistic regression"
# X = Variable("X",boolean)
# w0 = 0.01
# print(NoisyOR(X,[A,B,C,D],[w0, 1-(1-0.05)/(1-w0), 1-(1-0.1)/(1-w0), 1-(1-0.2)/(1-w0), 1-(1-0.2)/(1-w0), ]).to_table(given={X:True}))


p_cold_lr = Prob(Cold,[],[0.9,0.1])
p_flu_lr = Prob(Flu,[],[0.95,0.05])
p_covid_lr = Prob(Covid,[],[0.99,0.01])

p_cough_lr =  LogisticRegression(Cough,  [Cold,Flu,Covid], [-2.2,  1.67,  1.26,  3.19])
p_fever_lr =  LogisticRegression(Fever,  [     Flu,Covid], [-4.6,         5.02,  5.46])
p_sneeze_lr = LogisticRegression(Sneeze, [Cold,Flu      ], [-2.94, 3.04,  1.79    ])

bn_lr1 = BeliefNetwork("Bipartite Diagnostic Network -  logistic regression",
                         {Cough, Fever, Sneeze, Cold, Flu, Covid},
                          {p_cold_lr, p_flu_lr, p_covid_lr, p_cough_lr, p_fever_lr, p_sneeze_lr})  

# to see the conditional probability of Noisy-or do:
#print(p_cough_lr.to_table())

# example from box "Noisy-or compared to logistic regression"
# from learnLinear import sigmoid, logit
# w0=logit(0.01)
# X = Variable("X",boolean)
# print(LogisticRegression(X,[A,B,C,D],[w0, logit(0.05)-w0, logit(0.1)-w0, logit(0.2)-w0, logit(0.2)-w0]).to_table(given={X:True}))
# try to predict what would happen (and then test) if we had
# w0=logit(0.01)

from display import Displayable

class InferenceMethod(Displayable):
    """The abstract class of graphical model inference methods"""
    method_name = "unnamed"  # each method should have a method name

    def __init__(self,gm=None):
        self.gm = gm

    def query(self, qvar, obs={}):
        """returns a {value:prob} dictionary for the query variable"""
        raise NotImplementedError("InferenceMethod query")   # abstract method

    def testIM(self, threshold=0.0000000001):
        solver = self(bn_4ch)
        res = solver.query(B,{D:True})
        correct_answer = 0.429632380245
        assert correct_answer-threshold < res[True] < correct_answer+threshold, \
                f"value {res[True]} not in desired range for {self.method_name}"
        print(f"Unit test passed for {self.method_name}.")
    

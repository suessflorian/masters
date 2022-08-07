# probRC.py - Recursive Conditioning for Graphical Models
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import math
from probGraphicalModels import GraphicalModel, InferenceMethod
from probFactors import Factor
from utilities import dict_union

class ProbSearch(InferenceMethod):
    """The class that queries graphical models using recursive conditioning

    gm is graphical model to query
    """
    method_name = "recursive conditioning"
 
    def __init__(self,gm=None):
        InferenceMethod.__init__(self, gm)
        ## self.max_display_level = 3

    def query(self, qvar, obs={}, split_order=None):
        """computes P(qvar | obs) where
        qvar is the query variable
        obs is a variable:value dictionary
        split_order is a list of the non-observed non-query variables in gm
        """
        if qvar in obs:
            return {val:(1 if val == obs[qvar] else 0) for val in qvar.domain}
        else:
           if split_order == None:
                split_order = [v for v in self.gm.variables if (v not in obs) and v != qvar]
           unnorm = [self.prob_search(dict_union({qvar:val},obs), self.gm.factors, split_order)
                         for val in qvar.domain]
           p_obs = sum(unnorm)
           return {val:pr/p_obs for val,pr in zip(qvar.domain, unnorm)}

    def prob_search(self, context, factors, split_order):
        """simple search algorithm
        context is a variable:value dictionary
        factors is a set of factors
        split_order is a list of variables in factors not assigned in context
        returns sum over variable assignments to variables in split order or product of factors """
        self.display(2,"calling prob_search,",(context,factors))
        if not factors:
            return 1
        elif to_eval := {fac for fac in factors if fac.can_evaluate(context)}:
            # evaluate factors when all variables are assigned
            self.display(3,"prob_search evaluating factors",to_eval)
            val = math.prod(fac.get_value(context) for fac in to_eval)
            return val * self.prob_search(context, factors-to_eval, split_order)
        else:
            total = 0
            var = split_order[0]
            self.display(3, "prob_search branching on", var)
            for val in var.domain:
                total += self.prob_search(dict_union({var:val},context), factors, split_order[1:])
            self.display(3, "prob_search branching on", var,"returning", total)
            return total

class ProbRC(ProbSearch):
    def __init__(self,gm=None):
        self.cache = {(frozenset(), frozenset()):1}
        ProbSearch.__init__(self,gm)
  
    def prob_search(self, context, factors, split_order):
        """ returns the number \sum_{split_order} \prod_{factors} given assignments in context
        context is a variable:value dictionary
        factors is a set of factors
        split_order is a list of variables in factors that are not assigned in context
        returns sum over variable assignments to variables in split_order
                    of the product of factors 
        """
        self.display(3,"calling rc,",(context,factors))
        ce = (frozenset(context.items()),  frozenset(factors))  # key for the cache entry
        if ce in self.cache:
            self.display(3,"rc cache lookup",(context,factors))
            return self.cache[ce]
#        if not factors:  # no factors; needed if you don't have forgetting and caching
#            return 1
        elif vars_not_in_factors := {var for var in context
                                         if not any(var in fac.variables for fac in factors)}:
             # forget variables not in any factor
            self.display(3,"rc forgetting variables", vars_not_in_factors)
            return self.prob_search({key:val for (key,val) in context.items()
                                if key not in vars_not_in_factors},
                            factors, split_order)
        elif to_eval := {fac for fac in factors if fac.can_evaluate(context)}:
            # evaluate factors when all variables are assigned
            self.display(3,"rc evaluating factors",to_eval)
            val = math.prod(fac.get_value(context) for fac in to_eval)
            if val == 0:
                return 0
            else:
             return val * self.prob_search(context, {fac for fac in factors
                                                     if fac not in to_eval}, split_order)
        elif len(comp := connected_components(context, factors, split_order)) > 1:
            # there are disconnected components
            self.display(3,"splitting into connected components",comp,"in context",context)
            return(math.prod(self.prob_search(context,f,eo) for (f,eo) in comp))
        else:
            assert split_order, "split_order should not be empty to get here"
            total = 0
            var = split_order[0]
            self.display(3, "rc branching on", var)
            for val in var.domain:
                total += self.prob_search(dict_union({var:val},context), factors, split_order[1:])
            self.cache[ce] = total
            self.display(2, "rc branching on", var,"returning", total)
            return total

def connected_components(context, factors, split_order):
    """returns a list of (f,e) where f is a subset of factors and e is a subset of split_order
    such that each element shares the same variables that are disjoint from other elements.
    """
    other_factors = set(factors)  #copies factors
    factors_to_check = {other_factors.pop()}  # factors in connected component still to be checked
    component_factors = set()  # factors in first connected component already checked 
    component_variables = set() # variables in first connected component
    while factors_to_check:
        next_fac = factors_to_check.pop()
        component_factors.add(next_fac)
        new_vars = set(next_fac.variables) - component_variables - context.keys()
        component_variables |= new_vars
        for var in new_vars:
            factors_to_check |= {f for f in other_factors if var in f.variables}
            other_factors -= factors_to_check # set difference
    if  other_factors:
        return ( [(component_factors,[e for e in split_order if e in component_variables])]
                + connected_components(context, other_factors, [e for e in split_order
                                                                     if e not in component_variables]) )
    else:
        return [(component_factors, split_order)]

from probGraphicalModels import bn_4ch, A,B,C,D,f_a,f_b,f_c,f_d
bn_4chv = ProbRC(bn_4ch)
## bn_4chv.query(A,{})
## bn_4chv.query(D,{})
## InferenceMethod.max_display_level = 3   # show more detail in displaying
## InferenceMethod.max_display_level = 1   # show less detail in displaying
## bn_4chv.query(A,{D:True},[C,B])
## bn_4chv.query(B,{A:True,D:False})

from probGraphicalModels import bn_report,Alarm,Fire,Leaving,Report,Smoke,Tamper
bn_reportRC = ProbRC(bn_report)    # answers queries using recursive conditioning
## bn_reportRC.query(Tamper,{})
## InferenceMethod.max_display_level = 0   # show no detail in displaying
## bn_reportRC.query(Leaving,{})
## bn_reportRC.query(Tamper,{}, split_order=[Smoke,Fire,Alarm,Leaving,Report])
## bn_reportRC.query(Tamper,{Report:True})
## bn_reportRC.query(Tamper,{Report:True,Smoke:False})
## Note what happens to the cache when these are called in turn:
## bn_reportRC.query(Tamper,{Report:True}, split_order=[Smoke,Fire,Alarm,Leaving])
## bn_reportRC.query(Smoke,{Report:True}, split_order=[Tamper,Fire,Alarm,Leaving])

from probGraphicalModels import bn_sprinkler, Season, Sprinkler, Rained, Grass_wet, Grass_shiny, Shoes_wet
bn_sprinklerv = ProbRC(bn_sprinkler)
## bn_sprinklerv.query(Shoes_wet,{})
## bn_sprinklerv.query(Shoes_wet,{Rained:True})
## bn_sprinklerv.query(Shoes_wet,{Grass_shiny:True})
## bn_sprinklerv.query(Shoes_wet,{Grass_shiny:False,Rained:True})

from probGraphicalModels import bn_no1, bn_lr1, Cough, Fever, Sneeze, Cold, Flu, Covid
bn_no1v = ProbRC(bn_no1)
bn_lr1v = ProbRC(bn_lr1)
## bn_no1v.query(Flu, {Fever:1, Sneeze:1})
## bn_lr1v.query(Flu, {Fever:1, Sneeze:1})
## bn_lr1v.query(Cough,{})
## bn_lr1v.query(Cold,{Cough:1,Sneeze:0,Fever:1})
## bn_lr1v.query(Flu,{Cough:0,Sneeze:1,Fever:1})
## bn_lr1v.query(Covid,{Cough:1,Sneeze:0,Fever:1})
## bn_lr1v.query(Covid,{Cough:1,Sneeze:0,Fever:1,Flu:0})
## bn_lr1v.query(Covid,{Cough:1,Sneeze:0,Fever:1,Flu:1})

if __name__ == "__main__":
    InferenceMethod.testIM(ProbRC)


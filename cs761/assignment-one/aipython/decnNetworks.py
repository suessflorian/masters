# decnNetworks.py - Representations for Decision Networks
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from probGraphicalModels import GraphicalModel, BeliefNetwork
from probFactors import Factor, CPD, TabFactor, factor_times, Prob
from probVariables import Variable
import matplotlib.pyplot as plt

class Utility(Factor):
     """A factor defining a utility"""
     pass
     
class UtilityTable(TabFactor, Utility):
    """A factor defining a utility using a table"""
    def __init__(self, vars, table, position=None):
        """Creates a factor on vars from the table.
        The table is ordered according to vars.
        """
        TabFactor.__init__(self,vars,table)
        self.position = position

class DecisionVariable(Variable):
    def __init__(self, name, domain, parents, position=None):
        Variable.__init__(self, name, domain, position)
        self.parents = parents
        self.all_vars = set(parents) | {self}

class DecisionNetwork(BeliefNetwork):
    def __init__(self, title, vars, factors):
        """vars is a list of variables
        factors is a list of factors (instances of CPD and Utility)
        """
        GraphicalModel.__init__(self, title, vars, factors) # don't call init for BeliefNetwork
        self.var2parents = ({v : v.parents for v in vars if isinstance(v,DecisionVariable)}
                     | {f.child:f.parents for f in factors if isinstance(f,CPD)})
        self.children = {n:[] for n in self.variables}
        for v in self.var2parents:
            for par in self.var2parents[v]:
                self.children[par].append(v)
        self.utility_factor = [f for f in factors if isinstance(f,Utility)][0]
        self.topological_sort_saved = None

    def split_order(self):
        so = []
        tops = self.topological_sort()
        for v in tops:
            if isinstance(v,DecisionVariable):
               so += [p for p in v.parents if p not in so]
               so.append(v)
        so += [v for v in tops if v not in so]
        return so
        
    def show(self):
        plt.ion()   # interactive
        ax = plt.figure().gca()
        ax.set_axis_off()
        plt.title(self.title)
        for par in self.utility_factor.variables:
            ax.annotate("Utility", par.position, xytext=self.utility_factor.position,
                                    arrowprops={'arrowstyle':'<-'},bbox=dict(boxstyle="sawtooth,pad=1.0",color="red"),
                                    ha='center')
        for var in reversed(self.topological_sort()):
            if isinstance(var,DecisionVariable):
                bbox = dict(boxstyle="square,pad=1.0",color="green")
            else:
               bbox = dict(boxstyle="round4,pad=1.0,rounding_size=0.5")
            if self.var2parents[var]:
                for par in self.var2parents[var]:
                    ax.annotate(var.name, par.position, xytext=var.position,
                                    arrowprops={'arrowstyle':'<-'},bbox=bbox,
                                    ha='center')
            else:
                x,y = var.position
                plt.text(x,y,var.name,bbox=bbox,ha='center')

Weather = Variable("Weather", ["NoRain", "Rain"], position=(0.5,0.8))
Forecast = Variable("Forecast", ["Sunny", "Cloudy", "Rainy"], position=(0,0.4))
# Each variant uses one of the following:
Umbrella = DecisionVariable("Umbrella", ["Take", "Leave"], {Forecast}, position=(0.5,0))

p_weather = Prob(Weather, [], [0.7, 0.3])
p_forecast = Prob(Forecast, [Weather], [[0.7, 0.2, 0.1], [0.15, 0.25, 0.6]])
umb_utility = UtilityTable([Weather, Umbrella], [[20, 100], [70, 0]], position=(1,0.4))

umbrella_dn = DecisionNetwork("Umbrella Decision Network",
                                   {Weather, Forecast, Umbrella},
                                   {p_weather, p_forecast, umb_utility})

Umbrella2p = DecisionVariable("Umbrella", ["Take", "Leave"], {Forecast, Weather}, position=(0.5,0))
umb_utility2p = UtilityTable([Weather, Umbrella2p], [[20, 100], [70, 0]], position=(1,0.4))
umbrella_dn2p = DecisionNetwork("Umbrella Decision Network (extra arc)",
                                   {Weather, Forecast, Umbrella2p},
                                   {p_weather, p_forecast, umb_utility2p})

boolean = [False, True]
Alarm = Variable("Alarm", boolean, position=(0.25,0.633))
Fire = Variable("Fire", boolean, position=(0.5,0.9))
Leaving = Variable("Leaving", boolean, position=(0.25,0.366))
Report = Variable("Report", boolean, position=(0.25,0.1))
Smoke = Variable("Smoke", boolean, position=(0.75,0.633))
Tamper = Variable("Tamper", boolean, position=(0,0.9))

See_Sm = Variable("See_Sm", boolean, position=(0.75,0.366) )
Chk_Sm = DecisionVariable("Chk_Sm", boolean, {Report}, position=(0.5, 0.366))
Call = DecisionVariable("Call", boolean,{See_Sm,Chk_Sm,Report}, position=(0.75,0.1))

f_ta = Prob(Tamper,[],[0.98,0.02])
f_fi = Prob(Fire,[],[0.99,0.01])
f_sm = Prob(Smoke,[Fire],[[0.99,0.01],[0.1,0.9]])
f_al = Prob(Alarm,[Fire,Tamper],[[[0.9999, 0.0001], [0.15, 0.85]], [[0.01, 0.99], [0.5, 0.5]]])
f_lv = Prob(Leaving,[Alarm],[[0.999, 0.001], [0.12, 0.88]])
f_re = Prob(Report,[Leaving],[[0.99, 0.01], [0.25, 0.75]])
f_ss = Prob(See_Sm,[Chk_Sm,Smoke],[[[1,0],[1,0]],[[1,0],[0,1]]])

ut = UtilityTable([Chk_Sm,Fire,Call],[[[0,-200],[-5000,-200]],[[-20,-220],[-5020,-220]]], position=(1,0.633))

fire_dn = DecisionNetwork("Fire Decision Network",
                          {Tamper,Fire,Alarm,Leaving,Smoke,Call,See_Sm,Chk_Sm,Report},
                          {f_ta,f_fi,f_sm,f_al,f_lv,f_re,f_ss,ut})

grades = ['A','B','C','F']
Watched = Variable("Watched", boolean, position=(0,0.9))
Caught1 = Variable("Caught1", boolean, position=(0.2,0.7))
Caught2 = Variable("Caught2", boolean, position=(0.6,0.7))
Punish = Variable("Punish", ["None","Suspension","Recorded"], position=(0.8,0.9))
Grade_1 = Variable("Grade_1", grades, position=(0.2,0.3))
Grade_2 = Variable("Grade_2", grades, position=(0.6,0.3))
Fin_Grd = Variable("Fin_Grd", grades, position=(0.8,0.1))
Cheat_1 = DecisionVariable("Cheat_1", boolean, set(), position=(0,0.5))  #no parents
Cheat_2 = DecisionVariable("Cheat_2", boolean, {Cheat_1,Caught1}, position=(0.4,0.5))

p_wa = Prob(Watched,[],[0.7, 0.3])
p_cc1 = Prob(Caught1,[Watched,Cheat_1],[[[1.0, 0.0], [0.9, 0.1]], [[1.0, 0.0], [0.5, 0.5]]])
p_cc2 = Prob(Caught2,[Watched,Cheat_2],[[[1.0, 0.0], [0.9, 0.1]], [[1.0, 0.0], [0.5, 0.5]]])
p_pun = Prob(Punish,[Caught1,Caught2],[[[1.0, 0.0, 0.0], [0.5, 0.4, 0.1]], [[0.6, 0.2, 0.2], [0.2, 0.5, 0.3]]])
p_gr1 = Prob(Grade_1,[Cheat_1], [{'A':0.2, 'B':0.3, 'C':0.3, 'D': 0.2}, {'A':0.5, 'B':0.3, 'C':0.2, 'D':0.0}])
p_gr2 = Prob(Grade_2,[Cheat_2], [{'A':0.2, 'B':0.3, 'C':0.3, 'D': 0.2}, {'A':0.5, 'B':0.3, 'C':0.2, 'D':0.0}])
p_fg = Prob(Fin_Grd,[Grade_1,Grade_2],
        {'A':{'A':{'A':1.0, 'B':0.0, 'C': 0.0, 'D':0.0},
              'B': {'A':0.5, 'B':0.5, 'C': 0.0, 'D':0.0},
              'C':{'A':0.25, 'B':0.5, 'C': 0.25, 'D':0.0},
              'D':{'A':0.25, 'B':0.25, 'C': 0.25, 'D':0.25}},
         'B':{'A':{'A':0.5, 'B':0.5, 'C': 0.0, 'D':0.0},
              'B': {'A':0.0, 'B':1, 'C': 0.0, 'D':0.0},
              'C':{'A':0.0, 'B':0.5, 'C': 0.5, 'D':0.0},
              'D':{'A':0.0, 'B':0.25, 'C': 0.5, 'D':0.25}},
         'C':{'A':{'A':0.25, 'B':0.5, 'C': 0.25, 'D':0.0},
              'B': {'A':0.0, 'B':0.5, 'C': 0.5, 'D':0.0},
              'C':{'A':0.0, 'B':0.0, 'C': 1, 'D':0.0},
              'D':{'A':0.0, 'B':0.0, 'C': 0.5, 'D':0.5}},
         'D':{'A':{'A':0.25, 'B':0.25, 'C': 0.25, 'D':0.25},
              'B': {'A':0.0, 'B':0.25, 'C': 0.5, 'D':0.25},
              'C':{'A':0.0, 'B':0.0, 'C': 0.5, 'D':0.5},
              'D':{'A':0.0, 'B':0.0, 'C': 0, 'D':1.0}}})

utc = UtilityTable([Punish,Fin_Grd],{'None':{'A':100, 'B':90, 'C': 70, 'D':50},
                                     'Suspension':{'A':40, 'B':20, 'C': 10, 'D':0},
                                     'Recorded':{'A':70, 'B':60, 'C': 40, 'D':20}}, position=(1,0.5))

cheating_dn = DecisionNetwork("Cheating Decision Network",
                            {Punish,Caught2,Watched,Fin_Grd,Grade_2,Grade_1,Cheat_2,Caught1,Cheat_1},
                            {p_wa, p_cc1, p_cc2, p_pun, p_gr1, p_gr2,p_fg,utc})

S0 = Variable('S0', boolean,  position=(0,0.5))
D0 = DecisionVariable('D0', boolean, {S0},  position=(1/7,0.1))
S1 = Variable('S1', boolean,  position=(2/7,0.5))
D1 = DecisionVariable('D1', boolean, {S1},  position=(3/7,0.1))
S2 = Variable('S2', boolean,   position=(4/7,0.5))
D2 = DecisionVariable('D2', boolean, {S2}, position=(5/7,0.1))
S3 = Variable('S3', boolean,  position=(6/7,0.5))

p_s0 = Prob(S0, [], [0.5,0.5])
tr = [[[0.1, 0.9], [0.9, 0.1]], [[0.2, 0.8], [0.8, 0.2]]] # 0 is flip, 1 is keep value
p_s1 = Prob(S1, [D0,S0], tr)
p_s2 = Prob(S2, [D1,S1], tr)
p_s3 = Prob(S3, [D2,S2], tr)

ch3U = UtilityTable([S3],[0,1], position=(7/7,0.9))

ch3 = DecisionNetwork("3-chain", {S0,D0,S1,D1,S2,D2,S3},{p_s0,p_s1,p_s2,p_s3,ch3U})
#rc3 = RC_DN(ch3)
#rc3.optimize()
#rc3.opt_policy

import math
from probGraphicalModels import GraphicalModel, InferenceMethod
from probFactors import Factor
from utilities import dict_union
from probRC import connected_components

class RC_DN(InferenceMethod):
    """The class that queries graphical models using recursive conditioning

    gm is graphical model to query
    """
 
    def __init__(self,gm=None):
        self.gm = gm
        self.cache = {(frozenset(), frozenset()):1}
        ## self.max_display_level = 3

    def optimize(self, split_order=None):
        """computes expected utility, and creates optimal decision functions, where
        elim_order is a list of the non-observed non-query variables in gm
        """
        if split_order == None:
            split_order = self.gm.split_order()
        self.opt_policy = {}
        return self.rc({}, self.gm.factors, split_order)

    def rc0(self, context, factors, split_order):
        """simplest search algorithm"""
        self.display(2,"calling rc0,",(context,factors),"with SO",split_order)
        if not factors:
            return 1
        elif to_eval := {fac for fac in factors if fac.can_evaluate(context)}:
            self.display(3,"rc0 evaluating factors",to_eval)
            val = math.prod(fac.get_value(context) for fac in to_eval)
            return val * self.rc0(context, factors-to_eval, split_order)
        else:
            var = split_order[0]
            self.display(3, "rc0 branching on", var)
            if isinstance(var,DecisionVariable):
                assert set(context) <= set(var.parents), f"cannot optimize {var} in context {context}"
                maxres = -math.inf
                for val in var.domain:
                    self.display(3,"In rc0, branching on",var,"=",val)
                    newres = self.rc0(dict_union({var:val},context), factors, split_order[1:])
                    if newres > maxres:
                        maxres = newres
                        theval = val
                self.opt_policy[frozenset(context.items())] = (var,theval)
                return maxres
            else:
                total = 0
                for val in var.domain:
                    total += self.rc0(dict_union({var:val},context), factors, split_order[1:])
                self.display(3, "rc0 branching on", var,"returning", total)
                return total

    def rc(self, context, factors, split_order):
        """ returns the number \sum_{split_order} \prod_{factors} given assignments in context
        context is a variable:value dictionary
        factors is a set of factors
        split_order is a list of variables in factors that are not in context
        """
        self.display(3,"calling rc,",(context,factors))
        ce = (frozenset(context.items()),  frozenset(factors))  # key for the cache entry
        if ce in self.cache:
            self.display(2,"rc cache lookup",(context,factors))
            return self.cache[ce]
#        if not factors:  # no factors; needed if you don't have forgetting and caching
#            return 1
        elif vars_not_in_factors := {var for var in context
                                         if not any(var in fac.variables for fac in factors)}:
             # forget variables not in any factor
            self.display(3,"rc forgetting variables", vars_not_in_factors)
            return self.rc({key:val for (key,val) in context.items()
                                if key not in vars_not_in_factors},
                            factors, split_order)
        elif to_eval := {fac for fac in factors if fac.can_evaluate(context)}:
            # evaluate factors when all variables are assigned
            self.display(3,"rc evaluating factors",to_eval)
            val = math.prod(fac.get_value(context) for fac in to_eval)
            if val == 0:
                return 0
            else:
             return val * self.rc(context, {fac for fac in factors if fac not in to_eval}, split_order)
        elif len(comp := connected_components(context, factors, split_order)) > 1:
            # there are disconnected components
            self.display(2,"splitting into connected components",comp)
            return(math.prod(self.rc(context,f,eo) for (f,eo) in comp))
        else:
            assert split_order, f"split_order empty rc({context},{factors})"
            var = split_order[0]
            self.display(3, "rc branching on", var)
            if isinstance(var,DecisionVariable):
                assert set(context) <= set(var.parents), f"cannot optimize {var} in context {context}"
                maxres = -math.inf
                for val in var.domain:
                    self.display(3,"In rc, branching on",var,"=",val)
                    newres = self.rc(dict_union({var:val},context), factors, split_order[1:])
                    if newres > maxres:
                        maxres = newres
                        theval = val
                self.opt_policy[frozenset(context.items())] = (var,theval)
                self.cache[ce] = maxres
                return maxres
            else:
                total = 0
                for val in var.domain:
                    total += self.rc(dict_union({var:val},context), factors, split_order[1:])
                self.display(3, "rc branching on", var,"returning", total)
                self.cache[ce] = total
                return total

# Umbrella decision network
#urc = RC_DN(umberella_dn)
#urc.optimize()
#urc.opt_policy

#rc_fire = RC_DN(fire_dn)
#rc_fire.optimize()
#rc_fire.opt_policy

#rc_cheat = RC_DN(cheating_dn)
#rc_cheat.optimize()
#rc_cheat.opt_policy

#rc_ch3 = RC_DN(ch3)
#rc_ch3.optimize()
#rc_ch3.opt_policy

from probVE import VE

class VE_DN(VE):
    """Variable Elimination for Decision Networks"""
    def __init__(self,dn=None):
        """dn is a decision network"""
        VE.__init__(self,dn)
        self.dn = dn
        
    def optimize(self,elim_order=None,obs={}):
        if elim_order == None:
                elim_order = reversed(self.gm.split_order())
        policy = []
        proj_factors = [self.project_observations(fact,obs) 
                           for fact in self.dn.factors]
        for v in elim_order:
            if isinstance(v,DecisionVariable):
                to_max = [fac for fac in proj_factors
                          if v in fac.variables and set(fac.variables) <= v.all_vars]
                assert len(to_max)==1, "illegal variable order "+str(elim_order)+" at "+str(v)
                newFac = FactorMax(v, to_max[0])
                policy.append(newFac.decision_fun)
                proj_factors = [fac for fac in proj_factors if fac is not to_max[0]]+[newFac]
                self.display(2,"maximizing",v,"resulting factor",newFac.brief() )
                self.display(3,newFac)
            else:
                proj_factors = self.eliminate_var(proj_factors, v)
        assert len(proj_factors)==1,"Should there be only one element of proj_factors?"
        value = proj_factors[0].get_value({})
        return value,policy

class FactorMax(Factor):
    """A factor obtained by maximizing a variable in a factor.
    Also builds a decision_function. This is based on FactorSum.
    """

    def __init__(self, dvar, factor):
        """dvar is a decision variable. 
        factor is a factor that contains dvar and only parents of dvar
        """
        self.dvar = dvar
        self.factor = factor
        vars = [v for v in factor.variables if v is not dvar]
        Factor.__init__(self,vars)
        self.values = [None]*self.size
        self.decision_fun = FactorDF(dvar,vars,[None]*self.size)

    def get_value(self,assignment):
        """lazy implementation: if saved, return saved value, else compute it"""
        index = self.assignment_to_index(assignment)
        if self.values[index]:
            return self.values[index]
        else:
            max_val = float("-inf")  # -infinity
            new_asst = assignment.copy()
            for elt in self.dvar.domain:
                new_asst[self.dvar] = elt
                fac_val = self.factor.get_value(new_asst)
                if fac_val>max_val:
                    max_val = fac_val
                    best_elt = elt
            self.values[index] = max_val
            self.decision_fun.values[index] = best_elt
            return max_val
           
class FactorDF(TabFactor):
    """A decision function"""
    def __init__(self,dvar, vars, values):
        TabStored.__init__(self,vars,values)
        self.dvar = dvar
        self.name = str(dvar)  # Used in printing

# Example queries:
# v,p = VE_DN(fire_dn).optimize(); print(v)
# for df in p: print(df,"\n")

# VE_DN.max_display_level = 3  # if you want to show lots of detail
# v,p = VE_DN(cheating_dn).optimize(); print(v)
# for df in p: print(df,"\n") # print decision functions


# probDo.py - Probabilistic inference with the do operator
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from probGraphicalModels import InferenceMethod, BeliefNetwork
from probFactors import CPD, ConstantCPD

def queryDo(self, qvar, obs={}, do={}):
    assert isinstance(self.gm, BeliefNetwork), "Do only applies to belief networks"
    if do=={}:
        return self.query(qvar, obs)
    else:
        newfacs = ({f for (ch,f) in self.gm.var2cpt.items() if ch not in do} |
                       {ConstantCPD(v,c) for (v,c) in do.items()})
        self.modBN = BeliefNetwork(self.gm.title+"(mod)", self.gm.variables, newfacs)
        oldBN, self.gm = self.gm, self.modBN
        result = self.query(qvar, obs)
        self.gm = oldBN  # restore original
        return result
    
InferenceMethod.queryDo = queryDo
    
from probRC import ProbRC

from probGraphicalModels import bn_sprinkler, Season, Sprinkler, Rained, Grass_wet, Grass_shiny, Shoes_wet, bn_sprinkler_soff
bn_sprinklerv = ProbRC(bn_sprinkler)
## bn_sprinklerv.queryDo(Shoes_wet)
## bn_sprinklerv.queryDo(Shoes_wet,obs={Sprinkler:"off"})
## bn_sprinklerv.queryDo(Shoes_wet,do={Sprinkler:"off"})
## ProbRC(bn_sprinkler_soff).query(Shoes_wet) # should be same as previous case
## bn_sprinklerv.queryDo(Season, obs={Sprinkler:"off"})
## bn_sprinklerv.queryDo(Season, do={Sprinkler:"off"})

from probVariables import Variable
from probFactors import Prob
from probGraphicalModels import boolean

Drug_Prone = Variable("Drug_Prone", boolean, position=(0.1,0.5))
Takes_Marijuana = Variable("Takes_Marijuana", boolean, position=(0.1,0.5))
Side_Effects = Variable("Side_Effects", boolean, position=(0.1,0.5))
Takes_Hard_Drugs = Variable("Takes_Hard_Drugs", boolean, position=(0.9,0.5))

p_dp = Prob(Drug_Prone, [], [0.8, 0.2])
p_tm = Prob(Takes_Marijuana, [Drug_Prone], [[0.98, 0.02], [0.2, 0.8]])
p_be = Prob(Side_Effects, [Takes_Marijuana], [[1, 0], [0.4, 0.6]])
p_thd = Prob(Takes_Hard_Drugs, [Side_Effects, Drug_Prone],
                 # Drug_Prone=False    Drug_Prone=True
                 [[[0.999, 0.001],     [0.6, 0.4]], # Side_Effects=False
                  [[0.99999, 0.00001], [0.995, 0.005]]])  # Side_Effects=True

drugs = BeliefNetwork("Gateway Drugs",
                    [Drug_Prone,Takes_Marijuana,Side_Effects,Takes_Hard_Drugs],
                    [p_dp, p_tm, p_be, p_thd])
drugsq = ProbRC(drugs)
# drugsq.queryDo(Takes_Hard_Drugs)
# drugsq.queryDo(Takes_Hard_Drugs, obs = {Takes_Marijuana: True})
# drugsq.queryDo(Takes_Hard_Drugs, obs = {Takes_Marijuana: False})
# drugsq.queryDo(Takes_Hard_Drugs, do = {Takes_Marijuana: True})
# drugsq.queryDo(Takes_Hard_Drugs, do = {Takes_Marijuana: False})


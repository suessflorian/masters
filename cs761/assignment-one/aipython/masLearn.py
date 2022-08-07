# masLearn.py - Simulations of agents learning
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from display import Displayable
import utilities  # argmaxall for (element,value) pairs
import matplotlib.pyplot as plt
import random

class GameAgent(Displayable):
    next_id=0
    def __init__(self, actions):
        """
        Actions is the set of actions the agent can do. It needs to be told that!
        """
        self.actions = actions
        self.id = GameAgent.next_id
        GameAgent.next_id += 1
        self.display(2,f"Agent {self.id} has actions {actions}")
        self.total_score = 0
        self.dist = {act:1 for act in actions} # unnormalized distibution

    def init_action(self):
        """ The initial action.
        Act randomly initially
        Could be overridden (but I'm not sure why you would).
        """
        self.act = random.choice(self.actions)
        self.dist[self.act] += 1
        return self.act

    def select_action(self, reward):
        """ 
        Select the action given the reward.
        This implements "Act randomly" and should  be overridden!
        """
        self.total_score += reward
        self.act = random.choice(self.actions)
        self.dist[self.act] += 1
        return self.act

class SimpleQAgent(GameAgent):
    """This agent just counts the number of times (it thinks) it has won and does the 
    actions it thinks is most likely to win.
    """
    def __init__(self, actions, alpha=0.1, q_init=1, explore=0.01):
        """
        Actions is the set of actions the agent can do.
        alpha is the Q step size
        q_init is the initial q-values
        explore is the probability of an exporatory (random) action
        """
        GameAgent.__init__(self, actions)
        self.Q = {a:q_init for a in self.actions}
        self.dist = {act:1 for act in actions} # unnormalized distibution
        self.num_steps = 0
        self.alpha = alpha
        self.explore = explore
        
    def select_action(self, reward):
        self.total_score += reward
        self.num_steps += 1
        self.display(2,f"The reward for agent {self.id} was {reward}")
        self.Q[self.act] += self.alpha*(reward-self.Q[self.act])
        if random.random() < self.explore:
            self.act = random.choice(self.actions) # act randomly
        else:
            self.act = utilities.argmaxd(self.Q)
        self.dist[self.act] += 1
        self.display(2,f"Agent {self.id} did {self.act}")
        return self.act

class StochasticQAgent(GameAgent):
    """This agent  maintains the Q-function for each state. 
    (Or just the average reward as the future state is all the same).
    Chooses the best action using 
    """
    def __init__(self, actions, alpha=0.1, q_init=10, p_init=5):
        """
        Actions is the set of actions the agent can do. 
        alpha is the Q step size
        q_init is the initial q-values
        p_init is the initial counts for q
         """
        GameAgent.__init__(self, actions)
        self.Q = {a:q_init for a in self.actions}
        self.dist = {a:p_init for a in self.actions} # start with random dist
        self.alpha = alpha
        self.num_steps = 0
           
    def select_action(self, reward):
        self.total_score += reward
        self.display(2,f"The reward for agent {self.id} was {reward}")
        self.Q[self.act] += self.alpha*(reward-self.Q[self.act])
        a_best = utilities.argmaxall(self.Q.items())
        for a in a_best:
                self.dist[a] += 1
        self.display(2,f"Distribution for agent {self.id} is {self.dist}")
        self.act = select_from_dist(self.dist)
        self.display(2,f"Agent {self.id} did {self.act}")
        return self.act

def normalize(dist):
    """unnorm dict is a {value:number} dictionary, where the numbers are all non-negative
    returns dict where the numbers sum to one
    """
    tot = sum(dist.values())
    return {var:val/tot for (var,val) in dist.items()}

def select_from_dist(dist):
    rand = random.random()
    for (act,prob) in normalize(dist).items():
        rand -= prob
        if rand < 0:
            return act
        
class SimulateGame(Displayable):
    def __init__(self, game, agents):
        self.game = game
        self.agents = agents  # list of agents
        self.action_history = []
        self.reward_history = []
        self.dist_history = []
        self.actions = tuple(ag.init_action() for ag in self.agents)
        self.num_steps = 0

    def go(self, steps):
        for i in range(steps):
            self.num_steps += 1
            self.rewards = self.game.play(self.actions)
            self.reward_history.append(self.rewards)
            self.actions = tuple(self.agents[i].select_action(self.rewards[i])
                                     for i in range(self.game.num_agents))
            self.action_history.append(self.actions)
            self.dist_history.append([normalize(ag.dist) for ag in self.agents])
        print("Scores:", ' '.join(f"Agent {ag.id} average reward={ag.total_score/self.num_steps}" for ag in self.agents))
        #return self.reward_history, self.action_history

    def action_dist(self,which_actions=[1,1]):
        """ which actions is  [a0,a1]
        returns the empirical disctribition of actions for agents,
           where ai specifies the index of the actions for agent i
        """
        return [sum(1 for a in sim.action_history
                        if a[i]==gm.actions[i][which_actions[i]])/len(sim.action_history)
                    for i in range(2)]


    def plot_dynamics(self, x_action=0, y_action=0):
        #plt.ion()  # make it interactive
        agents = self.agents
        x_act = self.game.actions[0][x_action]
        y_act = self.game.actions[1][y_action]
        plt.xlabel(f"Probability {self.game.players[0]} {self.agents[0].actions[x_action]}")
        plt.ylabel(f"Probability {self.game.players[1]} {self.agents[1].actions[y_action]}")
        plt.plot([self.dist_history[t][0][x_act] for t in range(len(self.dist_history))],
                 [self.dist_history[t][1][y_act] for t in range(len(self.dist_history))],
                 color='k')
        #plt.legend()
        plt.savefig('soccerplot.pdf')
        plt.show()

class ShoppingGame(Displayable):
    def __init__(self):
        self.num_agents = 2
        self.actions = [['shopping', 'football']]*2
        self.players = ['football preferer goes to', 'shopping preferer goes to']

    def play(self, actions):
        return {('football', 'football'): (2,1),
                ('football', 'shopping'): (0,0),
                ('shopping', 'football'): (0,0),
                ('shopping', 'shopping'): (1,2)}[actions]


class SoccerGame(Displayable):
    def __init__(self):
        self.num_agents = 2
        self.actions = [['right', 'left']]*2
        self.players = ['goalkeeper jumps', 'kicker kicks']

    def play(self, actions):
        return {('left', 'left'): (0.6, 0.4),
                ('left', 'right'): (0.3, 0.7),
                ('right', 'left'): (0.2, 0.8),
                ('right', 'right'): (0.9,0.1)
               }[actions]
               
class GameShow(Displayable):
    def __init__(self):
        self.num_agents = 2
        self.actions = [['takes', 'gives']]*2
        self.players = ['Agent 1', 'Agent 2']

    def play(self, actions):
        return {('takes', 'takes'): (1, 1),
                ('takes', 'gives'): (11, 0),
                ('gives', 'takes'): (0, 11),
                ('gives', 'gives'): (10,10)
               }[actions]
               

class UniqueNEGameExample(Displayable):
    def __init__(self):
        self.num_agents = 2
        self.actions = [['a1', 'b1', 'c1'],['d2', 'e2', 'f2']]
        self.players = ['agent 1 does', 'agent 2 does']

    def play(self, actions):
        return {('a1', 'd2'): (3, 5),
                ('a1', 'e2'): (5, 1),
                ('a1', 'f2'): (1, 2),
                ('b1', 'd2'): (1, 1),
                ('b1', 'e2'): (2, 9),
                ('b1', 'f2'): (6, 4),
                ('c1', 'd2'): (2, 6),
                ('c1', 'e2'): (4, 7),
                ('c1', 'f2'): (0, 8)
               }[actions]

# Choose one:
# gm = ShoppingGame()
# gm = SoccerGame()
# gm = GameShow()
# gm = UniqueNEGameExample()

# Choose one of the combinations of learners:
# sim=SimulateGame(gm,[StochasticQAgent(gm.actions[0]), StochasticQAgent(gm.actions[1])]); sim.go(10000)
# sim= SimulateGame(gm,[SimpleQAgent(gm.actions[0]), SimpleQAgent(gm.actions[1])]); sim.go(10000)
# sim=SimulateGame(gm,[SimpleQAgent(gm.actions[0]),StochasticQAgent(gm.actions[1])]); sim.go(10000)
# sim=SimulateGame(gm,[StochasticQAgent(gm.actions[0]),SimpleQAgent(gm.actions[1])]); sim.go(10000)


# sim.plot_dynamics()

# empirical proportion that agents did their action at index 1:
# sim.action_dist([1,1])

# (unnormalized) emprirical distribution for agent 0
# sim.agents[0].dist
# solution to Exercise 14.8 (i) of Poole & Mackworth 2023
class StochasticQAgent_i(GameAgent):
    """This agent  maintains the Q-function for each state. 
    (Or just the average reward as the future state is all the same).
    Chooses the best action using 
    """
    def __init__(self, actions, alpha=0.1, q_init=10, p_init=50, beta=0.001):
        """
        Actions is the set of actions the agent can do. 
        alpha is the Q step size
        q_init is the initial q-values
        p_init is the initial counts for q
        beta is the discount for older probabilities
         """
        GameAgent.__init__(self, actions)
        self.Q = {a:q_init for a in self.actions}
        self.dist = {a:p_init for a in self.actions} # start with random dist
        self.alpha = alpha
        self.beta = beta
        self.num_steps = 0
           
    def select_action(self, reward):
        self.total_score += reward
        self.display(2,f"The reward for agent {self.id} was {reward}")
        self.Q[self.act] += self.alpha*(reward-self.Q[self.act])
        a_best = utilities.argmaxall(self.Q.items())
        for a in self.Q.keys():
             self.dist[a] *= (1-self.beta)
        for a in a_best:
                self.dist[a] += 1
        self.display(2,f"Distribution for agent {self.id} is {self.dist}")
        self.act = select_from_dist(self.dist)
        self.display(2,f"Agent {self.id} did {self.act}")
        return self.act


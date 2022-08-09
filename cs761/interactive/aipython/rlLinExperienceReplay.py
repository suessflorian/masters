# rlLinExperienceReplay.py - Linear Reinforcement Learner with Experience Replay
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from rlFeatures import SARSA_LFA_learner, dot_product
from utilities import flip
import random

class SARSA_LFA_AR_learner(SARSA_LFA_learner):

    def __init__(self, env, get_features, discount, explore=0.2, step_size=0.01,
                 winit=0, label="SARSA_LFA-AR", max_buffer_size=500,
                 num_updates_per_action=5, burn_in=100 ):
        SARSA_LFA_learner.__init__(self, env, get_features, discount, explore, step_size,
                                       winit, label)
        self. max_buffer_size = max_buffer_size
        self.action_buffer = [0]*max_buffer_size
        self.number_added = 0
        self.num_updates_per_action = num_updates_per_action
        self.burn_in = burn_in

    def add_to_buffer(self,experience):
        if self.number_added < self.max_buffer_size:
            self.action_buffer[self.number_added] = experience
        else:
            if flip(self.max_buffer_size/self.number_added):
                position = random.randrange(self.max_buffer_size)
                self.action_buffer[position] = experience
        self.number_added += 1
    
    def do(self,num_steps=100):
        """do num_steps of interaction with the environment"""
        self.display(2,"s\ta\tr\ts'\tQ\tdelta")
        for i in range(num_steps):
            next_state,reward = self.env.do(self.action)
            self.add_to_buffer((self.state,self.action,reward,next_state)) #remember experience
            self.acc_rewards += reward
            next_action = self.select_action(next_state)
            feature_values = self.get_features(self.state,self.action)
            oldQ = dot_product(self.weights, feature_values)
            nextQ = dot_product(self.weights, self.get_features(next_state,next_action))
            delta = reward + self.discount * nextQ - oldQ
            for i in range(len(self.weights)):
                self.weights[i] += self.step_size * delta * feature_values[i]
            self.display(2,self.state, self.action, reward, next_state,
                         dot_product(self.weights, feature_values), delta, sep='\t')
            self.state = next_state
            self.action = next_action
            if self.number_added > self.burn_in:
              for i in range(self.num_updates_per_action):
                (s,a,r,ns) = self.action_buffer[random.randrange(min(self.number_added,
                                                                         self.max_buffer_size))]
                na = self.select_action(ns)
                feature_values = self.get_features(s,a)
                oldQ = dot_product(self.weights, feature_values)
                nextQ = dot_product(self.weights, self.get_features(ns,na))
                delta = reward + self.discount * nextQ - oldQ
                for i in range(len(self.weights)):
                    self.weights[i] += self.step_size * delta * feature_values[i]

from rlQTest import senv    # monster game environment
from rlMonsterGameFeatures import get_features, simp_features
from rlPlot import plot_rl

fa1 = SARSA_LFA_AR_learner(senv, get_features, 0.9, step_size=0.01)
#fa1.max_display_level = 2
#fa1.do(20)
#plot_rl(fa1,steps_explore=10000,steps_exploit=10000,label="SARSA_LFA_AR(0.01)")
fas1 = SARSA_LFA_AR_learner(senv, simp_features, 0.9, step_size=0.01)
#plot_rl(fas1,steps_explore=10000,steps_exploit=10000,label="SARSA_LFA_AR(simp)")


# rlQExperienceReplay.py - Linear Reinforcement Learner with Experience Replay
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from rlQLearner import Q_learner
from utilities import flip
import random

class BoundedBuffer(object):
    def __init__(self, buffer_size=1000):
        self.buffer_size = buffer_size
        self.buffer = [0]*buffer_size
        self.number_added = 0

    def add(self,experience):
        if self.number_added < self.buffer_size:
            self.buffer[self.number_added] = experience
        else:
            if flip(self.buffer_size/self.number_added):
                position = random.randrange(self.buffer_size)
                self.buffer[position] = experience
        self.number_added += 1

    def get(self):
        return self.buffer[random.randrange(min(self.number_added, self.buffer_size))]

class Q_AR_learner(Q_learner):
    def __init__(self, env, discount, explore=0.1, fixed_alpha=True, alpha=0.2,
                 alpha_fun=lambda k:1/k, qinit=0, label="Q_AR_learner", max_buffer_size=5000,
                 num_updates_per_action=5, burn_in=1000 ):
        Q_learner.__init__(self, env, discount, explore, fixed_alpha, alpha,
                 alpha_fun, qinit, label)
        self.experience_buffer = BoundedBuffer(max_buffer_size)
        self.num_updates_per_action = num_updates_per_action
        self.burn_in = burn_in


    def do(self,num_steps=100):
        """do num_steps of interaction with the environment"""
        self.display(2,"s\ta\tr\ts'\tQ")
        alpha = self.alpha
        for i in range(num_steps):
            action = self.select_action(self.state)
            next_state,reward = self.env.do(action)
            self.experience_buffer.add((self.state,action,reward,next_state)) #remember experience
            if not self.fixed_alpha:
                k = self.visits[(self.state, action)] = self.visits.get((self.state, action),0)+1
                alpha = self.alpha_fun(k)
            self.q[(self.state, action)] = (
                (1-alpha) * self.q.get((self.state, action),self.qinit)
                + alpha * (reward + self.discount
                                    * max(self.q.get((next_state, next_act),self.qinit)
                                          for next_act in self.actions)))
            self.display(2,self.state, action, reward, next_state, 
                         self.q[(self.state, action)], sep='\t')
            self.state = next_state
            self.acc_rewards += reward
            # do some updates from experince buffer
            if self.experience_buffer.number_added > self.burn_in:
              for i in range(self.num_updates_per_action):
                (s,a,r,ns) = self.experience_buffer.get()
                if not self.fixed_alpha:
                    k = self.visits[(s,a)]
                    alpha = self.alpha_fun(k)
                self.q[(s,a)] = (
                    (1-alpha) * self.q[(s,a)]
                    + alpha * (reward + self.discount
                                    * max(self.q.get((ns,na),self.qinit)
                                            for na in self.actions)))

from rlMonsterEnv import Monster_game_env
from rlQTest import sag1, sag2, sag3
from rlPlot import plot_rl

senv = Monster_game_env()
sag1ar = Q_AR_learner(senv,0.9,explore=0.2,fixed_alpha=True,alpha=0.1)
# plot_rl(sag1ar,steps_explore=100000,steps_exploit=100000,label="AR alpha="+str(sag1ar.alpha))
sag2ar = Q_AR_learner(senv,0.9,explore=0.2,fixed_alpha=False)
# plot_rl(sag2ar,steps_explore=100000,steps_exploit=100000,label="AR alpha=1/k")
sag3ar = Q_AR_learner(senv,0.9,explore=0.2,fixed_alpha=False,alpha_fun=lambda k:10/(9+k))
# plot_rl(sag3ar,steps_explore=100000,steps_exploit=100000,label="AR alpha=10/(9+k)")


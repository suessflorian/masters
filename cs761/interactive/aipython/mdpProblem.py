# mdpProblem.py - Representations for Markov Decision Processes
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from utilities import argmaxd
import random
import matplotlib.pyplot as plt
from matplotlib.widgets import Button, CheckButtons

class MDP(object):
    """A Markov Decision Process. Must define:
    self.states the set (or list) of states
    self.actions the set (or list) of actions
    self.discount a real-valued discount
    """

    def __init__(self, states, actions, discount, init=0):
        self.states = states
        self.actions = actions
        self.discount = discount
        self.initv = self.v = {s:init for s in self.states}
        self.initq = self.q = {s: {a: init for a in self.actions} for s in self.states}

    def P(self,s,a):
        """Transition probability function
        returns a dictionary of {s1:p1} such that P(s1 | s,a)=p1. Other probabilities are zero.
        """
        raise NotImplementedError("P")   # abstract method

    def R(self,s,a):
        """Reward function R(s,a)
        returns the expected reward for doing a in state s.
        """
        raise NotImplementedError("R")   # abstract method

    def vi(self,  n):
        """carries out n iterations of value iteration, updating value function self.v
        Returns a Q-function, value function, policy
        """
        print("calling vi")
        assert n>0,"You must carry out at least one iteration of vi. n="+str(n)
        #v = v0 if v0 is not None else {s:0 for s in self.states}
        for i in range(n):
            self.q = {s: {a: self.R(s,a)+self.discount*sum(p1*self.v[s1]
                                                          for (s1,p1) in self.P(s,a).items())
                      for a in self.actions}
                 for s in self.states}
            self.v = {s: max(self.q[s][a] for a in self.actions)
                  for s in self.states}
        self.pi = {s: argmaxd(self.q[s])
                  for s in self.states}
        return self.q, self.v, self.pi
        
class GridMDP(MDP):
    def __init__(self, states, actions, discount):
        MDP.__init__(self, states, actions, discount)

    def show(self):
        #plt.ion()   # interactive
        fig,(self.ax) = plt.subplots()
        plt.subplots_adjust(bottom=0.2)
        stepB = Button(plt.axes([0.8,0.05,0.1,0.075]), "step")
        stepB.on_clicked(self.on_step)
        resetB = Button(plt.axes([0.6,0.05,0.1,0.075]), "reset")
        resetB.on_clicked(self.on_reset)
        self.qcheck = CheckButtons(plt.axes([0.2,0.05,0.35,0.075]),
                                       ["show q-values","show policy"])
        self.qcheck.on_clicked(self.show_vals)
        self.show_vals(None)
        plt.show()

    def show_vals(self,event):
        self.ax.cla()
        array = [[self.v[(x,y)] for x in range(self.x_dim)]
                                             for y in range(self.y_dim)]
        self.ax.pcolormesh([x-0.5  for x in range(self.x_dim+1)],
                               [x-0.5  for x in range(self.y_dim+1)],
                               array, edgecolors='black',cmap='summer')
            # for cmap see https://matplotlib.org/stable/tutorials/colors/colormaps.html
        if self.qcheck.get_status()[1]:  # "show policy"
                for (x,y) in self.q:
                   maxv = max(self.q[(x,y)][a] for a in self.actions)
                   for a in self.actions:
                       if self.q[(x,y)][a] == maxv:
                          # draw arrow in appropriate direction
                          self.ax.arrow(x,y,self.xoff[a]*2,self.yoff[a]*2,
                                    color='red',width=0.05, head_width=0.2, length_includes_head=True)
        if self.qcheck.get_status()[0]:  # "show q-values"
           self.show_q(event)
        else:
           self.show_v(event)
        self.ax.set_xticks(range(self.x_dim))
        self.ax.set_xticklabels(range(self.x_dim))
        self.ax.set_yticks(range(self.y_dim))
        self.ax.set_yticklabels(range(self.y_dim))
        plt.draw()
        
    def on_step(self,event):
        self.vi(1)
        self.show_vals(event)

    def show_v(self,event):
        """show values"""
        for (x,y) in self.v:
            self.ax.text(x,y,"{val:.2f}".format(val=self.v[(x,y)]),ha='center')

    def show_q(self,event):
        """show q-values"""
        for (x,y) in self.q:
            for a in self.actions:
                self.ax.text(x+self.xoff[a],y+self.yoff[a],
                                 "{val:.2f}".format(val=self.q[(x,y)][a]),ha='center')

    def on_reset(self,event):
       self.v = self.initv
       self.q = self.initq
       self.show_vals(event)

    def avi(self,n):
          states = list(self.states)
          actions = list(self.actions)
          for i in range(n):
              s = random.choice(states)
              a = random.choice(actions)
              self.q[s][a] = (self.R(s,a) + self.discount *
                                  sum(p1 * max(self.q[s1][a1]
                                                    for a1 in self.actions)
                                        for (s1,p1) in self.P(s,a).items()))
          return Q
    

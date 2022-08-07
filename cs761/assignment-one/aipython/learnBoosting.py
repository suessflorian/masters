# learnBoosting.py - Functional Gradient Boosting
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnProblem import Data_set, Learner, Evaluate
from learnNoInputs import Predict
from learnLinear import sigmoid
import statistics
import random

class Boosted_dataset(Data_set):
    def __init__(self, base_dataset, offset_fun, subsample=1.0):
        """new dataset which is like base_dataset,
           but offset_fun(e) is subtracted from the target of each example e
        """
        self.base_dataset = base_dataset
        self.offset_fun = offset_fun
        self.train = random.sample(base_dataset.train,int(subsample*len(base_dataset.train)))
        self.test = base_dataset.test
        #Data_set.__init__(self, base_dataset.train, base_dataset.test, 
        #                  base_dataset.prob_test, base_dataset.target_index)

        #def create_features(self):
        """creates new features - called at end of Data_set.init()
        defines a new target
        """
        self.input_features = self.base_dataset.input_features
        def newout(e):
            return self.base_dataset.target(e) - self.offset_fun(e)
        newout.frange = self.base_dataset.target.frange
        newout.ftype = self.infer_type(newout.frange)
        self.target = newout

    def conditions(self, *args, colsample_bytree=0.5, **nargs):
        conds = self.base_dataset.conditions(*args, **nargs)
        return random.sample(conds, int(colsample_bytree*len(conds)))

class Boosting_learner(Learner):
    def __init__(self, dataset, base_learner_class, subsample=0.8):
        self.dataset = dataset
        self.base_learner_class = base_learner_class
        self.subsample = subsample
        mean = sum(self.dataset.target(e) 
                   for e in self.dataset.train)/len(self.dataset.train)
        self.predictor = lambda e:mean     # function that returns mean for each example
        self.predictor.__doc__ = "lambda e:"+str(mean)
        self.offsets = [self.predictor]  # list of base learners
        self.predictors = [self.predictor] # list of predictors
        self.errors = [data.evaluate_dataset(data.test, self.predictor, Evaluate.squared_loss)]
        self.display(1,"Predict mean test set mean squared loss=", self.errors[0] )


    def learn(self, num_ensembles=10):
        """adds num_ensemble learners to the ensemble.
        returns a new predictor.
        """
        for i in range(num_ensembles):
            train_subset = Boosted_dataset(self.dataset, self.predictor, subsample=self.subsample)
            learner = self.base_learner_class(train_subset)
            new_offset = learner.learn()
            self.offsets.append(new_offset)
            def new_pred(e, old_pred=self.predictor, off=new_offset):
                return old_pred(e)+off(e)
            self.predictor = new_pred
            self.predictors.append(new_pred)
            self.errors.append(data.evaluate_dataset(data.test, self.predictor, Evaluate.squared_loss))
            self.display(1,f"Iteration {len(self.offsets)-1},treesize = {new_offset.num_leaves}. mean squared loss={self.errors[-1]}")
        return self.predictor

# Testing

from learnDT import DT_learner
from learnProblem import Data_set, Data_from_file

def sp_DT_learner(split_to_optimize=Evaluate.squared_loss,
                             leaf_prediction=Predict.mean,**nargs):
    """Creates a learner with different default arguments replaced by **nargs
    """
    def new_learner(dataset):
        return DT_learner(dataset,split_to_optimize=split_to_optimize,
                                leaf_prediction=leaf_prediction, **nargs)
    return new_learner

#data = Data_from_file('data/car.csv', target_index=-1) regression
data = Data_from_file('data/student/student-mat-nq.csv', separator=';',has_header=True,target_index=-1,seed=13,include_only=list(range(30))+[32]) #2.0537973790924946
#data = Data_from_file('data/SPECT.csv', target_index=0, seed=62) #123)
#data = Data_from_file('data/mail_reading.csv', target_index=-1)
#data = Data_from_file('data/holiday.csv', num_train=19, target_index=-1)
#learner10 = Boosting_learner(data, sp_DT_learner(split_to_optimize=Evaluate.squared_loss, leaf_prediction=Predict.mean, min_child_weight=10))
#learner7 = Boosting_learner(data, sp_DT_learner(0.7))
#learner5 = Boosting_learner(data, sp_DT_learner(0.5))
#predictor9 =learner9.learn(10)
#for i in learner9.offsets: print(i.__doc__)
import matplotlib.pyplot as plt

def plot_boosting_trees(data, steps=10, mcws=[30,20,20,10], gammas= [100,200,300,500]):
    # to reduce clutter uncomment one of following two lines
    #mcws=[10]
    #gammas=[200]
    learners = [(mcw, gamma, Boosting_learner(data, sp_DT_learner(min_child_weight=mcw, gamma=gamma)))
                    for gamma in gammas for mcw in mcws
                    ]
    plt.ion()
    plt.xscale('linear')  # change between log and linear scale
    plt.xlabel("number of trees")
    plt.ylabel("mean squared loss")
    markers = (m+c for c in ['k','g','r','b','m','c','y'] for m in ['-','--','-.',':'])
    for (mcw,gamma,learner) in learners:
        data.display(1,f"min_child_weight={mcw}, gamma={gamma}")
        learner.learn(steps)
        plt.plot(range(steps+1), learner.errors, next(markers),
                     label=f"min_child_weight={mcw}, gamma={gamma}")
    plt.legend()
    plt.draw()

# plot_boosting_trees(data)

class GTB_learner(DT_learner):
    def __init__(self, dataset, number_trees, lambda_reg=1, gamma=0, **dtargs):
        DT_learner.__init__(self, dataset, split_to_optimize=Evaluate.log_loss, **dtargs)
        self.number_trees = number_trees
        self.lambda_reg = lambda_reg
        self.gamma = gamma
        self.trees = []

    def learn(self):
        for i in range(self.number_trees):
            tree = self.learn_tree(self.dataset.conditions(self.max_num_cuts), self.train)
            self.trees.append(tree)
            self.display(1,f"""Iteration {i} treesize = {tree.num_leaves} train logloss={
                self.dataset.evaluate_dataset(self.dataset.train, self.gtb_predictor, Evaluate.log_loss)
                    } test logloss={
                self.dataset.evaluate_dataset(self.dataset.test, self.gtb_predictor, Evaluate.log_loss)}""")
        return self.gtb_predictor

    def gtb_predictor(self, example, extra=0):
        """prediction for example,
        extras is an extra contribution for this example being considered
        """
        return sigmoid(sum(t(example) for t in self.trees)+extra)

    def leaf_value(self, egs, domain=[0,1]):
        """value at the leaves for examples egs
        domain argument is ignored"""
        pred_acts = [(self.gtb_predictor(e),self.target(e)) for e in egs]
        return sum(a-p for (p,a) in pred_acts) /(sum(p*(1-p) for (p,a) in pred_acts)+self.lambda_reg)


    def sum_losses(self, data_subset):
        """returns sum of losses for dataset (assuming a leaf is formed with no more splits)
        """
        leaf_val = self.leaf_value(data_subset)
        error = sum(Evaluate.log_loss(self.gtb_predictor(e,leaf_val), self.target(e))
                     for e in data_subset) + self.gamma
        return error

# data = Data_from_file('data/carbool.csv', target_index=-1, seed=123)
# gtb_learner = GTB_learner(data, 10)
# gtb_learner.learn()


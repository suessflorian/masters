# learnDT.py - Learning a binary decision tree
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnProblem import Learner, Evaluate
from learnNoInputs import Predict
import math

class DT_learner(Learner):
    def __init__(self,
                 dataset,
                 split_to_optimize=Evaluate.log_loss,     # to minimize for at each split 
                 leaf_prediction=Predict.empirical,   # what to use for value at leaves
                 train=None,                     # used for cross validation
                 max_num_cuts=8,   # maximum number of conditions to split a numerical feature into
                 gamma=1e-7  , # minimum improvement needed to expand a node
                 min_child_weight=10):
        self.dataset = dataset
        self.target = dataset.target
        self.split_to_optimize = split_to_optimize
        self.leaf_prediction = leaf_prediction
        self.max_num_cuts = max_num_cuts
        self.gamma = gamma
        self.min_child_weight = min_child_weight
        if train is None:
            self.train = self.dataset.train
        else:
            self.train = train

    def learn(self, max_num_cuts=8):
        """learn a decision tree"""
        return self.learn_tree(self.dataset.conditions(self.max_num_cuts), self.train)
        
    def learn_tree(self, conditions, data_subset):
        """returns a decision tree
        conditions is a set of possible conditions
        data_subset is a subset of the data used to build this (sub)tree

        where a decision tree is a function that takes an example and
        makes a prediction on the target feature
        """
        self.display(2,f"learn_tree with {len(conditions)} features and {len(data_subset)} examples")
        split, partn = self.select_split(conditions, data_subset)
        if split is None:  # no split; return a point prediction
            prediction = self.leaf_value(data_subset, self.target.frange)
            self.display(2,f"leaf prediction for {len(data_subset)} examples is {prediction}")
            def leaf_fun(e):
                return prediction
            leaf_fun.__doc__ = str(prediction)
            leaf_fun.num_leaves = 1
            return leaf_fun
        else:   # a split succeeded 
            false_examples, true_examples = partn
            rem_features = [fe for fe in conditions if fe != split]
            self.display(2,"Splitting on",split.__doc__,"with examples split",
                           len(true_examples),":",len(false_examples))
            true_tree = self.learn_tree(rem_features,true_examples)
            false_tree =  self.learn_tree(rem_features,false_examples)
            def fun(e):
                if split(e):
                    return true_tree(e)
                else:
                    return false_tree(e)
            #fun = lambda e: true_tree(e) if split(e) else false_tree(e)
            fun.__doc__ = (f"(if {split.__doc__} then {true_tree.__doc__}"
                           f" else {false_tree.__doc__})")
            fun.num_leaves = true_tree.num_leaves + false_tree.num_leaves
            return fun
        
    def leaf_value(self, egs, domain):
        return self.leaf_prediction((self.target(e) for e in egs), domain)
            
    def select_split(self, conditions, data_subset):
        """finds best feature to split on.

        conditions is a non-empty list of features.
        returns feature, partition
        where feature is an input feature with the smallest error as
              judged by split_to_optimize or
              feature==None if there are no splits that improve the error
        partition is a pair (false_examples, true_examples) if feature is not None
        """
        best_feat = None # best feature
        # best_error = float("inf")  # infinity - more than any error
        best_error = self.sum_losses(data_subset) - self.gamma
        self.display(3,"   no split has error=",best_error,"with",len(conditions),"conditions")
        best_partition = None
        for feat in conditions:
            false_examples, true_examples = partition(data_subset,feat)
            if min(len(false_examples),len(true_examples))>=self.min_child_weight:  
                err = (self.sum_losses(false_examples)
                       + self.sum_losses(true_examples))
                self.display(3,"   split on",feat.__doc__,"has error=",err,
                          "splits into",len(true_examples),":",len(false_examples),"gamma=",self.gamma)
                if err < best_error:
                    best_feat = feat
                    best_error=err
                    best_partition = false_examples, true_examples
        self.display(2,"best split is on",best_feat.__doc__,
                               "with err=",best_error)
        return best_feat, best_partition

    def sum_losses(self, data_subset):
        """returns sum of losses for dataset (with no more splits)
        There a single prediction for all leaves using leaf_prediction
        It is evaluated using split_to_optimize
        """
        prediction = self.leaf_value(data_subset, self.target.frange)
        error = sum(self.split_to_optimize(prediction, self.target(e))
                     for e in data_subset)
        return error

def partition(data_subset,feature):
    """partitions the data_subset by the feature"""
    true_examples = []
    false_examples = []
    for example in data_subset:
        if feature(example):
            true_examples.append(example)
        else:
            false_examples.append(example)
    return false_examples, true_examples


from learnProblem import Data_set, Data_from_file

def testDT(data, print_tree=True, selections = None, **tree_args):
    """Prints errors and the trees for various evaluation criteria and ways to select leaves.
    """
    if selections == None: # use selections suitable for target type
        selections = Predict.select[data.target.ftype]
    evaluation_criteria = Evaluate.all_criteria
    print("Split Choice","Leaf Choice\t","#leaves",'\t'.join(ecrit.__doc__
                                                 for ecrit in evaluation_criteria),sep="\t")
    for crit in evaluation_criteria:
        for leaf in selections:
            tree = DT_learner(data, split_to_optimize=crit, leaf_prediction=leaf,
                                   **tree_args).learn()
            print(crit.__doc__, leaf.__doc__, tree.num_leaves,
                    "\t".join("{:.7f}".format(data.evaluate_dataset(data.test, tree, ecrit))
                                  for ecrit in evaluation_criteria),sep="\t")
            if print_tree:
                print(tree.__doc__)

#DT_learner.max_display_level = 4
if __name__ == "__main__":
    # Choose one of the data files
    #data=Data_from_file('data/SPECT.csv', target_index=0); print("SPECT.csv")
    #data=Data_from_file('data/iris.data', target_index=-1); print("iris.data")
    data = Data_from_file('data/carbool.csv', target_index=-1, seed=123)
    #data = Data_from_file('data/mail_reading.csv', target_index=-1);  print("mail_reading.csv")
    #data = Data_from_file('data/holiday.csv', num_train=19, target_index=-1); print("holiday.csv")
    testDT(data, print_tree=False)
    

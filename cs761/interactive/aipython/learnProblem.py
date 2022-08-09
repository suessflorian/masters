# learnProblem.py - A Learning Problem
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

import math, random, statistics
import csv
from display import Displayable
from utilities import argmax

boolean = [False, True]

class Data_set(Displayable):
    """ A data set consists of a list of training data and a list of test data.
    """
    
    def __init__(self, train, test=None, prob_test=0.20, target_index=0,
                     header=None, target_type= None, seed=None): #12345):
        """A dataset for learning.
        train is a list of tuples representing the training examples
        test is the list of tuples representing the test examples
        if test is None, a test set is created by selecting each
            example with probability prob_test
        target_index is the index of the target. 
            If negative, it counts from right.
            If target_index is larger than the number of properties,
            there is no target (for unsupervised learning)
        header is a list of names for the features
        target_type is either None for automatic detection of target type 
             or one of "numerical", "boolean", "cartegorical"
        seed is for random number; None gives a different test set each time
        """
        if seed:  # given seed makes partition consistent from run-to-run
            random.seed(seed)
        if test is None:
            train,test = partition_data(train, prob_test)
        self.train = train
        self.test = test
        
        self.display(1,"Training set has",len(train),"examples. Number of columns: ",{len(e) for e in train})
        self.display(1,"Test set has",len(test),"examples. Number of columns: ",{len(e) for e in test})
        self.prob_test = prob_test
        self.num_properties = len(self.train[0])
        if target_index < 0:   #allows for -1, -2, etc.
            self.target_index = self.num_properties + target_index
        else:
            self.target_index = target_index
        self.header = header
        self.domains = [set() for i in range(self.num_properties)]
        for example in self.train:
            for ind,val in enumerate(example):
                self.domains[ind].add(val)
        self.conditions_cache = {}  # cache for computed conditions
        self.create_features()
        if target_type:
            self.target.ftype =  target_type
        self.display(1,"There are",len(self.input_features),"input features")

    def __str__(self):
        if self.train and len(self.train)>0: 
            return ("Data: "+str(len(self.train))+" training examples, "
                    +str(len(self.test))+" test examples, "
                    +str(len(self.train[0]))+" features.")
        else:
            return ("Data: "+str(len(self.train))+" training examples, "
                    +str(len(self.test))+" test examples.")

    def create_features(self):
        """create the set of features
        """
        self.target = None
        self.input_features = []
        for i in range(self.num_properties):
            def feat(e,index=i):
                return e[index]
            if self.header:
                feat.__doc__ = self.header[i]
            else:
                feat.__doc__ = "e["+str(i)+"]"
            feat.frange = list(self.domains[i])
            feat.ftype = self.infer_type(feat.frange)
            if i == self.target_index:
                self.target = feat
            else:
                self.input_features.append(feat)

    def infer_type(self,domain):
        """Infers the type of a feature with domain
        """
        if all(v in {True,False} for v in domain):
            return "boolean"
        if all(isinstance(v,(float,int)) for v in domain):
            return "numeric"
        else:
            return "categorical"
            
    def conditions(self, max_num_cuts=8, categorical_only = False):
        """returns a set of boolean conditions from the input features
        max_num_cuts is the maximum number of cute for numerical features
        categorical_only is true if only categorical features are made binary
        """
        if (max_num_cuts, categorical_only) in self.conditions_cache:
            return self.conditions_cache[(max_num_cuts, categorical_only)]
        conds = []
        for ind,frange in enumerate(self.domains):
            if ind != self.target_index and len(frange)>1:
                if len(frange) == 2:
                    # two values, the feature is equality to one of them.
                    true_val = list(frange)[1] # choose one as true
                    def feat(e, i=ind, tv=true_val):
                        return e[i]==tv
                    if self.header:
                        feat.__doc__ = f"{self.header[ind]}=={true_val}"
                    else:
                        feat.__doc__ = f"e[{ind}]=={true_val}"
                    feat.frange = boolean
                    feat.ftype = "boolean"
                    conds.append(feat)
                elif all(isinstance(val,(int,float)) for val in frange):
                    if categorical_only:  # numerical, don't make cuts
                        def feat(e, i=ind):
                            return e[i]
                        feat.__doc__ = f"e[{ind}]"
                        conds.append(feat)
                    else:
                        # all numeric, create cuts of the data
                        sorted_frange = sorted(frange)
                        num_cuts = min(max_num_cuts,len(frange))
                        cut_positions = [len(frange)*i//num_cuts for i in range(1,num_cuts)]
                        for cut in cut_positions:
                            cutat = sorted_frange[cut]
                            def feat(e, ind_=ind, cutat=cutat):
                                return e[ind_] < cutat

                            if self.header:
                                feat.__doc__ = self.header[ind]+"<"+str(cutat)
                            else:
                                feat.__doc__ = "e["+str(ind)+"]<"+str(cutat)
                            feat.frange = boolean
                            feat.ftype = "boolean"
                            conds.append(feat)
                else:
                    # create an indicator function for every value
                    for val in frange:
                        def feat(e, ind_=ind, val_=val):
                            return e[ind_] == val_
                        if self.header:
                            feat.__doc__ = self.header[ind]+"=="+str(val)
                        else:
                            feat.__doc__= "e["+str(ind)+"]=="+str(val)
                        feat.frange = boolean
                        feat.ftype = "boolean"
                        conds.append(feat)
        self.conditions_cache[(max_num_cuts, categorical_only)] = conds
        return conds

    def evaluate_dataset(self, data, predictor, error_measure):
        """Evaluates predictor on data according to the error_measure
        predictor is a function that takes an example and returns a
                prediction for the target features. 
        error_measure(prediction,actual) -> non-negative real
        """
        if data:
            try:
                value = statistics.mean(error_measure(predictor(e), self.target(e)) 
                            for e in data)
            except ValueError: # if error_measure gives an error
                return float("inf")  # infinity 
            return value
        else:
            return math.nan  # not a number

class Evaluate(object):
    """A container for the evaluation measures"""
    
    def squared_loss(prediction, actual):
        "squared loss  "
        if isinstance(prediction, (list,dict)):
             return (1-prediction[actual])**2 # the correct value is 1
        else:
             return (prediction-actual)**2

    def absolute_loss(prediction, actual):
        "absolute loss "
        if isinstance(prediction, (list,dict)):
             return abs(1-prediction[actual]) # the correct value is 1
        else:
            return abs(prediction-actual)

    def log_loss(prediction, actual):
        "log loss (bits)"
        try:
            if isinstance(prediction, (list,dict)):
                 return  -math.log2(prediction[actual])
            else:
                return -math.log2(prediction) if actual==1 else -math.log2(1-prediction)
        except ValueError:
            return float("inf")  # infinity 

    def accuracy(prediction, actual):
        "accuracy      "
        if isinstance(prediction, dict):
            prev_val = prediction[actual]
            return 1 if all(prev_val >= v for v in prediction.values()) else 0
        if isinstance(prediction, list):
            prev_val = prediction[actual]
            return 1 if all(prev_val >= v for v in prediction) else 0
        else:
            return 1 if abs(actual-prediction) <= 0.5 else 0

    all_criteria = [accuracy, absolute_loss, squared_loss, log_loss]

def partition_data(data, prob_test=0.30):
    """partitions the data into a training set and a test set, where
    prob_test is the probability of each example being in the test set.
    """
    train = []
    test = []
    for example in data:
        if random.random() < prob_test:
            test.append(example)
        else:
            train.append(example)
    return train, test

class Data_from_file(Data_set):
    def __init__(self, file_name, separator=',', num_train=None, prob_test=0.3,
                 has_header=False, target_index=0, boolean_features=True,
                 categorical=[], target_type= None, include_only=None, seed=None): #seed=12345):
        """create a dataset from a file
        separator is the character that separates the attributes
        num_train is a number specifying the first num_train tuples are training, or None 
        prob_test is the probability an example should in the test set (if num_train is None)
        has_header is True if the first line of file is a header
        target_index specifies which feature is the target
        boolean_features specifies whether we want to create Boolean features
            (if False, it uses the original features).
        categorical is a set (or list) of features that should be treated as categorical
        target_type is either None for automatic detection of target type 
             or one of "numerical", "boolean", "cartegorical"
        include_only is a list or set of indexes of columns to include
        """
        self.boolean_features = boolean_features
        with open(file_name,'r',newline='') as csvfile:
            self.display(1,"Loading",file_name)
            # data_all = csv.reader(csvfile,delimiter=separator)  # for more complicated CSV files
            data_all = (line.strip().split(separator) for line in csvfile)
            if include_only is not None:
                data_all = ([v for (i,v) in enumerate(line) if i in include_only]
                                for line in data_all)
            if has_header:
                header = next(data_all)
            else:
                header = None
            data_tuples = (interpret_elements(d) for d in data_all if len(d)>1)
            if num_train is not None:
                # training set is divided into training then text examples
                # the file is only read once, and the data is placed in appropriate list
                train = []
                for i in range(num_train):     # will give an error if insufficient examples
                    train.append(next(data_tuples))
                test = list(data_tuples)
                Data_set.__init__(self,train, test=test, target_index=target_index,header=header)
            else:     # randomly assign training and test examples
                Data_set.__init__(self,data_tuples, test=None, prob_test=prob_test,
                                  target_index=target_index, header=header, seed=seed, target_type=target_type)

class Data_from_files(Data_set):
    def __init__(self, train_file_name, test_file_name, separator=',', 
                 has_header=False, target_index=0, boolean_features=True,
                 categorical=[], target_type= None, include_only=None):
        """create a dataset from separate training and  file
        separator is the character that separates the attributes
        num_train is a number specifying the first num_train tuples are training, or None 
        prob_test is the probability an example should in the test set (if num_train is None)
        has_header is True if the first line of file is a header
        target_index specifies which feature is the target
        boolean_features specifies whether we want to create Boolean features
            (if False, it uses the original features).
        categorical is a set (or list) of features that should be treated as categorical
        target_type is either None for automatic detection of target type 
             or one of "numerical", "boolean", "cartegorical"
        include_only is a list or set of indexes of columns to include
        """
        self.boolean_features = boolean_features
        with open(train_file_name,'r',newline='') as train_file:
          with open(test_file_name,'r',newline='') as test_file:
            # data_all = csv.reader(csvfile,delimiter=separator)  # for more complicated CSV files
            train_data = (line.strip().split(separator) for line in train_file)
            test_data = (line.strip().split(separator) for line in test_file)
            if include_only is not None:
                train_data = ([v for (i,v) in enumerate(line) if i in include_only]
                                for line in train_data)
                test_data = ([v for (i,v) in enumerate(line) if i in include_only]
                                for line in test_data)
            if has_header:  # this assumes the training file has a header and the test file doesn't
                header = next(train_data)
            else:
                header = None
            train_tuples = [interpret_elements(d) for d in train_data if len(d)>1]
            test_tuples = [interpret_elements(d) for d in test_data if len(d)>1]
            Data_set.__init__(self,train_tuples, test_tuples, 
                                  target_index=target_index, header=header)

def interpret_elements(str_list):
    """make the elements of string list str_list numerical if possible.
    Otherwise remove initial and trailing spaces.
    """
    res = []
    for e in str_list:
        try:
            res.append(int(e))
        except ValueError:
            try:
                res.append(float(e))
            except ValueError:
                se = e.strip()
                if se in ["True","true","TRUE"]:
                    res.append[True]
                if se in ["False","false","FALSE"]:
                    res.append[False]
                else:
                    res.append(e.strip())
    return res

class Data_set_augmented(Data_set):
    def __init__(self, dataset, unary_functions=[], binary_functions=[], include_orig=True):
        """creates a dataset like dataset but with new features
        unary_function is a list of  unary feature constructors
        binary_functions is a list of  binary feature combiners.
        include_orig specifies whether the original features should be included
        """
        self.orig_dataset = dataset
        self.unary_functions = unary_functions
        self.binary_functions = binary_functions
        self.include_orig = include_orig
        self.target = dataset.target
        Data_set.__init__(self,dataset.train, test=dataset.test,
                          target_index = dataset.target_index)

    def create_features(self):
        if self.include_orig:
            self.input_features = self.orig_dataset.input_features.copy()
        else:
            self.input_features = []
        for u in self.unary_functions:
            for f in self.orig_dataset.input_features:
                self.input_features.append(u(f))
        for b in self.binary_functions:
            for f1 in self.orig_dataset.input_features:
                for f2 in self.orig_dataset.input_features:
                    if f1 != f2:
                        self.input_features.append(b(f1,f2))

def square(f):
    """a unary  feature constructor to construct the square of a feature
    """
    def sq(e):
        return f(e)**2
    sq.__doc__ = f.__doc__+"**2"
    return sq

def power_feat(n):
    """given n returns a unary  feature constructor to construct the nth power of a feature.
    e.g., power_feat(2) is the same as square, defined above
    """
    def fn(f,n=n):
        def pow(e,n=n):
            return f(e)**n
        pow.__doc__ = f.__doc__+"**"+str(n)
        return pow
    return fn

def prod_feat(f1,f2):
    """a new feature that is the product of features f1 and f2
    """
    def feat(e):
        return f1(e)*f2(e)
    feat.__doc__ = f1.__doc__+"*"+f2.__doc__
    return feat

def eq_feat(f1,f2):
    """a new feature that is 1 if f1 and f2 give same value
    """
    def feat(e):
        return 1 if f1(e)==f2(e) else 0
    feat.__doc__ = f1.__doc__+"=="+f2.__doc__
    return feat

def neq_feat(f1,f2):
    """a new feature that is 1 if f1 and f2 give different values
    """
    def feat(e):
        return 1 if f1(e)!=f2(e) else 0
    feat.__doc__ = f1.__doc__+"!="+f2.__doc__
    return feat

# from learnProblem import Data_set_augmented,prod_feat
# data = Data_from_file('data/holiday.csv', num_train=19, target_index=-1)
# data = Data_from_file('data/iris.data', prob_test=1/3, target_index=-1)
## Data = Data_from_file('data/SPECT.csv',  prob_test=0.5, target_index=0)
# dataplus = Data_set_augmented(data,[],[prod_feat])
# dataplus = Data_set_augmented(data,[],[prod_feat,neq_feat])
from display import Displayable
 
class Learner(Displayable):
    def __init__(self, dataset):
        raise NotImplementedError("Learner.__init__")    # abstract method

    def learn(self):
        """returns a predictor, a function from a tuple to a value for the target feature
        """
        raise NotImplementedError("learn")    # abstract method


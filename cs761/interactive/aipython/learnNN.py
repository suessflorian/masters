# learnNN.py - Neural Network Learning
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from learnProblem import Learner, Data_set, Data_from_file, Data_from_files, Evaluate
from learnLinear import sigmoid, one, softmax, indicator
import random, math, time

class Layer(object):
    def __init__(self, nn, num_outputs=None):
        """Given a list of inputs, outputs will produce a list of length num_outputs.
        nn is the neural network this layer is part of
        num outputs is the number of outputs for this layer.
        """
        self.nn = nn
        self.num_inputs = nn.num_outputs # output of nn is the input to this layer
        if num_outputs:
            self.num_outputs = num_outputs
        else:
            self.num_outputs = nn.num_outputs  # same as the inputs

    def output_values(self,input_values, training=False):
        """Return the outputs for this layer for the given input values.
        input_values is a list of the inputs to this layer (of length num_inputs)
        returns a list of length self.num_outputs.
        It can act differently when training and when predicting.
        """
        raise NotImplementedError("output_values")    # abstract method

    def backprop(self,errors):
        """Backpropagate the errors on the outputs
        errors is a list of errors for the outputs (of length self.num_outputs).
        Returns the errors for the inputs to this layer (of length self.num_inputs).
        
        You can assume that this is only called after corresponding output_values, 
           which can remember information information required for the back-propagation.
        """
        raise NotImplementedError("backprop")    # abstract method

    def update(self):
        """updates parameters after a batch.
        overridden by layers that have parameters
        """
        pass

class Linear_complete_layer(Layer):
    """a completely connected layer"""
    def __init__(self, nn, num_outputs, limit=None):
        """A completely connected linear layer.
        nn is a neural network that the inputs come from
        num_outputs is the number of outputs
        the random initialization of parameters is in range [-limit,limit]
        """
        Layer.__init__(self, nn, num_outputs)
        if limit is None:
            limit =math.sqrt(6/(self.num_inputs+self.num_outputs))
        # self.weights[o][i] is the weight between input i and output o
        self.weights = [[random.uniform(-limit, limit) if inf < self.num_inputs else 0
                          for inf in range(self.num_inputs+1)]
                        for outf in range(self.num_outputs)]
        self.delta = [[0 for inf in range(self.num_inputs+1)]
                        for outf in range(self.num_outputs)]

    def output_values(self,input_values, training=False):
        """Returns the outputs for the input values.
        It remembers the values for the backprop.

        Note in self.weights there is a weight list for every output,
        so wts in self.weights loops over the outputs.
        The bias is the *last* value of each list in self.weights.
        """
        self.inputs = input_values + [1]
        return [sum(w*val for (w,val) in zip(wts,self.inputs))
                    for wts in self.weights]

    def backprop(self,errors):
        """Backpropagate the errors, updating the weights and returning the error in its inputs.
        """
        input_errors = [0]*(self.num_inputs+1)
        for out in range(self.num_outputs):
            for inp in range(self.num_inputs+1):
                input_errors[inp] += self.weights[out][inp] * errors[out]
                self.delta[out][inp] += self.inputs[inp] * errors[out]
        return input_errors[:-1]   # remove the error for the "1"

    def update(self):
        """updates parameters after a batch"""
        batch_step_size = self.nn.learning_rate / self.nn.batch_size
        for out in range(self.num_outputs):
            for inp in range(self.num_inputs+1):
                self.weights[out][inp] -= batch_step_size * self.delta[out][inp]
                self.delta[out][inp] = 0
               
class ReLU_layer(Layer):
    """Rectified linear unit (ReLU) f(z) = max(0, z).
    The number of outputs is equal to the number of inputs. 
    """
    def __init__(self, nn):
        Layer.__init__(self, nn)

    def output_values(self, input_values, training=False):
        """Returns the outputs for the input values.
        It remembers the input values for the backprop.
        """
        self.input_values = input_values
        self.outputs= [max(0,inp) for inp in input_values]
        return self.outputs

    def backprop(self,errors):
        """Returns the derivative of the errors"""
        return [e if inp>0 else 0 for e,inp in zip(errors, self.input_values)]

class Sigmoid_layer(Layer):
    """sigmoids of the inputs.
    The number of outputs is equal to the number of inputs. 
    Each output is the sigmoid of its corresponding input.
    """
    def __init__(self, nn):
        Layer.__init__(self, nn)

    def output_values(self, input_values, training=False):
        """Returns the outputs for the input values.
        It remembers the output values for the backprop.
        """
        self.outputs= [sigmoid(inp) for inp in input_values]
        return self.outputs

    def backprop(self,errors):
        """Returns the derivative of the errors"""
        return [e*out*(1-out) for e,out in zip(errors, self.outputs)]

class NN(Learner):
    def __init__(self, dataset, validation_proportion = 0.1, learning_rate=0.001):
        """Creates a neural network for a dataset,
        layers is the list of layers
        """
        self.dataset = dataset
        self.output_type = dataset.target.ftype
        self.learning_rate = learning_rate
        self.input_features = dataset.input_features
        self.num_outputs = len(self.input_features)
        validation_num = int(len(self.dataset.train)*validation_proportion)
        if validation_num > 0:
            random.shuffle(self.dataset.train)
            self.validation_set = self.dataset.train[-validation_num:]
            self.training_set = self.dataset.train[:-validation_num]
        else:
            self.validation_set = []
            self.training_set = self.dataset.train
        self.layers = []
        self.bn = 0 # number of batches run

    def add_layer(self,layer):
        """add a layer to the network.
        Each layer gets number of inputs from the previous layers outputs.
        """
        self.layers.append(layer)
        self.num_outputs = layer.num_outputs

    def predictor(self,ex):
        """Predicts the value of the first output for example ex.
        """
        values = [f(ex) for f in self.input_features]
        for layer in self.layers:
            values = layer.output_values(values)
        return sigmoid(values[0]) if self.output_type =="boolean" \
               else softmax(values, self.dataset.target.frange) if self.output_type == "categorical" \
               else values[0]

    def predictor_string(self):
        return "not implemented"

    def learn(self, epochs=5, batch_size=32, num_iter = None, report_each=10):
        """Learns parameters for a neural network using stochastic gradient decent.
        epochs is the number of times through the data (on average)
        batch_size is the maximum size of each batch
        num_iter is the number of iterations over the batches
             - overrides epochs if provided (allows for fractions of epochs)
        report_each means give the errors after each multiple of that iterations
        """
        self.batch_size = min(batch_size, len(self.training_set)) # don't have batches bigger than training size
        if num_iter is None:
             num_iter = (epochs * len(self.training_set)) // self.batch_size
        #self.display(0,"Batch\t","\t".join(criterion.__doc__ for criterion in Evaluate.all_criteria))
        for i in range(num_iter):
            batch = random.sample(self.training_set, self.batch_size)
            for e in batch:
                # compute all outputs
                values = [f(e) for f in self.input_features]
                for layer in self.layers:
                    values = layer.output_values(values, training=True)
                # backpropagate
                predicted = [sigmoid(v) for v in values] if self.output_type == "boolean"\
                             else softmax(values) if self.output_type == "categorical"\
                             else values
                actuals = indicator(self.dataset.target(e), self.dataset.target.frange) \
                            if self.output_type == "categorical"\
                            else [self.dataset.target(e)]
                errors = [pred-obsd for (obsd,pred) in zip(actuals,predicted)]
                for layer in reversed(self.layers):
                    errors = layer.backprop(errors)
            # Update all parameters in batch
            for layer in self.layers:
                layer.update()
            self.bn+=1
            if (i+1)%report_each==0:
                self.display(0,self.bn,"\t",
                            "\t\t".join("{:.4f}".format(
                                self.dataset.evaluate_dataset(self.validation_set, self.predictor, criterion))
                               for criterion in Evaluate.all_criteria), sep="")

class Linear_complete_layer_momentum(Linear_complete_layer):
    """a completely connected layer"""
    def __init__(self, nn, num_outputs, limit=None, alpha=0.9, epsilon = 1e-07, vel0=0):
        """A completely connected linear layer.
        nn is a neural network that the inputs come from
        num_outputs is the number of outputs
        max_init is the maximum value for random initialization of parameters
        vel0 is the initial velocity for each parameter
        """
        Linear_complete_layer.__init__(self, nn, num_outputs, limit=limit)
        # self.weights[o][i] is the weight between input i and output o
        self.velocity = [[vel0 for inf in range(self.num_inputs+1)]
                        for outf in range(self.num_outputs)]
        self.alpha = alpha
        self.epsilon = epsilon

    def update(self):
        """updates parameters after a batch"""
        batch_step_size = self.nn.learning_rate / self.nn.batch_size
        for out in range(self.num_outputs):
            for inp in range(self.num_inputs+1):
                self.velocity[out][inp] = self.alpha*self.velocity[out][inp] - batch_step_size * self.delta[out][inp]
                self.weights[out][inp] += self.velocity[out][inp]
                self.delta[out][inp] = 0
               
class Linear_complete_layer_RMS_Prop(Linear_complete_layer):
    """a completely connected layer"""
    def __init__(self, nn, num_outputs, limit=None, rho=0.9, epsilon = 1e-07):
        """A completely connected linear layer.
        nn is a neural network that the inputs come from
        num_outputs is the number of outputs
        max_init is the maximum value for random initialization of parameters
        """
        Linear_complete_layer.__init__(self, nn, num_outputs, limit=limit)
        # self.weights[o][i] is the weight between input i and output o
        self.ms = [[0 for inf in range(self.num_inputs+1)]
                        for outf in range(self.num_outputs)]
        self.rho = rho
        self.epsilon = epsilon

    def update(self):
        """updates parameters after a batch"""
        for out in range(self.num_outputs):
            for inp in range(self.num_inputs+1):
                gradient = self.delta[out][inp] / self.nn.batch_size
                self.ms[out][inp] = self.rho*self.ms[out][inp]+ (1-self.rho) * gradient**2
                self.weights[out][inp] -= self.nn.learning_rate/(self.ms[out][inp]+self.epsilon)**0.5 * gradient
                self.delta[out][inp] = 0
               
from utilities import flip
class Dropout_layer(Layer):
    """Dropout layer
    """
    
    def __init__(self, nn, rate=0):
        """
        rate is fraction of the input units to drop. 0 =< rate < 1
        """
        self.rate = rate
        Layer.__init__(self, nn)
        
    def output_values(self, input_values, training=False):
        """Returns the outputs for the input values.
        It remembers the input values for the backprop.
        """
        if training:
            scaling = 1/(1-self.rate)
            self.mask = [0 if flip(self.rate) else 1 
                           for _ in input_values]
            return [x*y*scaling for (x,y) in zip(input_values, self.mask)]
        else:
            return input_values

    def backprop(self,errors):
        """Returns the derivative of the errors"""
        return [x*y for (x,y) in zip(errors, self.mask)]

class Dropout_layer_0(Layer):
    """Dropout layer
    """
    
    def __init__(self, nn, rate=0):
        """
        rate is fraction of the input units to drop. 0 =< rate < 1
        """
        self.rate = rate
        Layer.__init__(self, nn)
        
    def output_values(self, input_values, training=False):
        """Returns the outputs for the input values.
        It remembers the input values for the backprop.
        """
        if training:
            scaling = 1/(1-self.rate)
            self.outputs= [0 if flip(self.rate) else inp*scaling # make 0 with probability rate
                           for inp in input_values]
            return self.outputs
        else:
            return input_values

    def backprop(self,errors):
        """Returns the derivative of the errors"""
        return errors

#data = Data_from_file('data/mail_reading.csv', target_index=-1)
#data = Data_from_file('data/mail_reading_consis.csv', target_index=-1)
data = Data_from_file('data/SPECT.csv',  prob_test=0.5, target_index=0)
#data = Data_from_file('data/iris.data', prob_test=0.2, target_index=-1) # 150 examples approx 120 test + 30 test
#data = Data_from_file('data/if_x_then_y_else_z.csv', num_train=8, target_index=-1) # not linearly sep
#data = Data_from_file('data/holiday.csv', target_index=-1) #, num_train=19)
#data = Data_from_file('data/processed.cleveland.data', target_index=-1)
random.seed(None)

nn1 = NN(data, validation_proportion = 0)
nn1.add_layer(Linear_complete_layer(nn1,3))
#nn1.add_layer(Sigmoid_layer(nn1))  # comment this or the next
nn1.add_layer(ReLU_layer(nn1))
nn1.add_layer(Linear_complete_layer(nn1,1)) # when using output_type="boolean"
#nn1.add_layer(Linear_complete_layer(nn1,1)) # when using output_type="categorical" 
#nn1.learn(epochs = 100)

nn1do = NN(data)
nn1do.add_layer(Linear_complete_layer(nn1do,3))
#nn1.add_layer(Sigmoid_layer(nn1))  # comment this or the next
nn1do.add_layer(ReLU_layer(nn1do))
nn1do.add_layer(Dropout_layer(nn1do, rate=0.5))
#nn1.add_layer(Linear_complete_layer(nn1do,1)) # when using output_type="boolean"
nn1do.add_layer(Linear_complete_layer(nn1do,1)) # when using output_type="categorical" 
#nn1do.learn(epochs = 100)


nn_r1 = NN(data)
nn_r1.add_layer(Linear_complete_layer_RMS_Prop(nn_r1,3))
#nn_r1.add_layer(Sigmoid_layer(nn_r1))  # comment this or the next
nn_r1.add_layer(ReLU_layer(nn_r1)) 
#nn_r1.add_layer(Linear_complete_layer(nn_r1,1)) # when using output_type="boolean"
nn_r1.add_layer(Linear_complete_layer_RMS_Prop(nn_r1,1)) # when using output_type="categorical" 
#nn_r1.learn(epochs = 100)


nnm1 = NN(data)
nnm1.add_layer(Linear_complete_layer_momentum(nnm1,3))
#nnm1.add_layer(Sigmoid_layer(nnm1))  # comment this or the next
nnm1.add_layer(ReLU_layer(nnm1)) 
#nnm1.add_layer(Linear_complete_layer(nnm1,1)) # when using output_type="boolean"
nnm1.add_layer(Linear_complete_layer_momentum(nnm1,1)) # when using output_type="categorical" 
#nnm1.learn(epochs = 100)


nn2 = NN(data) #"boolean") #
nn2.add_layer(Linear_complete_layer_RMS_Prop(nn2,2))
nn2.add_layer(ReLU_layer(nn2)) 
nn2.add_layer(Linear_complete_layer_RMS_Prop(nn2,1)) # when using output_type="categorical" 

nn3 = NN(data) #"boolean") #
nn3.add_layer(Linear_complete_layer_RMS_Prop(nn3,5))
nn3.add_layer(ReLU_layer(nn3)) 
nn3.add_layer(Linear_complete_layer_RMS_Prop(nn3,1)) # when using output_type="categorical" 

nn0 = NN(data,learning_rate=0.05)
nn0.add_layer(Linear_complete_layer(nn0,1)) # categorical linear regression
#nn0.add_layer(Linear_complete_layer_RMS_Prop(nn0,1)) # categorical linear regression

from learnLinear import plot_steps
from learnProblem import Evaluate

# To show plots:
# plot_steps(learner = nn1, data = data, criterion=Evaluate.log_loss, num_steps=10000, log_scale=False, legend_label="nn1")
# plot_steps(learner = nn2, data = data, criterion=Evaluate.log_loss, num_steps=10000, log_scale=False, legend_label="nn2")
# plot_steps(learner = nn3, data = data, criterion=Evaluate.log_loss, num_steps=100000, log_scale=False, legend_label="nn3")
# plot_steps(learner = nn0, data = data, criterion=Evaluate.log_loss, num_steps=10000, log_scale=False, legend_label="nn0")

# plot_steps(learner = nn0, data = data, criterion=Evaluate.accuracy, num_steps=10000, log_scale=False, legend_label="nn0")
# plot_steps(learner = nn1, data = data, criterion=Evaluate.accuracy, num_steps=10000, log_scale=False, legend_label="nn1")
# plot_steps(learner = nn2, data = data, criterion=Evaluate.accuracy, num_steps=10000, log_scale=False, legend_label="nn2")
# plot_steps(learner = nn3, data = data, criterion=Evaluate.accuracy, num_steps=10000, log_scale=False, legend_label="nn3")


# Print some training examples
#for eg in random.sample(data.train,10): print(eg,nn1.predictor(eg))

# Print some test examples
#for eg in random.sample(data.test,10): print(eg,nn1.predictor(eg))

# To see the weights learned in linear layers
# nn1.layers[0].weights
# nn1.layers[2].weights

# Print test:
# for e in data.train: print(e,nn0.predictor(e))

def test(data, hidden_widths = [5], epochs=100,
             optimizers = [Linear_complete_layer,
                        Linear_complete_layer_momentum, Linear_complete_layer_RMS_Prop]):
    data.display(0,"Batch\t","\t".join(criterion.__doc__ for criterion in Evaluate.all_criteria))
    for optimizer in optimizers:
        nn = NN(data)
        for width in hidden_widths:
            nn.add_layer(optimizer(nn,width))
            nn.add_layer(ReLU_layer(nn))
        if data.target.ftype == "boolean":
            nn.add_layer(optimizer(nn,1))
        else:
            error(f"Not implemented: {data.output_type}")
        nn.learn(epochs)

# Simplified version: (6000 training instances)
# data_mnist = Data_from_file('../MNIST/mnist_train.csv', prob_test=0.9, target_index=0, boolean_features=False, target_type="categorical")

# Full version:
# data_mnist = Data_from_files('../MNIST/mnist_train.csv', '../MNIST/mnist_test.csv', target_index=0, boolean_features=False,  target_type="categorical")

# nn_mnist = NN(data_mnist, validation_proportion = 0.02, learning_rate=0.001) #validation set = 1200 
# nn_mnist.add_layer(Linear_complete_layer_RMS_Prop(nn_mnist,512)); nn_mnist.add_layer(ReLU_layer(nn_mnist)); nn_mnist.add_layer(Linear_complete_layer_RMS_Prop(nn_mnist,10))
# start_time = time.perf_counter();nn_mnist.learn(epochs=1, batch_size=128);end_time = time.perf_counter();print("Time:", end_time - start_time,"seconds")  #1 epoch
# determine test error:
# data_mnist.evaluate_dataset(data_mnist.test, nn_mnist.predictor, Evaluate.accuracy)
# Print some random predictions:
# for eg in random.sample(data_mnist.test,10): print(data_mnist.target(eg),nn_mnist.predictor(eg),nn_mnist.predictor(eg)[data_mnist.target(eg)])

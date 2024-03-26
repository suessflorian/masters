# Deep Learning (part 1)
Classical ML methods have a couple of characteristics (by classical I assume we're speaking of decision tree classifiers etc...);
- Needs expert knowledge about the data to design features
- Can be complex to design or/and select good feature
- Not best use of the huge amount of data now available
- Hard to transfer

## Why deep learning?
Basically exactly counteracts the above points made...
- No need for feature engineering and selection anymore
- Scale with the amount of training data available
- Easier to transfer to other tasks/domains
- Better performance on a lot of tasks/domains

Not to say that classical ML methods are obsolete, far from that, in fact you can view the classical methods as still effective. Particularly comparable in situations where dataset quantities are small.

## Perceptron Model
As invented in 1940's. I should be very familiar with this, including the associated weights to each input, the bias, the summation, the activation and output - the parallel to typical vector arithmetic, important detail that platforms a lot of matrix multiplication focus in libraries today due to the NN layer abstractions that can be made.

## Neural Network
Input layer, hidden and output layer. D-NN's are considered when we have at least 2 hidden layers.

### Non-linearity in activation function
If no activation function, output neuron is just the vector of inputs dot product with the vector of associated weights + some bias term. This ofcourse inherently limits the modelling of only linear relationships in the application of NN's (as an arbitrary composition of linear functions is also linear), hence the need for some sort of non-linear activation function that takes this vector dot product as argument.

### Favourable characteristics in the Activation Function
With foresight, we want a function that; 
- Counteracts the vanishing/exploding gradients problem.
- Zero-centered: symmetrical, helps to form derivatives that have a bias toward one direction (? why)
- Computationally inexpensive; not these functions are computed a lot.
- Smooth (mostly): to be able to actually calculate the gradient for backprop.

## Output layer activations
- Sigmoid activation for binary
- Softmax for multi-class
- Multi-label number of outputs each with their own sigmoid activation
- Regression, typically a linear activation function

# Optimisation Problem (Learning)
Weights and biases tuned to minimise cost/loss/error.

High-level;
- Perform update in downhill direction of each coordinate (partial derivative of loss function with respect to the weight evaluated "at the current weights point")
- The steeper the slope (higher derivative) the bigger the step for that coordinate.
- The overall gradient of the loss function at the current weight position can then be visualised as a vector which can be combined (although multiplied by a learning rate/step) with the existing weight vector of each perception.

## Descent styles
For "classic gradient descent" takes your training set and averages out the gradient vector of each perception (loss backprop via chain rule of each training example) and then applied once in the step of the learning rate.

"Stochastic" refers to random sampling, "stochastic gradient descent" randomly chooses one to build a gradient from and updates the weights accordingly.

"Mini-batch" stochastic gradient descent averages a relative to the training set "small" group of training examples to build a gradient. Idea is that it's a bit more stable than using a single training example as you minimise the risk of picking a very unrepresentative training example.

## Hyperparameters
Learning rate is supposedly the most important hyper parameter in neural networks... hard to know in advance which would be ideal. We typically do a search on this (among others) and this links us to the familiar science of finding the best combination of hyper parameters (concept of hyper parameter space);

- Grid/random searching
- Sensitivity analysis
- Optimisation technics

**NN hyperparameters**: numbers of layers, number of neurons per layer, activation function, learning rate, weight inits, mini-batch size etc...

## Learning Rate
### Decay
- Decay schedule, decrease learning rate over time
- Linear decay, exponential decay etc... Based on number of iterations, then flat line a constant rate.
- Step-based, how much drop per epoch

Why? The gradients of the loss function with respect to weights become less steep the closer you are to a local minima. We also handle deterministic overshooting of local minima, as the function is non convex this is not necessarily great or bad, but at least the indication of having reached _some_ local minima is ideal.

Note; the classic SGD algorithm has a typically fixed learning rate value.

### Adaptive
- Monitors the model's performance and adapt the learning rate in response.
- Reduces learning rate when performance plateus;
- Increases learning rate when performance does not improve for a number of iterations.

Adaptive algorithms out there, Adagrad, RMSProp, AdaDelta, ADAM. Turns out that adaptive learning generally outperform fixed and not well tuned learning rates.

# Empirical and Iterative Evaluation
Evaluation: cost function, evaluation strategy. Split train, validation, test (golden rule).

Split size, you want to prioritise your model is tested correctly, providing to you the better estimate of real life performance -> meaning if small dataset, typically more allocation percentage wise (20%) to validation/tests. Otherwise if large then a lower allocation percentage is fine (1%) to validation/tests.

# Bias/Variance tradeoff
Important to keep in mind relationships to overfitting (high variance, low bias) and underfitting (low variance, high bias).

## Application to Deep learning
Deep learning techniques are shown to be able to completely eat your training data, allowing a form of data memorization which means that training error might drop far below testing error. Model complexity is to blame here.

### Regularisation
L1 & L2 where quite common regularisation techniques but **dropout** is shown to be very effective and used commonplace. Others

- Early stopping
- Data augmentation
- Batch normalization

#### L1 & L2
Quick video tutorial ([here](https://www.youtube.com/watch?v=pJ5c_uLeg2A)) notes; 
- Applied to linear regression, logistic regression, SVM's and NN's.
- "LP Norm", L1 (lasso) and L2 (ridge)
- L1 (penalises abs) tends to sends weights to zero, thus leading to an effect of feature selection pruning.
- L2 (penalises square) tends to send weights closer to zero, although still leaving them above zero. Leading to a sort of smoothing of loud coefficients.

## Intuitions
First; penalises dominating weight values, second; assuming zero centered activation function pushes a neuron to the linear zone of the function causing restricted ability for individual neurons to model non-linear relationships.

# Optimal Error rate
Theoretical optimal error rate, you want to get as close as you can to this. Hard to estimate.

- Avoidable bias, the space between the training error and this theoretical optimal error rate.
- Variance, the space between the training error and validation error.

## Addressing High Avoidable Bias
Model is not complex enough to map inputs and outputs, simple fix would be to increase model size somehow via increased layers or neurons per layer. Might increase variance by doing this and ofcourse we're now risking a step toward overfiting and if needed to talk to this area, would need to be regularised. This complexity increase also comes at the cost of increased compute requirement.

## Addressing High Variance
Training data not sufficient to generalise on validation data, simple fix would be to add data to the training set, more data although might not be available - data augmentation could be a viable option in this situation.

# Bias Variance tradeoff
You're always going to be balancing these two.

## PAPERS EXAMINABLE
- Motivations
- Key Points
- Conclusions


## R-NN
Explain the primary advantage of using LSTM's model over the traditional R-NN model for sequence data processing.

R-NN's are geared toward sequential processing by fundamentally including the mechanism of passing forward internal hidden state that is derived from previous input processing operations. This can be seen as contextual information when processing the next input in a sequence.

As per normal feed forward NN's, you can express all operations in the form of a computation graph, although for R-NN's the computation graph becomes linearly larger than a typical feed forward NN which means that model weights are a lot further removed from the final output as before, inducing the well known "vanishing gradient" problem.

LSTM's, or long-term short term memory architectures attempt to tackle this issue, by selectively remembering and forgetting information over long sequences. They incorporate memory cells and three types of gates (input, forget and output gates) to control the flow of information. These components work together to maintain a more stable gradient across longer sequences, allowing the model to remember more clearly thus helping the vanishing gradient problem.

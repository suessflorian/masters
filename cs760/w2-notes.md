# Understanding Deep Learning (Still) Requires Rethinking Generalisation
Highly accredited author; most cited paper by [Chiyuan Zhang](https://scholar.google.com/citations?user=l_G2vr0AAAAJ&hl=en).

## Motivation
"What is then that distinguishes NN's that generalise well from those that don't."

### Background

#### Generalisation Error
Difference between training error and test error.

#### Model Capacity
Universal Approximation Theorem "a feed-forward network with a single hidden layer containing a finite number of neurons, can approximate any continuous function on compact subsects of R^n"
    - Proved for Sigmoid Activation Functions

Does not define the algorithmic learnability of those parameters.

If you have a single layer NN, we can approximate any possible continuous function. But we may not be able to learn the weights to that network effectively.

VC-Dimension (Vapnik-Chervonenkis)
- A classification model `f` with some parameter vector theta, is said to *shatter* a set of data points if, for all assignments of labels to those points, there exists a theta such that `f` makes **no errors** when evaluating that set of data points.
- VC-Dimension of a model `f` is the maximum number of data points that can be arranged so that `f` shatters them.
    - We can use it to build an probabilistic upper bound on test error

#### Regularization
##### Explicit
- Weight Decay; wt+1 <- wt - learning_rate derivate of partial L(w) / partial w_t
- Dropout; randomly drop neurons from layers, removes reliance on individual neurons
    - note redundancies, but hopefully, learns more nuanced set of feature detectors
- Data Augmentation; domain specific transformations of the input data. Flipping, rotating, cropping, colour jittering, edge enhancement, PCA.

##### Implict
- Early Stopping; 
- Batch Normaliszation
- SGD

import numpy as np
import torch

data = [[1, 2],[3, 4]]

# NOTE: the two lines here
x_data = torch.tensor(data)
np_array = np.array(data)

# are best known to be equivalent
x_data = torch.from_numpy(np_array)
print(f"Parsed: \n {x_data} \n")

x_ones = torch.ones_like(x_data) # NOTE: retains the properties of x_data
print(f"Ones Tensor: \n {x_ones} \n")

x_rand = torch.rand_like(x_data, dtype=torch.float)
print(f"Rand Tensor: \n {x_rand} \n")

# NOTE: shape is a tuple of tensor dimensions. 
shape = (2, 3)
rand_tensor = torch.rand(shape)
ones_tensor = torch.ones(shape)
zeros_tensor = torch.zeros(shape)

print(f"(shape) Random Tensor: \n {rand_tensor} \n")
print(f"(shape) Ones Tensor: \n {ones_tensor} \n")
print(f"(shape) Zeros Tensor: \n {zeros_tensor}")

# NOTE: attributes
tensor = torch.rand(3,4)

print(f"Shape of tensor: {tensor.shape}")
print(f"Datatype of tensor: {tensor.dtype}")
print(f"Device tensor is stored on: {tensor.device}")

# NOTE: We move our tensor to Nvidea GPU if available
if torch.cuda.is_available():
    tensor = tensor.to("cuda")
    print(f"Can move to device: {tensor.device}")

# NOTE: We move our tensor to Metal Performance Shaders if available
if torch.backends.mps.is_available():
    tensor = tensor.to("mps")
    print(f"Can move to device: {tensor.device}")

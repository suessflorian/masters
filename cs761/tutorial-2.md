# Iterative Deepening A* Search (1st Aug)
Looks like we missed a section in a lecture related to A* search algorithm. So we covered a good chunk of it during this lecture instead

## The general idea
It is a low memory variant of A*. Performs a **series** of DFS's but cuts off each search when the sum f() = g() + h() exceeds some threshold. *We iteratively increase this threshold*. Asymptotically as efficient as A* for domains where the number of states grows exponentially.

Compared to ID-DFS: at each iteration, the **f threshold used** for the next iteration is the minimum cost of all current values in the frontier of the previous iteration.

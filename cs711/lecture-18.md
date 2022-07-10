# Continuing on document model p2p: Chord
ID space assembles a ring. Nodes and files associated to these identifiers. Files similarily to CAN are determined _close_ to a node dependaning on their ID distance. Ring is defined as addition modulo 2, hence closure etc... Each node hosts a finger table.

If a ring has size `2^n`, finger table of node `N` has length `n`; keys by `(N + 2^n-1) % 2`.

So example:
- 1, (next successor 1 away from `N`)
- 2, ...
- 4,
- 8,
- ...

When a client connects to some participating per, and requests for file `L`, a function is used to determine the corresponding identifier relative to the ring. The current peer then forwards the request to `L` to the machine closest to the request ID according to this finger table.

## Redundancy, similar to CAN, just add a secondary hashing function for file/node placement, although restrict to only file placement

### What happens when a new node wants to join this P2P model?
TBD, lecture wasn't super clear... :/

# Garbage Collection
We look at an example that highlights the flaw of reference counting technique in a distributed system.

Essentially what we find, is that the two operations
1. increasing
2. decreasing
The reference count can happen out of order...

So the general strategy for a distributed system is to only have one operation, namely `decreasing`.

## Weighted Reference Counting
- an object has a `weight`
- assign `weight` to each `pointer`
- object weight = sum of the pointer's weight
- when the pointer is copied, evenly distribute the weight
- when a pointer is deleted, the weight of the pointer is substracted from weight of obj
- obj GC'd if obj weight reaches 0

Now.... suppose we cannot split a weighted edge further, we create an indirection object. To which references of this object are weighted sufficiently high again.

_tradeoff with above is when de-referencing a pointer, you will have to incorporate pointer jumps causing a bit of a slowdown_

### Issue with GC, cyclic references.
We introduce a complementory algorithm aimed to collecting `cyclic garbage`

If an object, A, has a reference to another object, B, then A is the `predecessor` to B. Vice versa B, is A's `successor`.

So given `O`, to represent a set of objects, and `P` be the set of `O`'s predecessor's. It is easy to see that if all objects in O form a cyclic structure, P must be a subset of O.

**33min algorithm begins**

We use the fact that given a set for `O`, if `P` is subset of `O`, we deduce `O` to be garbage.

#### Implementation:
For a suspect in `O`, we initiate a probe.

Intiator hosts a `received probe weight` variable; `rw`.

Sends probe with weight `n` to all it's neighbours down object reference pointer paths. If there exists more than one neighbour, `n` is allocated somewhat evenly between them.

Suppose a node receives a probe that has already been sent a probe earlier, the "currently receiving" probe is sent back to the intiator. The initiator adds to `rw` value (terminating if `rw` = the initial `n` sent out).

If node has not received a probe before - it forwards the probe to it's children, ensuring `n` of that probe is spread evenly, but moreover, attaches the predecessor relationship to the probe.

**Intiator knows termination when `rw` = `n`**

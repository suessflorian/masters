# Deadlocks + Garbage Collection
Continuing on the Echo algorithm. Note, it is originally designed for network topology discovery.

Learnt about
- AND Dependancy Models
- OR Dependancy Models

`Wait-For` directed graph - direction determines `depends-on`. 

### Cycles in AND models determine deadlocks.

`knots`; where each vertix inside a knot has an outgoing edge pointing to another vertix belonging to the knot.

### Knots in a OR models determine deadlocks.

## We talked about deadlock detection algorithms
Supposedly a central deadlock detection manager has it's flaws. Demonstration given in that lecture. I feel like the example was loose. Essentially the asynchronous nature of process resource request updates may cause the depends-on graph to potentially represent a none existing deadlock.

#### Cycle detection algorithm
To have the following 2 properties
- detects all deadlocks
- does not detect deadlock when there is no deadlock
**deadlock detection iff system in deadlock state**

```
Note that we do not focus on deadlock resolution algorithms. 
But as a summary we'd need to:
- break existing wait-for dependancies in a deadlocked AND/OR model graph
- involves rolling back processes to let go of shared resources
```

## Distributed scheme for AND Cycle Models
probe signal, (i, j, k) (initiator, source, destination)
- if receiving probe, forward to it's dependants.
- if no dependancies - probe is dropped.
- if initatior receives it's own probe, well then we have a cycle.

## Distributed scheme for OR Cycle Models
- each blocked task passes down a probe along edges in wait-for graph
- if node participates in algo if it depends on another vertix
- if echo algorithm terminates, means deadlock is detected

# Intro into Garbage Collection
Essentially during the life of program, objects get created, and discarded. Garbage collection is an automatic process that finds stale objects and discards them, freeing the underlying memory.

The most common techniques in a centralised system is `reference counting`
- each object keeps a `reference count`
- when reference is copied, count goes up
- when reference is deleted, count goes down
- when reference count reaches 0, indicates that the object can be removed.

## Problems in a distributed system
- due to asynchronous behaviour of system updates, a central GC system might (similar to deadlock detection), detect an object with zero references prematurely.

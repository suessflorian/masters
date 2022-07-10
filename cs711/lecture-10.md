# Continuing on Maekawa's Algo
Focusing on how `relinquish` and `inquire` messages work on deadlock events.

Essentially inside a quorom, given a process that has allocated a vote, if a process receives a resource req with a timestamp that is comparatively smaller that 

## Token Based
`Raymonds` algo
- unique token is shared among tasks
- task is allowed access to shared resource iff it's holding that token
- each task is a node in the same tree
- each task accomodates `holder`, a pointer that points to one of it's direct neighbour nodes that knows who has the token.
- if task needs shared resource access, task sends a `token request` to the neighbour that might hold the token.
- if task receives `token request` and does not host the token, forwards the request to the node indicated by `holder`.

### Algo
Each task has a queue, call it `request_q`, records ID of the neighbour from which `token request` comes from.

Two routines:
1. `ASSIGN PRIVELAGE` - if first element in `request_q` is self **AND** we hold the token?
	- ACCESS Resource (remove itself from `request_q`)
**IF NOT**
	- Give token to node indicated by the first element in the `request_q`

2. `MAKE REQUEST` - if task has not sent any `token_request` to the neighbour indicated by `holder`, sends `token_request` message to the neighbour indicated by `holder`

#### Intialisation Step
I mean it exists, pretty intuitive, but we have to give some task the token. And propogate task `holder` var to point to the neighbour that knows where the token lives.

See 28min of `2022-03-21` for demonstration of resource req being served.

## The ECHO Algorithm
New topic! Deadlock detection. (later we will use this algo in particular to detect these deadlocks).

Don't think, given a tree of nodes. Imagine an intiator triggering an echo and visualise it. Enough intuition to derive what is going on. See 38:20min of lecture `2022-03-21`.

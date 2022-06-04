# Consensus Problem
Many processes in a distributed system want to reach an agreement. Assumptions going forward are simply natural.

No specific mention of FIFO, only reliability. Also at most 1 node fails, to which it may restart.

**Fault-tolerant** consensus protocol.
- Collect votes from N nodes
- Wait for majority response
- Tell everyone the outcome (decree it)
- Nodes "decide"
- Problem if message delayed or node restarts

## FLP Impossibility Of Consensus
*Intuition*
1. System tries to reach consensus
2. Node p's messages are `delayed` during transmission
3. System is Fault-tolerant, if p crashes, system should `adapt` and move on
4. Before decision is made, p's message `now arrives` => p must be involved in decision
5. `step 1`

As interesting of a proof as this is, field experts point out that a formal proof like FLP needs to show:
- safeness (intended consensus is reached)
- always terminates (no deadlock)

FLP proves Fault-tolerant algorithm solving consensus `never terminates`...
**In practice though these runs are extremely unlikely** ("zero probability")

IE, FLP only shows consensus is `not always` possible.

## Paxos Algorithm
Assumptions:
- `N` Nodes, the set of node is known a-priori.
- Nodes suffer `crash` failures, nodes can restart after a failure
- Network might be very `slow`
Guarantees safety
- Only a `single` value is chosen
- Only a `proposed` value can be chosen
- A process `never` learns that a value has been chosen unless it actually has been

By `FLP` then, cannot guarantee `liveness`.

### Overview
- Nodes make proposals to become a `leader` of a group
- Each proposal is associated with a `version` number
- A proposal only needs to be sent to a `majority` of the nodes
- A proposal accepted by a `majority` of nodes will get `passed` (consensus value)
- Node always accepts proposals with larger `version` numbers

### Details

## 3 roles
- proposer
- acceptor
- learner

## 3 phases
### PHASE 1. **prepare**
`proposer` chooses new version number `n` and asks the following two things of all it's neighbours:
- can I make a proposal with a number `n`?
- if yes, do you suggest a value for my proposal?

`acceptor` receives ("prepare", `n`) when `n` is the largest version number its seen so far: 
responds with `("ack", n, -, -)`, meaning:
- it promises not to accept	any proposal with version number less than `n`
- third arg, can actually be `v'` which denotes the current value "proposed" from the highest version number "accept" message
**IF IT IS NOT THE LARGEST VERSION NUMBER**
- abandons the engagement with the proposer with a smaller version number and continues to engage with the proposer with the larger version.

### PHASE 2 (if positive replies from a majority of the nodes): **propose**
If the proposer receives responses from a majority of the acceptors, it can issue a proposal value.

`proposer`
- Sends `("accept", n, v)`, n is the version number from step 1. `v` is the value of the highest version number proposal among the responses (if any), otherwise it creates it's own.

`acceptor`
- upon receiving `("accept", n, v)` it accepts the proposal unless it has already responded to a `prepare` request with a higher version number.
- upon accepting, immediately writes to stable storage the message (fault tolerance)
- returns some sort of `"ack"` message back to the `proposer`

### PHASE 3 (if positive replies from a majority of the nodes): **finalise**

`proposer`
- if receives `"ack"` from majority of acceptors it tells everyone about the chosen value.
`acceptors`
- can then tell all the `learners` about the chosen value.

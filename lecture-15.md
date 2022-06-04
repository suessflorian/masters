# Begins with discussions re PAXOS algo
Why versioning?
- fault-tolerance mechanism
- deadlock prevention mechanism (competing proposals, unable for proposer to receive majority)

If majority of the acceptors have logs of chosen value on disk, the value is chosen.
Why?
- The new proposer (higher version number)
- will receive from the `acceptors` responses `("ack", n, n', v)`, where `v` would have been the value written to disk.
- this value is written to disk by the majority of the group 
- and for a proposer to successfully move onto the second phase, it needs acknowledgments from the majority of the group. There will be at least one response of the value written to disk.

Another point to talk about is trading off efficiency for reliability, ie, reducing the number of acceptors.

### Proof of Safeness
As a value is `chosen` when a `majority` of the acceptors logs `v` sent by the proposer in phase 2, if `v` in proposal `(v,n)` is chosen, the value in all accept proposals `(v', n')` where `n'>n` must satisfy `v=v'`
- In the response to the `prepare request`, `at least one acceptor` informs the proposer of the value that the majority of the accepts have accepted. (by nature of _majority_)
- Proposer `uses accepted value` with the largest version number as its own proposed value in the accept request.

Let `(v, n)` be the earliest proposal that is accepted. If no other proposals are given, well.... safe this algo is.

Now assume other proposals are given. Assume `(v', n')` be the earliest accepted after `(v,n)`. As proposal needs a majority of the nodes to respond, at least one node must have responded to proposals for `(v,n)` AND `(v', n')`.
- this node must have suggested `v'` as `v`
- proposer must have accepted `v'` as it's `v`
hence `v'=v`

# [NEXT TOPIC] Consistency and CAP
Only two important theorems applicable to distributed systems, FLP theorem and CAP theorem.

_Motivation_
## Reasons for replication....
common technique, two reasons
- increased `reliability` (more points of failures)
- improves `performance` (more readers, or moving things closer to readers)

The key issue is the need to maintain `consistency` of replicated data.

We introduce
### Consistency Model
Defines semantics of a `read` operation of a data model. Set of possible values returned by the data store.

Two types of models here:
- strong consistency: clients of a data storage always see the `latest` value that was written for a data object
- eventual consistency: clients of data storage get value of the object at some `past` point in time. Replicated objects `converge` towards identical copies in the absence of updates.

## Enforcing strong consistency (Quorom algo)
Two weights given:
- write operation `ww`
- read operation `rw`
- each replication site has one `token` that carries some weight (normally 1).

In order to carry out a read/write operation a client needs to collect enough weight (i.e. tokens)
- a read operation can be carried out if the weight collected by the client is `>=` than `rw`
- a write operation can be carried out if the weight collected by the client is `>=` than `ww`

### `rw` and `ww` have to satisfy the following:
- `ww > ns/2`
	- ensure writes are exclusive
- `(rw + ww) > ns`
	- ensure read and writes exlcude each other
	- read operation will never read a value which is out-of-date

`ns` is the total number of tokens in the system, and each token carries weight 1

## Enforcing eventual consistency
Relies on two properties
- `total propogation`, updates reach ALL sites
- `consistent ordering`, updates are processed by ALL sites in consistent order

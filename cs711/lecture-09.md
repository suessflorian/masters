# Mutex (mutual exclusion)

Three different approaches:
- Timestamp-based
- Quorum-based
- Token-based

# Requirements/Garantues that comprises of MUTEX
1. **Safety**: At any one point, only `one` task can access the resource at a time
2. **Liveness**: Tasks should not endlessly wait, no `deadlock`
3. **Fairness**: each task gets a `fair chance` to access the shared resource, request _eventually_ gets satisfied.

## Timestamp-based
`Ricart et al` algo
- scheme is based on totally ordered logical clock
- each req for accessing the shared resource is given a timestamp
- req's ordered on allocated timestamps
- req with smallest timestamp access the shared resource first

### Prooving Correctness of Ricart Et Al

Safe, given any two processes with resource reqs (T1, P1) and (T2, P2).
Suppose (T1, P1) < (T2, P2)
=> P1 will **NOT** send an `OK` message to P2
=> Hence P2 will not access the resource at the same time as P1
=> P1 and P2 cannot access the shared resource at the same time

Liveness, assume the total ordering between resource reqs among processes P1, ..., Pn
=> Means there exists a smallest resource req timestamp
=> Resource req with the smallest timestamp will receive OK's from all other processes

Fairness,
=> Resource req timestamps by definition monotonically increase 
=> Resource req upon waiting long enough will have the chance to enter critical region 

#### Corollaries

- n requests out, for each of n, sends request back: complexity O(2(n-1)) => O(n), compared to central access manager which is O(2) => O(1).

- central access manager has 1 point of failure, Ricart Et Al has n point of failures (need to receive `OK` from all processes)

Objectively worse than central access manager in two key areas:
- Reliability
- Complexity

## Quorum-based
- each task requests permission to access the shared resource from a subset of tasks
- subset of tasks is called a `quorum`
- several quorums in the system
- each tasks belong to one to many quorums
- quorum must satisfy the following property
	- given two quorums q1, q2: q1 intersecting q2 != empty

`Maekawa`'s Algo
- several voting sets in the system
- each process is assigned to a voting set
- voting sets are chosen to overlap, process must collect replies from all members of it's voting set (similar to `Ricart Et Al`)
- member can only reply to one member of its voting set at a time, will not reply to another message until receiving some sort of `receive/relinquish` message.
- can change its vote if received request with an earlier timestamp, does this via an `inquire` message to process it last voted for.

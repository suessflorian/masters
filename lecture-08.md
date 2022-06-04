Recall `reliable multicast`, we either deliver a multicast to `all` or to `none`.

# Continuing on Reliable Multicasts
Since processes might crash, this is very non-trivial.
	- suppose a process delivers a message to one process, crashes and fails to deliver this message to another process.

We want all `non-faulty` proceses to receive the same set of multicasts, `faulty` processes will not participate in computation, not a concern.

## Naive Algo for achieving reliable multicast
Sender uses TCP (FIFO ordering)
- Every received message, would be emitted to all other processes except the sender.
Complexity: O(n^2)

# Introduction Virtual Synchrony Model (aimed to garantuee reliable multicast property)
**Maybe it's more a preliminary**

So note, this garantues that all _view changes_ are delivered in the **same order** (smells like total ordering?).

Also realise that a view change doesn't nessecarily only involve one process going in/out. Could be a group of processes joining/leaving. 

- managing group membership and group comms
- process my join or leave
- `view` certain point in time, membership of a multicast group.
- `view` `changes` when proceses join or leave.
- processes in a group should have the **same** `group view` when message is multicast.
	I think a better way to phrase the above; the set of multicasts delivered in a given view is the same for all none-faulty processes that were in that view.
- upon process leave a `view change message` is broadcasted to all processes
	- `processes` should change their view together

**virtual synchrony garantues that all `view changes` are delivered in the `same order` at all non-faulty processes**

### IMPLEMENTATION
Assumes:
- Reliable point-to-point communication (TCP).
- No process crash during view change
- There exists a leader inside handling view changes

Solution:
1. For all messages `m`, all processes in view `G`, `keeps m` until it knows that all members in `G` have received `m`. 
2. If `m` is received by all	members of `G`, `m` is considered `stable`
3. Only stable messages can be let go.

The view change itself is handled by a view's leader. Periodically health checks all members in `G`, once failure is detected. It multicasts a `view change`

So when a process say `P` receives a view change message, it multicasts all it's stable messages followed by a `flush message`. After `P` has received a flush message from all other process in view `G`, it then "installs" the new `view`.

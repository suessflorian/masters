# Continuing Total Ordering
We already know how this works though... so algo in previous lecture notes.

## Why can we garantuee that the first message in the holding queue, that has a timestamp allocated by the emitter, is safe to deliver?
- for every non-received message that has yet to arrive in the queue, will have a timestamp strictly larger than any timestamp validated message
- for every unvalidated message in the queue, the final timestamp allocated will be at least as big as it's provisional one

# Implementing Causal Ordering
Assumes FIFO between any two processes

Inside a process group, 
- every process keeps a variable for each process (including itself) tracking messages received.
- as a messages are emitted, the emitter stamps the message it's send with it's current variables (including itself incremented by one)
- receivers will compare message timestamps with it's own variables. If the message is a _perfect successor_, it receives the message and increments the variable required accordingly
- similar to enforcing partial ordering, passing around the dependancy tree

Keep in mind that multicast messages send messages to the receivers of all processes in a process group. INCLUDING the receiver of the emitter itself!

# Reliable Multicast
**Means that every process in the process group receives all multicasts.**
Orthogonal to ordering (reliable-fifo, reliable-causal, reliable-total)

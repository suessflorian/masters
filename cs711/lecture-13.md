# Snapshot
Used for system failure recovery, or perhaps system debugging.

## Consistent global state conditions
1. if the sending of a message is recorded in the state of the sender, the receiving of the message must be recorded in the state of the receiver.
2. messages that have not been recorded by senders should not be recorded by receivers.

### Issues in recording a global state
How do we ensure:
1. any message sent by a process `before recording` its snapshot, must be recorded in the global snapshot.
2. any message sent by a process `after recording` its snapshot, must not be recorded in the global snapshot.

Additionally:
3. How to actually determine the instant when a process takes a snapshot?
- As we need to have a process record its snapshot `before` processing a message that was sent by another process which recorded its snapshot `before` it sent that message.

# Algorithm (Chandy-Lampart) for FIFO channels (eg: TCP)
- Uses a control message called `marker` to separate messages in channels.
- `After` a site has recorded its `snapshot`, it sends a `marker`, along all of its outgoing channels before sending out any more messages.
- A marker `separates` the messages in the channel from the messages to be included in a message and those that are not.
- a process must `record` its snapshot no later than when it receives a marker on any of its incoming channels.

### Implementation
**Initiator**
Records local state, starts recording incoming channels
Sends marker signal to all out going channels

**Unsuspecting Process**
1. If not seen marker before:
- records local state, starts recording all incoming channels
- marks the channel that the marker signal came in as *empty*
2. If marker seen already
- stops recording on inbound channel that received the marker channel

**Termination**
When all processes have received marker signals from all neighbouring processes, ie, has finished recording on all incoming channels.

[using external resource to learn more about Chandy-Lampart](https://www.youtube.com/watch?v=x1BCZ351dJk)

## Correctness proof (hard to understand)
1. FIFO assumption, for all channels any message sent after a marker (snapshot) 
=> it is not recorded in the channel state.
=> (contraposition) If a message is recorded => message is sent before marker (snapshot)

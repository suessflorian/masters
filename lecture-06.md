# Multicast
Continuing on...

## Ordering Property
- FIFO, for all messages, m and m' given a emitter, if m is sent before m' from the emitter, then for all processes in the group m -> m' re: delivery
- Casual ordering, given messages m, m' such that m causally relates to m', then for all processes, messages are deliver m -> m'

Those two seem similar, if you're confused check out the [recording](https://auckland.au.panopto.com/Panopto/Pages/Viewer.aspx?id=65906407-d299-4679-b6d7-ae53017f4c1d) at around 9-10min. **There is a difference**

- Total ordering: if a process delivers message m before m', then all other processes will deliver m before m'.


Enforcing FIFO can we done via TCP 😲
```
- process assigns sequence number to message that it broadcasts
- each process maintains some variables to track sent/received for each other process
- let S be the sequence number assigned to broadcasts
- let Rq be the number of the last message that is broad cast by process q
- when broadcast, assign S to it, S := S + 1
- when receives:
	if sequence number of message is Rq+1, deliver
	else place in a waiting queue
```

Enforcing Total Ordering
Makes use of logical total ordering strategy.

```
- Each receiver hosts a holding queue and a delivery queue
- When messages are received, they are immediately placed on the holding queue and stamped
- This timestamp is sent back to the emitter 
- The emitter will wait, until all processes in the process group returns a timestamp
- Once all the processes return with their proposed timestamps
- The emiiter finds the maximum timestamp and emits those back to the processes
- The receivers then re-sort the holding queue
  if the confirmed event is at the top of the queue then deliver the message

# Problems with our Total Ordering approach?
For some apps, giving an order between event is netiher nessecary nor desirable.
- hides casual relationships
- debugging a distributed program (considering events when not needed to)
Opting for a partial ordering helps surface causal relationships

# Partially Ordered CLock
Example starts at [17.40s](https://auckland.au.panopto.com/Panopto/Pages/Viewer.aspx?id=dddd033a-15c1-4d48-9f78-ae510184bbf3)

One-way communication

So for every process, associate a letter. Say `a`.

As events occur inside of process `a`, associate an event number.

`(a, 1)`, `(a, 2)` and so on...

As the process continues we build a set of dependancies {(a, 2)}, where each tuple represents the last known step of a dependant process (including itself).

Suppose this process `a` receives a message from some process `b` with it's own set of dependancies {(b, 12), (z, 4), ...}. First, this is an event in `a`, hence amend the dependency set to show another event in `a`.

Then take the union of `a` and `b`'s dependency set. This now annotates the dependency set of `a`.

# Totally vs. Partially 
- Partially ordered clock is more expensive
	- so much so that it's impractical for long living computations
	- no upper bound for timestamps
	- the number of item set is limited by the number of processes created at run time

## Next TOPIC for next lecture is MultiCast
Process group, many processes, any of which can belong to multiple other process groups at the same time.

**Multicast Op** sends message to all members of a process group.

# Deliver a message in a distributed system
Middleware involved (structuring consistent multicasting both sender and receiver). Required to garantuee certain properties related to delivery (like ordering?).

# Logical Time
In distributed systems, consists many machines, machines by default are not garantueed to have a synchronized clock (eg. different timezones, moreover physical limitations of having perfectly synchronized clocks...).

We don't need synchronized clocks most of the times, but "event" ordering is very important.

_Pretty average example given to motivate such a problem._

### ENTER LOGICAL TIMESTAMP
Not nessecarily a timestamp. Basically given events, a & b. If a _occurs_ before b, then a -> b is true.

If a is the event of a message being sent, b is the even to of the message being received, a -> b is true. (-> happens before.)

`->` is transitive

Now to find some function `c` (clock), such that for all events a,b such that a -> b, then c(a) < c(b).

### LOGICAL CLOCK ALGO
```
loopforever
	if an event occurs in the process
		assign the value of clock to the event;
		clock := clock + 1
	endif
	if a message m is received
	then clock := max(time(m), clock) + 1;
		assign the value of the clock to the receiving message event
		clock := clock + 1
	endif
endloop
```

Difference between `event` and `message`?

Seems like a message refers to messages being sent between system boundaries, and events describe the events that happen within system boundaries.

For some reason, no one could comprehend this?

# Total Order
So with the above we can still have contesting events with respect to allocated logical times. We want to order them. We do this by introducing a tie breaker, being a process identifier.

Assume `a` and `b` are timestamps of events `(Ta, Ida)` and `(Tb, Idb)`.

If a -> b then Ta < Tb **OR (Ta = Tb && Ida < Idb)**

__Causal relationship__

This is an artifical mechanism to enforce total ordering.

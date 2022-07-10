# CAP Theorem
Reminded that `FLP` and `CAP` theorem are the most important theorems in distributed systems. We continue with what we covered in lecture 15.

We finally converge to the topic

### CAP Theorem
– `consistency` (C) equivalent to having a single up-to-date copy of the data.
– `high availability` (A) of that data (for updates).
– tolerance to network `partitions` (P).

Some key notes (not sure if I'd consider them hot takes or not):
- The NoSQL movement is about creating choices that focus on availability first and consistency second.
- NoSQL systems use BASE (basically available, soft state, eventually consistent).

## Basically Available
Providing system availability in the case of partial system failure... Ofcourse the node that fails will refuse operations. But the system as a whole should be able to continue.

## Soft State
State returned by system is not necessarily the representative indented state of the system.

## Eventually Consistent
Builds on `soft state`, updates will be propagated to every site eventually. State of the system converges.

# B-A-S-E
Implementing BASE typically involves a messaging queue. Leveraging properties:
- `total propogation`, updates reach ALL sites
- `consistent ordering`, updates are processed by ALL sites in consistent order

Illustration:
```
Begin transaction
   Insert into transaction(id, seller_id, buyer_id, amount);
   Queue message “update user(“seller”, seller_id, amount)”;
   Queue message “update user(“buyer”, buyer_id, amount)”;
End transaction
```

Note:
`partially ordered timestamps` and event logging should be used for the events in a BASE conforming system. This helps when identifying and resolving conflicting and inconsistent updates.

---

Now we jump to another topic:

# Mutual inconsistency (Parker’s Algorithm)
VECTOR CLOCKS coming in for the rescue. Essentially every process hosts a vector clock. So suppose a network partitioning happens and updates occur to one process but not the other. Where each point-wise unit of the vector represents _particular state_...

If these processes combine again, in the event of network "union" I suppose... If the vector clocks of these processes are strictly comparable, ie for any two, `a`, `b`. If `a` >= `b` OR `b` >= `a`... then we may merge state in a consistent manner, **ELSE** we resort to some sort of consistency resolution path.

### LIMITATION??!
It is assumed that state captured in these point-wise units of a vector are causally independent. VERY IMPORTANT!

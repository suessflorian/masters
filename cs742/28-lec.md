(18th Oct)

# Active Queue Management (AQM)
Umbrella term for techniques that go beyond FIFO's

Includes
- RED (random early detection / random early drop)
- Differentiated queueing (DiffServ) - queue packets based on urgency
- Lots of other schemes

## RED - Random Early Detection / Random Early Drop
Basic idea "As queue fills up, increase probability of dropping a new incoming packet". Buffer operates as FIFO (BFIFO or PFIFO) in principle:
- Drops packets before the buffer fills completely
- An arriving is dropped with a certain probability
    - Below a minimum queue length threshold, all packets are accepted.
    - Above that threshold, packets are dropped with a probability that increases to 1 as the queue size hits maximum queue capacity.

**Objective of RED: Get TCP senders to back off before the queue workflows**

### Under the spotlight
Objective of RED: GET TCP senders to back off _before_ the queue workflows.

- How do the senders know about the drops?
    - TCP senders expects ACK for the packet from other end of the connection.
    - If ACK times out (i.e., no ACK after RTT + some timeout), packet is presumed lost.
    - A single packet loss usually only triggers a fast retransmit, not a backoff.

- Effect of backoff(s) on arrival rate at router FIFO must make a difference before the queue is full.
    - That requires RTT < time it takes to fill the queue.
        - If the RTT is longer than the time it takes for the queue to fill up, the feedback (in the form of packet drops) that RED provides to the TCP senders will be too late. The senders will only realize that they need to slow down after the queue is already full, and packets have been dropped. This scenario defeats the purpose of RED, which is to signal congestion early enough for senders to slow down and avoid overwhelming the network.

    - Harder to achieve for large RTTs (most routers see a mix of RTTs)
    - Incentivises larger buffers (buffer bloat)

Can adapt RED so it weights the drop probabilities by packet type (protocol, type of service / differentiated services code point) - this is known as WRED.

Active RED (ARED) adapts the threshold from where the router starts dropping based on observed average queue length.

## Effect of FIFO buffers in the network
Increases in bandwidth-delay product (BDP)
- BDP is the "amount" of data that can be "in flight" in a connection
Entices TCP to increase its congestion window
- Also: after tail drops, TCP senders don't back off as much before there is capacity again.
- So, having plenty of FIFO capacity should be a good thing, right?
    - Increased latency, bigger queue, but the queue doesn't go faster.
- TCP attempts to match the congestion window to the BDP
- If BDP grows, TCP grows the congestion window
    - This will attempt to fill the extra memory
- If we deploy more buffer memory, we increase the BDP by increasing the delay - more buffer memory means longer queue sojourn times.
    - Queue sojourn time is the time a packet spends in the queue
    - Longer queue sojourn times mean larger RTTs
        - Larger RTTs mean slower growth in congestion window

## Net effect of adding buffer memory
- Buffers contain sending queues that contribute to RTT
- Standing queues != shock absorbers
- Longer RTT:
    - TCP congestion windows take longer to (re-)open
- Without differentiated queueing: time-critical packets get stuck in the queues behind less time-critical stuff.

### What buffer sizes are then appropriate?
Classical approach: buffer size = BDP of bare onward link
    - BDP of bare onward link is easy to determine
    - Still in wide use

Guido Appenzeller (2004): BDP is too large, use BDP/sqrt(N) instead
    - N is the number of long-lived TCP flows (> 1 RTT)

Jim Gettys and Kathleen Nichols (2011): Bufferbloat
    - Not a reccomendation at that point, just an observation: curretn buffers are too large!
    - Subsequently: development of `codel`, `fq_codel`, and `cake`

## Queue Sojourn Times
If the outgoing link is not shared with other transmissions (i.e., not WiFi):
- Queue sojourn time = queue size in bits / link bit rate
- Maximum queue sojourn time limited by buffer size

If the outgoing link is shared (i.e., WiFi)
- Queue sojourn time = unpredictable
- Maximum queue sojourn time = infinite (if link is continuously busy ofc)

# CoDel
Actively managing the queues themselves! **Co**ntrolled **Del**ay queueing discipline, "if a packet in the queue has been in the queue for a certain amount of time already, drop it".
- Pronounced "coddle"

Based on PFIFO, but:
- Limits the queue sojourn time by dropping packets, regardless of outgoing link state.
- Targets a small residual sojourn time.
- Allows short bursts of arriving packets to queue for longer than target time.
- Fair queueing version `fq_codel` is now the standard queueing discipline in Linux.

# Explicit Congestion Notification (ECN)
"Communicate congestion directly to senders", type of service header.

- Uses the last two bits of the TOS / traffic class field in the IPv4 or IPv6 header.
- Requires both IP hosts to have ECN enabled, as well as an ECN-enabled router.
- ECN capable endpoint host sets ONE of the two bits to 1.
- Any router that does not see congestion does not change the bits.
- A router experiencing congestion that sees a non-zero ECN bit sets the other bit to 1 as well.
- Receiving endpoint passes this information to the transport layer.

## ECN and TCP
If the transport layer is TCP:
- Host receiving ECN bits set to 11 sets ECN-Echo (ECE) flag in extended TCP flags field to 1 in its next TCP packet back to the sender.
- Sending host receiving ECE flag to set to 1 reduces `cwnd`, sets `CWR` flag in next TCP packet to receiving host.
- ECE and CWR flag are located before the conventional TCP flags in the header.

### Common Threads
- AQM and ECN all rely on TCP congestion control to do its job by denying the sender ACKs.
- Communication path from routr to TCP sender is via the other TCP endpoint.
    - This is not normally the shortest path from router to sender!
- Effect of any intervention is not seen at router for > 1 RTT
- Large RTT lets the TCP sender respond to a badly outdated congestion picture at the router.


# RTT distributions
E.g., router in data centre handling traffic between servers in the data centre only.
- BDP dominated by bandwidth, not latency. Short RTTs, all RTTs in the same order of magnitude.

E.g., router at a major internet exchange, handling traffic between a highly diverse set of endpoints locally and internationally
- BDP depends on characteristics of outgoing link
- RTT distribution possibly between sub-ms and several 100ms

E.g., router at GEO satellite modem on a link to a small island ISP
- BDP dominated by latency, not bandwidth
- Long RTTs starting upwards of 500ms

## Impact of RTT distributions
If the RTT distribution is more or less homogenous, all TCP senders respond to drops (tail, RED, or otherwise) within the same time frame.
- Drops happen for all flows more or less at the same time
- All long flows back off simultaneously
- Global synchronisation (TCP queue oscillation)

If the RTT distribution is heterogeneous, TCP senders respond at different times.
- Some back off immediately, some keep going for a while
- Some recover more quickly from back-off than others
- This helps in congestion control

(12th Oct)

Finishing up submarine cables, mainly focusing on recap of TCP.
# Continuing with Submarine cables, politics
One of the problems you have is "people don't necessarily trust their neighbours". Lot of countries do interestingly trust Singapore, hence the major hub established there. Land locked countries don't really want to feed cables through other countries land etc... the usual.

## Can we trust cables?
Much of the traffic between NZ/Australia and Asia goes via the USA.
    - Just because it's cheaper? Eavesdropping etc...

How secure are cables sabotage?

# TCP Recap
TCP: transmission control protocol
- transport layer
- connection-oriented
- reliable byte stream
- bi-directional (Alice can send to Bob while Bob sends to Alice)

What TCP isn't:
- A protocol capable of delivering data on time
- The same thing to all people (many flavours exist)

## Packet Structure
- Every TCP packet contains:
    - A header
        - Port numbers of the sending and receiving socket (application)
        - Sequence number (SEQ, of first byte in the packet, in relation to byte stream and initial sequence number (ISN))
        - Acknowledgement number (ACK number, sequence number of next packet needed from the other side at the time packet is sent)
        - Flags: SYN, ACK, FIN, RST, plus two ECN-related flags are the only ones really in use. Flags are 1 if set, 0 if unset.
        - Advertised window: Available receive buffer space in bytes at the host sending the packet signals to other side how much data we can accept right now.
        - Options: TCP options (in many cases, this includes an extended version of the advertised window)
    - Possible: payload data (the data the sequence number relates to)

## Connection Setup
"Three way handshake"

- Initiator/client sends a packet to server:
    - Random initial value `C` in SEQ field, SYN flag set indicates that SEQ is an ISN
    - ACK field typically zeroed out, ACK flag 0, no payload data
- Server response with a packet to client:
    - Random initial value `S` in SEQ field, SYN flag set indicates that SEQ is an ISN
    - ACK field set to `C+1`, ACK flag 1, no payload data
- Client completes handshake with a packet to Server
    - `C+1` in SEQ field, SYN flag 0
    - ACK field set to `S+1`, Ack flag 1, no payload data

_Random ISN btw to protect against predictability exploiting attacks_ 

## Sending data, mid-stream
- client sends to server a packet with:
    - `C + 1 + #bytes` to SEQ, SYN flag 0
    - ACK field set to the next sequence number from server that client needs to see to continue the byte stream received from server. ACK flag is set to 1.
    - Advertised window field set to number of available bytes in client receive buffer that can be filled with data from server.

- Server does the same, analogously, when server has data to send.

## Receiving data, mid-stream
- Client receives a data packet from server with sequence number `H + 1 + #bytes` containing `n` bytes of payload data
    - Checks whether she has received all bytes up to and including `H + #bytes`
    - If YES, client sends a packet with:
        - `C + 1 + #bytes` in SEQ field (where ofcourse the #bytes differs here to that of the amount sent by the client previously), SYN set to 0.
        - An ACK field of `H + 1 + #bytes + n` and ACK set to 1
        - Payload ofcourse is optional
    - If No, client sends a packet with
        - `C + 1 + #bytes` like before in SEQ, SYN set zero
        - An ACK field with the next sequence number needed to continue the received byte stream
        - Payload is optional
    - These packets are also known as "ACK packets" or simply "ACKs"
- Server does the same, analogously, when server has received data from client.
        
## ACK timeouts and retransmissions
- TCP sender sends a data packet. Question is, how long should it wait for?

Timeout based on default / previously seen RTT + X. If ACK fails to arrive, data packet needs re-transmission: re-send just one lost packet or all packets since the lost one? 
- Queue overflows are often burst losses, losses due to bit errors affect single packets

If receiver sees a packet with sequence number larger than its current ACC number, it sends an ACK with its current ACK number: duplicate ACK.
    - Duplicate ACK received by sender: re-transmit only that packet
TCP options allow SACK: selective ACK of multiple data packets with gaps.

## Sender transmit Window
TCP sender and receiver are some latency part:
- ACK arrive after 1 RTT
- But: RTT can vary as queues along the IP forwarding path grow and shrink
How much data should a TCP sender send before waiting for an ACK? Each TCP sender maintains a transmit window or sending window. This is the minimum of:
- Amount of data available to send
- Other side's advertised window (plus estimated clearance rate at far end)
- Sender's TCP congestion window

Congestion window (cwnd): Maximum number of bytes (or, more commonly, data packets) allowed to be sent without having received an ACK covering them.
- Maintained by each TCP sender
- Core part of TCP congestion control

Basic rule:
- TCP senders grow their cwnd with each ACK received.
- TCP senders shrink their cwnd on ACK timeout / multiple packet loss.

## TCP congestion control
If TCP senders collectively or individually send more data that can fit through a bottleneck link, the router at the entrance to the link will drop excess packets.

- Simplest case: FIFO queue at bottleneck entrance, tail drops
    - More complicated cases: Later!
- Dropped data packets don't result in ACKs
    - Senders time out, retransmit & reduce their `cwnd`.
    - Amount of data heading to link decreases.

**GOAL**; make `cwnd` match the available RTT bandwidth delay product.
- BDP is the amount of data that "fits" into the link between sender and receiver.
- Problem: don't know the current available BDP & it changes all the time!

Have to start somewhere: initial size of `cwnd` is typically 10 these days
- This is quite small by today's standards. Example: RTT BDP of 150km 1000Mb/s link is 2 x 1ms x 1000Mb/s = 1M bits = 125,000B: over 83 full size 1500B packets.

## Increasing `cwnd`
### Slow Start
Increase `cwnd` by 1 for each ACK received
    - This implies `cwnd` doubling once per RTT (plust transmission time of cwnd packets)
    - Not actually a "slow" start - it's exponential growth! 10 packets at start, 20 after 1 RTT, 40 after 2 RTT, 80 after 3 RTT (if all goes well)
    - Do this only up to a limit known as `ssthresh` (slow start threshold) or until loss occurs.
        - Then switch congestion avoidance
        - Initial `sshthres`: E.g., half the bandwidth of the connection.

### AIMD (additive increase / multiplicative decrease)
For congestion avoidance after `ssthresh` has been reached, increase `cwnd` by 1 for each lossless RTT: linear growth.
- Too slow in hitting BDP on high BDP links!
- Exponential backoff after loss (multiply `cwnd` by a factor such as 0.7 or 0.5 after each loss, hence multiplicative decrease):
    - Re-enter slow start after losses with new `ssthresh` at a fraction of the size of the last `cwnd`)

# TCP Flavours
- Slow start and AIMD aren't identical
    - Slow growth in AIMD - inefficient on high BDP links
    - Excessive backoff after sporadic losses not related to congestion
- Various TCP flavours exist that tinker with performance in specific scenarios
    - E.G., adjust ACK timeout / `cwnd` based on previous RTT seen
        - Respond to growing queues
    - Lossy (noisy links)
    - Different TCP flavours are usually interoperable: client can run a different flavour than server.

## Famous TCP Flavours
- Reno / NewReno: the classic. No going back to slow start (fast recovery).
- Hybla: optimised for high latency links (satellite)
- BIC: optimised for long latency + high bandwidth networks (LFNs)
    - Uses a binary search to find "optimal" `cwnd` size, limiting in an additive increase.
- CUBIC: similar to BIC in aim to functioning, less aggressive
    - Default in current Linux versions
- Compound TCP: maintains two `cwnd` for good performance on LFN's and fairness to other TCP
    - Used in Windows.


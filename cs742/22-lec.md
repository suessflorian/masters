(4th Oct)

# Continuing Queue Oscillation in Satellite Communication

Queue oscillation in satellite communication is a critical issue that involves the fluctuation of packet numbers in a transmission queue. This oscillation can cause inefficiency and packet loss due to the unique challenges posed by satellite communication, such as high latency and the high bandwidth-delay product. Requires three factors; bottleneck, latency, multiple transmissions.

## High Latency

Satellite communication involves significant transmission distances, which naturally induce delays. A geostationary satellite link can easily experience round-trip delays exceeding half a second.

## Bandwidth-Delay Product

The bandwidth-delay product for satellite links indicates that there is a substantial amount of data 'in flight' at any moment. Improper queue management can lead to inefficient cycling between full and empty queues.

## TCP Congestion Control Challenges

Traditional TCP congestion control algorithms are not well-suited for the high-latency environment of satellite links. They can cause a 'global synchronization of queues', where all senders reduce their window size simultaneously due to packet loss, leading to queue size oscillation.

## Oscillations

The result is a cyclical pattern where queues become full, causing packet drops, and then become empty, leading to underutilization of the link.

## Variable Bandwidth

Changes in bandwidth due to external factors, such as weather conditions, can further complicate queue management and exacerbate oscillations.

# Effect of Queue Oscillation on TCP flows
Most flows are really short.

- Ping: short flows
- Loading web sites: short flows (most elements are small)
- So: users can surf and get their mail
- If something appears slow: users blame server
- User's don't complain to SIP

Short flows don't experience queue oscillation: user experience dominated by RTT delay, not rate.

# Practical effect of queue oscillation
- Mail headers and email messages load quickly - but large attachments don't
- Web browsing pages with only text or small elements is fast - but download of software and larger documents (e.g., PDFs, movies) isn't
- Note: streaming movies works reasonably well - why?

## Common misconception
"The download time depends mainly on the link data rate"
- This is true for large downloads only!
- Example: 160ms RTT, 300Mbsps MEO sat link, assume no server delay
    - 5kB download averaging a rate of 4Mbps takes 170ms - 94% RTT
        - This is what users experience in web browsing
        - Half the data rate takes this up to 180ms only
    - 10MB download averaging a rate of 4Mbps takes 20.16s - 0.8% RTT
        - If we only achieve half the data rate here, we need to wait over 40 seconds!

TCP slow start should let larger flows make better use of the capacity 
- But: this isn't happening here: shorter flows between 4 - 32kB in size achieve peak data rates around 70% faster than flows of 1MB and more.

## Three types of bent pipe scenarios
1. Low load scenario
    - Low user demand - queue drainage / underutilisation due to lack of demand
    - Link buffer seldom fills up
    - No queue oscillation
    - Large flow congestion window opening constrainted by RTT only - but we have few large flows anyway
2. High Load
    - Medium-high user demand
    - Link buffer fills and drains in quick succession (within seconds): Excessive queue oscillation.
    - Large flows constrained by excessive backoff. TCP can't get congestion window right.
3. Overload
    - High user demand
    - Small flows (<10 packets, i.e., < `init_cwnd`) take over
    - Link buffer permanently full - most small flows don't back off.
    - Large flows time out.

## Engineer vs. Computer Scientists
Your satellite link features link underutilisation and high packet loss. Users complain of "slow internet". What could be the cause?
- Engineer's answer: "Low SNR or interference at the receiver. Check antenna, antenna alignment to satellite, feed line, receiver, weather"
- Computer scientist's answer: "Could be TCP queue oscillation" 

In response to this diurnal pattern of;
- High packet loss / low goodput during day / evening
- Low / no packet loss / high goodput during night

# Routing in LEO network
- LEOs are not normally in range of an Internet gateway ground station
- Will need routing between satellites
- Routing needs to be dynamic (satellites move)
- Part of the Earth may not see coverage by any orbit.
     - Coverage depends on inclination

## Challenges
- LEOs move, rise and set with respect to ground stations.
- Ground stations do not remain under the same orbit.
- LEOs in one orbit can follow each other in a fixed "necklace"-like sequence.
- LEOs in different orbits move towards and away from each other and can lose sigh of each other.
- Routing is a cost in a satellite's power budget.

## Opportunities
- Orbital movements is highly predictable
- Each LEO satellite can compute who & where its neighbours are.
- Each LEO satellite knows which ground stations it can reach directly (and may know where they are).
- Ground stations knowing its time and positions knows where the satellites are.

## Possible Approaches
- Ground stations compute required VC route to gateway in advance, route gets communicated with each packet.
- Ground station sends to satellite overhead, satellite and onward hops take care of route determination / maintenance.
- Other approaches

## Inter-satellite links
#### Intra-plane/intra-orbit:
- Links between satellites in the same orbital plane (and usually same orbit).
- Satellites "follow" each other in the orbit.
- Relative position between satellites is always the same (link never changes).
- But: Earth rotates under orbital plane, most point pairs on Earth are never found in the same orbital plane.

#### Cross-plane:
- Links between satellites in different orbital planes.
- Satellites may "fly alongside" each other for a short while.
- Relative position between satellites changes and they may lose sight of each other.


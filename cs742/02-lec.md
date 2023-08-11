# First Lecture

## Internet Traffic Measurement
Why measure the internet, predominate interest stems; commercial, social, technical. Intuitive reasons respectively.

Related to performing;
1. Network Monitor Placement
2. Measurement Analysis Tools
3. Measurement Result Reporting
4. Probing Mechanism
5. Vantage Points

### Edge Vs Core
To bring into view that measurements can happen at different levels (service quality/speeds etc...).

Simplified image of the internet, residence <-> modem parallel to business <-> edge router. Both parallel connecting to access networks. In term to Tier-2 and Tier-1 ISP. To switches, which hit data centers/web servers.

**Edge is on the left** and in the middle (ISP area) is **referred to as the core**. (Access, fibre optic, coaxial, copper, wireless based access networks). Edge routers (aka Modem/Edge Router). Tier 2; regional, Tier 1; globally, (Tier 3; local routers).

Basic narrative is that measurements can be easily obtained at the edge, ie, imagine your closest edge router. However measurements will be presented as demographically skewed (eg university network). Core ideal better representation of holistic network activity, proprietary/corporate/competition/privacy driven restrictions.

### Online vs Offline
Realtime: using high speed network cards that capture/trace network traffic etc... vs Offline: using any programming language for network characterisation, allows for anonymisation.

### Passive vs Active
- Passive meaning large amounts of data, capturing/sampling all the traffic. Tap into an edge router and capture packets.
- Active means intercepting and physically modifying network packets as they proxy through from source to destination.

### Single vs Multiple Vantage Points
- Multiple better representation, ofcourse harder (resources, time).
- Single, less so obviously.


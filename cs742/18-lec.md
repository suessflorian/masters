(22nd Sept)
New topic now, we move away from generic microwave communications.

# Mobile Networks - Node location
On original internet, mapping between MAC address, physical location an IP address usually remained constant.

- In a mobile network, the physical structure of the network undergoes constant change - a node may be in several locations on the network during one session (phone call, TCP connection...)
- BUT: IP leaves physical paths determination/adaptation/routing to lower-level protocols
- Most mobile services (802.11, Bluetooth, IP/PPP/GSM, 3G, 4G, 5G, ...) use their own generic protocols to establish virtual circuits (VCs) to a mobile node or between mobile nodes.
- **IP sees a virtual circuit between a gateway and a destination node as a single and continuous link (usually using PPP).**
- Need for protocol stacking (OSI model).
- Look at TCP/IP as an example. To use IP to ring a mobile phone, IP address or phone number must stay the same even if the mobile node using it moves throughout the network.
- Also, IP numbers belong to a particular subnet. We cannot move nodes between subnets.
- So we need way to send an IP packet straight from the destination node's subnet gateway (fixed location) to a mobile node without IP-based routing in between.
- Need a mechanism/protocol at a layer below IP to deliver the IP packet.
- In a mobile network with access points (base stations), we can associate a mobile node with a particular access point on the fixed part of the network.
- Can use an IP tunneling protocol or similar (such as PPP/IP or PPP/ATM) to deliver the datagram to the access point, which can then pass it to the mobile node.
- Keep a central (in mobile networks) register of mobile-node-to-access-point mappings.

# Stack Perspective
- TCP Layer
- IP Layer
- Virtual Circuit Layer & Data Link Layer (e.g., using PPP)
    - Mobile Node END
        - Data link layer (e.g., PPP)
        - Physical layer (radio)
    - Access Point to IP Gateway
        - Tunneling Layer (TCP/IP encapsulation)
        - Data link layer (e.g., Ethernet)
        - Physical Layer (e.g., Cable)
_Pulls anecdote around configuring APM in Japan re: his SIM card_.

## Mobile Networks - Virtual Circuit Layer
- Presume that access points (base stations) are part of a fixed network, e.g., IP-based, so can be routed to.
- I.e., virtual circuits to access points can be established from any access point on the fixed network to the mobile node (tunneling layer).
- Keep some kind of register of which mobile node is associated with which access point.
- When a VC to a mobile node needs to be setup up, find associated access point and get it to set up a VC to a mobile node itself (which should be in direct radio range)
- When association changes, VC's follow to new access point.
    - Need a protocol to do this between access points
- Run, e.g., PPP over the VC, so it looks as if there was just a single link between the mobile node and the IP gateway.

### PPP
PPP is defined in RFC 1172/1331/1332/1661 (is this the latest?). Looks like a wire communication, at least this is the basic perspective from IP.

- Assumes we have a dedicated bi-directional full-duplex data link that is capable of transporting data between two peers (e.g., two telephone modems connected to each other, but a TCP/IP connection also qualifies!). Can assume no problem with collisions (i.e., we can transmit data over the connection at any time without no need for medium reservation etc.)
- Can assume packets will always arrive in the order they are sent (FIFO)
- Then we can encapsulate higher-level protocol packets in PPP packets for transfer across this link.
- Can negotiate PPP link parameters for optimum bandwidth utilization (link does not have to be error-free).
- Point-to-point acknowledgement of frames (HDLC), i.e., we can be pretty sure that higher level protocol packets (e.g., IP) actually get to the other end of the PPP link.
- Used as a underlying protocol on many point-to-point links (esp. dial-up connections).

### Case Study: IEEE 802.11-family (better known as your classic WiFi)
- Initially intended to network offices as wireless LAM - replace Ethernet throughout an office floor or a building
- Now also used to operate wireless metropolitan area networks (MAN)
- Designed for stationary (or slowly moving) nodes that may not operate continuously
- Works in 2.4GHz (13cm) and 5GHz frequency bands (~6cm) (which include ISM = industrial, scientific and medical bands, **Allowed to use these bandwidths without any permission!**) must tolerate interference from other stations and applications such as microwave ovens. There is also an infrared version included in the 802.11 standard and some versions use unused TV spectrum. 
- Power output of transmitters typically up to 100mW (20dBm), power controlled (what do we mean by power controlled, analogy provided loudness transmission depends on distance to receiver)
- About 20 different versions of modulation, some use FHSS, DSSS, OFDM, MIMO, MU-MIMO, cognitive radio, some use.
- May be used as ad-hoc peer-to-peer OR as base-station (access point) based network
- Access point-based networks assume existence of a distribution network (backbone) for the LAN/MAN

## Keeping track of a mobile node: Example 802.11 W-Lan
Mobile node, provides a probe to proximal access points, access point(s) respond, mobile node chooses "closest", sends association request, the access point then yields a association response.

"Distribution System" (typically Ethernet) sitting above the APs receives the association info. Eventually informed of a dissociation and subsequent re-association.

### Tracking issues
- When using IP over 802.11, all mobile nodes in the network usually retain their IP addresses (usually obtained via DHCP), no matter which access point they are associated with
- "Constant IP address" within the wireless network implies that all nodes & access points must be within the same (virtual) IP subnet
- So: 802.11 WiFi isn't _really_ mobile

## Technology Evolution
- Late 80s: Analog (mobile, installed car)
- Early 1990's: Digital 2G (GSM)
- Late 1990's: 2.5G (EDGE etc.)
- Early 2000's: 3G (UMTS etc.)
- 2007-2010: 4G networks based on long term evolution (LTE) began to emerge
- 5G from around 2013, still not universal in 2023
- 6G at current is an active research area. 

"Pretty sure there isn't a single person on a planet that has a fully read the 3G+ standards" as motivation re: 6G being far away.

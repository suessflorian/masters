# HTTP Latencies

We go through the very basic, "how does HTTP work"...

- Transmission Times
- Propogation Times
- RTT (Round Trip Time)
- Handshake (TCP, sync, sync + ACK)

Typical excercise, given a network bandwidth, file size, RTT value. Should be able to derive the total time for target to receive resource from some source.

`file size / bandwidth + 2 RTT`

## Keep Alive
How we avoid handshaking per resource needed to be collected.

## Parallel Connections
Assuming synchronous file transfers. We investigate parallel connections and how their not really that effective. Each parallel connection needs to handshake. Connections can congest each other re: resource transfers.

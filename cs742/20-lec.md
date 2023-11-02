(28th Sept)

Continuing on with the 2G stuff... basically we were chatting about how to get out of the trap of low data rates, one of the resources is frequencies/bandwidth, an expensive resource to get.

# Spectrum Access
- Two fundamental problems to solve:
  - Duplex: how to ensure a user can listen and talk at the same time. Remember that recievers do not like transmitters nearby, and in a cellphone this is hard to avoid!
  - Multiple access: how to serve multiple users in one piece of spectrum.

## Duplex
Two fundamental approach:
- TDD: time division duplex. Handset transmits then switches back to receive every few milliseconds. Drawback: small delay in communication (not noticeable in voice). Advantage: uses one frequency, so transmitter and receiver can share antenna and some circuitry.
- FDD: Frequency division duplex. Handset transmits and receives continously, but on two different frequencies. Advantage: no delay. Disadvantage: need two frequencies sufficiently far apart so transmitter and receivers don't interfere. Potentially inefficient use of our limited resource.

_No clear winner. You'd typically find us using a hybrid of the above._

## Multiple Access
Several approaches:
- FDMA (frequency division multiple access) - each handset is assigned a different frequency (pair in the case of FDD) for communication.
- TDMA (time division multiple access) - each handset is given a different time slot for communication, very much like burst slots in GSM.

These above should be very straight forward... but we apply orthogonality and come up with the following two approaches which bakes the fundamentals behind 2-3G and then the latter being what is used for 4G and LTE.

- CDMA (code division multiple access) - each handset transmits simultaneously in the same frequency band but is assigned a unique chip sequence (or frequency hopping sequence).
- OFDMA (orthogonal frequency division multiple access) - each handset is assigned a subset of carrier frequencies from a band and transmits simultaneously on all of them.

- Hybrid approaches of the above.

Ulrich brings up the importance of _power control_ when it comes to using CDMA and OFDMA as these rely on equal representation of signals in the receiving frontier.

## Making efficient use of a spectrum in a transmission
In data communications, we like to park the ambulance at the bottom of the cliff. We want to lean into the chance of transmission error and utilise error correcting codes.

- Conventional approach is to avoid symbol errors in a transmission. This usually involves staying well away from the channel capacity.
- Alternative: transmit at a high rate and accept that errors will occur - but compensate by robust error correction.
- Information theory provides us with a number of different error-corrected codes for this purpose. Hamming codes are an example (but in practice are too simple for this job).

### Spectrum re-use
- The only point at which the bandwidth in a mobile communication system needs to be "exclusive" is at the location of the respective receiver.
- The same frequency may be used to serve another handset elsewhere. 
- This is the principle behind cells, but it can be exploited further by techniques such as beamforming, MIMO, or the use of several base stations.

#### Beamforming (using wave overlap)
- If a base station knows the approximate location of a handset, within it's range, it can use beamforming.
- Beamforming invovles transmitting the base station signal with multiple antennas from a phase array
- This forms a wave interference pattern such that the signal is maximised elsewhere.
    - Maximum: phases of signals from antennas align at the receiver.
    - Elsewhere: phases of signals from antennas don't align at receiver and (ideally) cancel out.
- Beamforming can also work in the reverse - the receiver can shift the signals from its antennas a little in time with respect to each other and so zero in on the desired transmitter.

#### MIMO
Both transmitter and receiver use multiple antennas
- If the transmitted uses T antennas and the receiver uses R, this creates T * R paths between transmitter and receiver (and many more if multipath propagation in an urban environment is involved).
- Each of these paths can be utilized either for beam-forming, or even to have completely different data streams on each path.

#### Multiple base stations
In a cellular network, many handsets can communicate with more than one base station - especially if they are at the edge of a cell far way from the strongest base station.
- Some base stations that the handset can communicate with many have spare capacity.
- Can let handset communicate with several base stations at once, utilising the spare capacity and giving the handset a higher data rate.
- This also makes handovers less critical.

## Universality of protocol platform
- Past: technology defined for access to network only: 802.11, GSM
No universality: data goes via different paths than voice traffic (which may even pass through analog lines still in GSM)
- Future: divided protocol stacks at lower layers for access and non-access networks ("backbone") joined by a network layer called NAS ("non-access stratum"). Everything above NAS is IP based (all-ip network).
- This includes control functions that previously used to be handled at the level of the access network. Handsets are now also more universally called UE (user equipment).

# Current state of the art: 5G
Focus moves away from human end user to machine-to-machine communication (IoT)
- IPv6 for up to 50 billion connected devices

Higher data rates from approx 50Mbps to > 1Gbps

New technologies:
- New (licensed) frequency bands
- Convergence with WiFi in unlicensed bands
- Better use of spectrum through technologies such as beamforming (beam division mulitple access)
- Massive MIMO (up to 64 TX & RX antennas either side)
- Service provided via multiple base stations at a time
- Software radios
- Software defined networking (SDN)
- Terrestrial service via base stations but also aerial segment (drones) and LEO satellites.

# Why IoT via 5G?
IoT: sensors (temperature, pressure, light beam, cameras, ...) and actors (motors, relays, heaters, lights, valves, ...)

- Cabling a large number of sensors / actors is expensive
  - Risk of cabling damage
  - Risk of damage
  - Fault finding effort
  - Cable contains expensive metal
  - Distances between information source and sink have increased

Cabling doesn't usually take the most direct route
- Plus: latency in cable is 50% higher than on radio

Sensors/actors can collaborate in communication
- But: radio is subject to interference, cable less so.


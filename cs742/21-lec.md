(29th Sept)

General form discussion on satelites.

# Satellite Internet Application areas
Three

- Geostationary (36,000km from equator, same velocity as rotation of the earth)
    - "Bent pipe" internet to ISPs (AirNZ Wi-Fi!)
        - Meaning up and down again (rejuvenate receiving signal)
    - Direct-to-site
    - Direct-to-site downlink only
    - Long latency, physical 0.5s, buffering on either side another 0.5-1.5s

Can see half of the earth!

- Medium Earth Orbit (MEO, 8,000km above the equator, no longer stationary)
    - Currently only one provider: 03b mpower (SES) - "Bent pipe" Internet to ISPs

See's less of course because it's closer. Base dish needs adjusting throughout it's course. Needs extra satellites. Allows moving from C-band KU-band (closer) advantage. Physical 130-150ms, buffering gets smaller, total RTT 250-350ms.

(west to east?)

- Low Earth Orbit (LEO)
    - Direct-to-site
    - Direct-to-device
    - Since end of 2022, left the "bent pipe" setup.

## "Bent Pipe" Internet to ISPs
"Classic" model, most data heads to ISP, ratio in/out 4:1. Entry cost: US$10-$500K on ISP side and US$100M+ for building and launching the satellite. Satellites are typically shared. Operating cost: US$200+ per Mb/s per month.

## Direct to site
Subscription model for large number of end users, needs heavy satellite. At internet gateway, high gain (large) antenna. At user end, small antenna (VSAT - very small aperture terminal), 60cm diameter. Shared downlink bandwidth. Uplink from user site uses spread spectrum or burst-type arrangements.

#### Entry cost:
- US $1k on end user side
- US $100M+ for building and launching the satellite

#### Subscription cost:
- US$50+ per month depending on plan.
- Data caps or rate limiting per site.

## Direct to site downlink only
Subscription model for large number of end users in infrastructure-poor areas. At internet gateway, requires high gain (large) antennas. At user end similar to above, small antenna, (VSAT), 60cm diameter. Shared downlink bandwidth, uplink from user site uses wired telephone network.

#### Entry cost:
- US $1k on end user side
- US $100M+ for building and launching the satellite

#### Subscription cost:
- US$50+ per month depending on plan.
- Data caps or rate limiting per site.

## Direct to device (LEO)

Subscription model for large number of end users, needs many small satellites. At internet gateway, requires high gain (large) antennas.At satellite inter-satellite routing. At user end, small antenna, 3-36cm diameter (_few dozen_). Uplink/downlink similar to / same as 4G LTE or 5G cellular mobile data.

#### Entry cost:
- Less than US $1k on end user side
- US $1,000M+ for building and launching the satellite

#### Subscription cost:
- US$50+ per month depending on plan.
- Performance limitations? Volatile 60-300Mb/s down. 2-40Mb/s up.

## Satellite frequency bands
Trade-off, strength of signal/durability in the face of weather events (increasingly sensitive to atmospheric conditions) vs. bandwidth.

### L-Band (1-2GHz)
- Used for mobile satellite communications, GPS, and some television broadcasting.
- Very robust connection due to lower frequency which provides better penetration and diffraction around obstacles.
- Does not require large dishes or complex ground stations; portable terminals are often sufficient.
- Expensive bandwidth due to limited availability and high demand, especially from mobile services and GPS.
- Lower data rate capabilities compared to higher frequency bands.

### C-Band (4-8GHz) [GEO/MEO]
- Commonly used for satellite television broadcasting, some internet services, and long-distance radio telecommunications.
- Not affected much by rain fade, which is the absorption of microwave radio frequencies by atmospheric rain, snow, or ice.
- Subject to microwave interference from terrestrial systems, which can be a concern in densely populated areas.
- Requires moderately sized dishes for reception, typically around 1.8 to 2.4 meters in diameter for consumers.

### X-Band (9-12GHz) [GEO/MEO]
- Primarily reserved for government and military use, such as radar operations and secure communications.
- Resistant to jamming and interception, making it suitable for tactical military communications.
- Also used in some civil and commercial applications like weather monitoring and air traffic control radars.
- Offers a good balance between data rate capabilities and susceptibility to weather interference.

### Ku-Band (12-18GHz) [GEO/MEO/LEO]
- Widely used for satellite communications, direct-broadcast satellite television, and satellite internet access.
- Sensitive to atmospheric conditions, particularly rain fade, which can disrupt signals during heavy precipitation.
- Requires smaller dishes compared to C-Band, usually about 0.9 to 1.2 meters for consumer satellite dishes.
- Dishes must be accurately pointed at geostationary satellites to ensure a reliable connection.

### Ka-Band (26.5-40GHz) [GEO/MEO/LEO]
- Provides high-speed satellite broadband and backhauls for cellular networks.
- Bandwidth is cheaper due to a greater abundance of spectrum and smaller beam widths, which allow for frequency reuse.
- Rain fade is a serious problem, making the service potentially unreliable in tropical regions with heavy rainfall.
- Very precise antenna alignment is critical due to the higher frequency's shorter wavelength, which results in a narrower focus beam.

### E-Band (60-90GHz) [LEO]
- Increasingly used for short-range, high-bandwidth communications, such as point-to-point wireless links.
- Bandwidth is relatively cheap and abundantly available, supporting very high data rates.
- Atmospheric gases, particularly oxygen and water vapor, cause serious attenuation, limiting its use to short distances.
- Often used in conjunction with lower frequencies for last-mile access where direct line of sight can be maintained.

## What's all that about dish pointing?
Remember the path loss formula? Higher frequencies -> smaller wavelengths -> higher path loss.
- Lots itself is not a problem as smaller antennas give the same gain in dB at higher frequencies, can make up the higher path loss through higher gain antennas.
- But: the higher the gain of an antenna, the more directional it is!
    - Hence: Need to point short wavelength dishes more accurately than long wavelength ones
    - Or: Use beamforming with a large number of antennas (Starlink "Dishy")

## Bent pipe to ISP
Typical installation
- GEO, or more lately also 03b mpower MEO (with handovers)
- Up to a few 100Mbps down
- Up to a few dozen Mbps up

Link is actually shared between a few dozen to a few thousand end users.

Common feature:
- Long latency bottleneck.
- Large number of parallel TCP flows.

## Bandwidth-Delay Products (BDPs)
Typical bent pipe satellite BDPs (based on link RRT to ISP)

- 16Mbps x 500 ms link RTT GEO: 1MB
- 100Mbps x 500 ms link RTT GEO: 6.25MB
- 40Mbps x 130 ms link RTT GEO: 650kB
- 300Mbps x 130 ms link RTT GEO: 4.875MB
- Input buffer capacities not included

These can "store" a large number of packets "in flight".

# TCP Queue Oscillation
- Multiple TCP senders remotely send traffic to the sat gate
- Sat link is a bottleneck. Queue at sat gate acts like a funnel
- TCP sender cannot see queue state directly
- Feedback on queue state goes via the satellite to remote TCP receivers, and from there back to the senders.
- Long delays: >500ms on GEO, >125ms on MEO
- Queue can oscillate excessively between empty and overflow
- Complicating factors: TCP slow start, exponential back-off

## Four phases of queue oscillation
1. Sat gate queue not full. TCP senders receive ACKs increase congestion window. Queue builds up.
2. Sat gate queue full. New packets arriving are dropped. Senders still receive ACKs and send more data in the direction of the queue. Queue continues to overflow: burst losses.
3. ACKs from dropped packets become overdue. Sender throttle back. Packet arrival at queue slows to a trickle. Queue drains.
4. Queue clears completely. Link sits idle for part of the time, link not fully utilised.

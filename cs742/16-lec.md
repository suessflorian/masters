(20th Sept)

_Little scare mongering re: academic integrity_

# The need for decibels (CS315)
In communication, we often need to compare powers:
- Path loss: ratio of power at receiver compared to power transmitted
- Loss in cable: power out compared to power in
- Antenna gain: power seen from directional antenna compared to power seen from isotropic (omnidirectional) antenna
- Amplifier gain: power of amplified signal compared to power of input signal

Expressing and handling such ratios in absolute number is possible but cumbersome
- Values range over many orders of magnitude: need to divide and multiply very large and very small numbers
- Hard to read and interpret, error-prone when done by hand

## Decibels
Two powers, P1 and P2 as in decibels as
```
P1/P2 in dB = 10 log(10, P1/P2)
```

- Remember: log functions are not very sensitive to small changes in their argument
- The 10 is a convenience factor

As power is proportional to the square of the corresponding voltage (remember P = V^2/R), we can compare voltages in decibels too;

```
V1/V2 in dB = 10 log(10, V1^2 / R over V2^2 / R) = 10 log(10, V1^2 / V2^2)
= 10 log(10, V1/V2) ^ 2
= 20 log(10, V1/V2)
```

## Examples
(Can use wolfram alpha), power ratios;
```
1:1 = 0dB
10:1 = 10dB <-> 1:10 = -10dB
100:1 = 20dB <-> 1:100 = -20dB
1000:1 = 30dB
...
1.25:1 = ~1dB
2:1 = ~3dB
4:1 ~6dB
8:1 = ~9dB
32:1 = ~15dB
1:4 = ~ -6dB
```
Which of course differ to voltage ratios 10:1 = 20 log_10 (10/1)
```
1:1 = 0dB
10:1 = 20dB <-> 1:10 = -20dB
100: 1 = 40dB <-> ...
1000: 1 = 60dB

2:1 = ~6dB <-> inverse as we know...
4:1 = ~12dB
8:1 = ~18dB
1.4:1 = 1.5:1 = ~3dB
```

# Working in dB
**Add instead of multiplying**
- E.g., put signal into a cable that loses all but 1/10th of the input power: -10dB. Then feed into a cable that loses half the input power: -3dB. Total loss in dB: -10 dB + -3 dB = -13dB.
**Multiply instead of using exponents:**
- E.g., how much loss do we get if we use five cables in series? Each of which loses 7 out of 8 watts. (1/8)^5 is left. But ratio wise; We know 8:1 ~ -9dB hence final Decibel is 5 * -9dB = -45dB.

No need for a calculator. For power ratio to dB:
- Factor of 10 = summand of 10dB
- Factor of 2 = summand of 3dB
- Express ratio as 10^x * 2^y. Rounding up or down by a factor of up to sqrt(1.25) ~10% is allowed. In dB: 10*x dB + 3*y dB. Note x and y can be negative!

- Example; 47,527:1, round up to 50,000
express as 100,000/2 = 10*5 / 2^1 = 10*5 * 2^-1  => 5*`10dB` + -1*`3dB` => 47dB

## Using dBm
Fix the reference to 1mW (similar to SPL where we fix the reference to 20x10^-6 Pascals).
```
10dBm = dBm(10mW)
20dBm = dBm(100mW)
-50dBm = dBm(0.00001mW)
```

# Wireless of Basics
To communicate information via radio, we need:
1. An information source and a transmitter (black box)
2. A transmit antenna, if not mounted onto the transmitter, a "feedline" (coaxial cable) to the antenna.
3. A "line-of-sight" path from the transmitting to the receiving antenna, or a repeater/transponder of some kind, or a medium such as the ionosphere (upper atmosphere) that can refract or reflect our radio waves.
4. A receiving antenna and, if it is not mounted to the receiver a feedline to the receiver.
5. A receiver and an information sink.

## Point of Confusion
- In our previous definition, a transmitter is simply an electronic device that generates a radio signal and makes it available for transmission via a feedline and antenna.
- Sometimes (actually quite often), people will say "transmitter" but mean the entire "transmitter-feedline-antenna-system"
- The same applies to the "receiver".

# Fundamental Challenge
- Communicate as much as possible
- Across as much distance as possible
- In as little bandwidth as possible
- With as little delay as possible
- Using as little power as possible
- With the lowest error rate as possible
- Using devices that are as lightweight, cheap and compact as possible


# Characteristics of a transmitter
- Kind of information they transmit (analog, digital, voice, data, video, fax)
- The type of modulation(s) they use (AM, PM, FM, ASK, PSK, FSK, AFSK, QPSK, QAM, DSSS, FHSS, OFDM, ...)
- The centre frequency and bandwidth of the signal that they emit (few Hz to dozens of MHz)
- Their power output (few mW to 100s of kW)
- ... and a few other characteristics

Typical examples:
- Cellphone: Up to 23dBm (200mW) using OFDM with QAM/QPSK across multiple 15kHz channels using a variety of frequency bands.
- Cell site: around 10-15W
- WiFi: E.g., 802.11ac. Around 30dBm (1W) of 256 QAM at 2.4 or 5 GHz in channels up to 160MHz wide.
- Bluetooth: typ. 0dBm(1mW) of binary FSK in a bandwidth of < 1MHz at 2.45GHz

## Feedlines
Antenna to receiver or/*and* transmitter. They are typically found in fixed installations only where it is not feasible to connect the transmitter/receiver straight to the antenna.
- Example: "antenna cable" on a TV set - used so the signal can be received by a large high-gain antenna on the roof that would be out of place indoors
- Example: "transmission cables" in the sky tower. Actual transmitter is kept indoors for ease of maintenance access and protection from weather.
- A feedline always attenuates the signal travelling through it. At a particular frequency, we can specify a feedline's loss in dB per meter (dB/m). Longer the feedline and higher the frequency, the higher the loss.
- Bluetooth, 802.11 WiFi interfaces with internal antennas and handheld cellphones do not use feedlines.

Note: feedline with always attenuate. Electrical hesitance, higher frequency (skin effect) etc... impact this.

## Antennas
Various construction types, characterized by:
1. Frequency/frequencies of resonance, where the antennas have the highest gain (ability to transfer signal to the air interface). As a rule, the higher the frequency of operation, the smaller the antenna for a given gain
2. Gain is measured in dBi (dB over isotropic) or dBd (dB over dipole) in the main direction of radiation/reception. (dBd = dBi - 2.15dB). Rule of thumb: the larger the antenna the higher its frequency of operation, the higher its gain.
3. Directionality (e.g., dipole vs. dish). Rule of thumb: the larger the antenna, the higher the directionality. Think of a parabolic reflector mirror (car headlight)
4. Polarization (vertical, horizontal, LH/RH circular, elliptic). This may depend on the antenna's orientation at installation or may be a built-in feature.

Reciprocal, any transmit antenna can also be used to receive at the same frequency with the directionality and gain.

### Simple antennas
Simple antenna types
1. Isotropic antenna. Hypthetical antenna that has no gain, and radiates/receives equally well into/from all directions. It cannot be built in practice, though. It is used only as a reference for other antennas - hence "dBi"
2. Dipole. This antenna can be built in practice and looks like a stick half a wavelength long. It is mildly directional and has small gain: a receiver positioned perpendicular to the stick receives a signal that is 2.15dB stronger than it would be from an isotrophic antenna. Similarly, a dipole receives signal from this direction 2.15dB stronger than an isotrophic antenna would.
3. YAgi. Named after its inventor. Looks like a ladder, with steps made of dipoles. Your TVF antenna is probably a venison of a Yagi antenna.
4. Dish antenna. Very high gain and highly directional. Used mainly for satellite and microwave communication. Gain is proportional to exposed surface area (aperture), ie, twice the diameter means a gain of about 6dB.

# Propagation/Path loss
- Signals propagate spherically (transmitter is kinda-centered on the sphere)
- Obstacles cause additional signal loss
- Signal strength at distance r is proportional to 1/r^2 ("inverse square law")
- Path loss = (4*pi*r)^2/wavelength^2
- Each component should be explanatory there, recall `wavelength = speed of light / frequency` and `r` can be considered equivalent to the euclidean distance of the transmitting and receiving antenna's.
- Path loss (dB) = 10 log_10( (4*pi*r)^2/wavelength^2 )



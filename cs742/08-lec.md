3rd August (week 3)

## Continuing on with "Understanding Website Complexity"
- CDF Contribution of non-origin servers (fraction of contribution)

### Performance Implications
- Content-Level Characteristics
    - Total Objects
    - Object type: Number, Size
        - Absolute, Normalised
- Service-Level Characteristics
    - Number: Server & Origin
    - Non-Origin Fraction: Servers / Object / Time

What this paper has done, is correlate the series of metrics above to load time. They then plot the "Spearman" correlation coefficient.
- Num. Objects
- Num. JS
- Total Bytes
- Num. Servers
- Num. Origins
- Num. Images
- JS Bytes
- ...

Also, correlate the series of metrics that have a wide variability. All relatively low correlation.
- Num. Servers
- Num. Origins
- Num. JS
- Num. Objects
- Javascript Bytes

## Discussion and Summary
They do look at other factors
- Client-side plugins
    - `noscript` reduces num. objects by half, even though js objects accounted for 1/5 of objects.
- Mobile-specific customizations.
    - Mobile version reduces num. objects to a quarter.
    - Landing vs. non-landing pages
        - non-landing seem less complex by aggregate.

_Note: assignment group contracts_

# Next Paper "Ambient Interference Effects" in Wi-Fi Networks
Again a new theme, previous focused on web servers.

## Motivation
- Wi-Fi networks employ the IEEE 802.11 protocol which usees the unclicensed 2.4GHz ISM RF band.
- The ISM (industrial, scientific and medical) band is used by multiple devices (both Wi-Fi and non-Wi-fi), inherently causing interference for one another.
- Non-Wi-Fi devices are oblivious to the 802.11 protocol (polite protocol, transmit if it's clear).
- Deployment/operation of Wi-Fi networks often happens without knowledge of the ambient usage of the ISM band by non-Wi-Fi devices.

### Objectives
We consider 6 non-Wi-Fi devices:
- Unintentional interferers: a microwave oven, two cordless phones (one analog and one digital) (omitted), an analog wireless camera, and a Bluetooth headset.
- Intentional interferers: wireless jammers.
### Paper Studies
- Physical layer characteristics of interfere (controlled experiments)
- Inference on data, video and voice traffic.
- Interference on the operational performance of production network (passive measurements)

# Channel Structure in Wi-Fi
- Fourteen overlapping channels each having spectral bandwidth of 22MHz
- Adjacent channels separated by 5MHz (channel 14 exception, bigger)
- To avoid interference, wireless radios are expected to operate on non-overlapping channels
- Channel 1, 6 and 11 are most commonly used non-overlapping channels.

# Physical Layer Metrics
- Spectograms:
    - Representation of the RF (radio frequency) power levels over time in the spectrum.
    - Offer a temporal perspective of RF power in the frequency domain.
- Duty Cycle:
    - Measures the RF power in the spectrum; indicator of impact of RF power on the network performance.
    - Calculated by measuring the percentage of time the RF signal is 20 dBm above the noise floor.
- Tool: Using an off-the-shelf spectrum analyzer.

This paper is mostly concerned with controlled experiments. Running a microwave and just looking at the spectrogram and duty cycle graphs.

- Microwave as an interferer (chirping, intermittent) and a wide band interferer largely hitting channel 7-10. (50% duty).
- Analog video camera, similar to microwave (4-8 channels). Duty cycle is 100% means it is completely saturating the channels. Narrow band interferer.
- Bluetooth headset, low duty cycle (3.5%), but by spectrograph, is wide channel (FHSS, frequency hopping "SS", spread spectrum).

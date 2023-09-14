4th August (Week 3)

# Continuing "Ambient Interference Effects" in Wi-Fi Networks
Intentional vs unintentional interferer. Recall duty cycle a percentage based measurement that represents how occupied a channel is (by arbitrary threshold).

"Wideband, chirping" (radio frequency across many channels, chirping represents some "portion" of duty that is not 100%). *

## Analog Video Camera
100% duty cycle but concentrated on channels 4-6 hence considered "narrow band".

## Wireless Jammer
"Wideband, continuous interferer." This kinda puts into scope the weirdness around my introductory point of a "chirping" interferer;

### Continuous Interferers:
**Nature**: These are sources of interference that transmit continuously without any significant breaks.

**Impact**: Their presence can be consistently detected over a specified frequency range. This means that whenever your RF device is trying to receive or send a signal, it will always experience interference if it is within the range of the continuous interferer.

**Examples**: A malfunctioning electronic device emitting a steady RF noise, a jammer that is constantly transmitting, or any other RF source that has a continuous emission.

### Chirping Interferers:
**Nature**: The term "chirping" typically describes an interference source that varies its frequency over time, often in a predictable or repeating manner. This type of interferer doesn't stay fixed at one frequency but "sweeps" or "chirps" across a range of frequencies.

**Impact**: Chirping interferers can be more challenging to diagnose and mitigate because they change frequencies. A device might experience interference intermittently or when the chirping signal sweeps across its operating frequency.

**Examples**: Certain types of radars or electronic scanning systems might exhibit chirping behavior. In some contexts, a "chirp" can be a burst of increasing or decreasing frequency over a very short duration, useful for obtaining detailed information about a target's range in radar systems.

## Impact of Interferers on WI-FI traffic
The paper goes through two controlled experiments, the "data experiment" and the "voice experiment". The interferers are placed at different distances from the experiment and then we measure respectively the _throughput_ and _quality of experience_ (re: voice).

Unsurprisingly, in both experiments similar have similar degradation graphs (percent degradation x interferer distance).. The wireless jammer having major impact.

## Passively Interference in Campus Network
- Channel utilization and active time in channel. Took physical-layer measurements for 8 hours during a week day in the campus Wi-Fi network.
- Measurements were taken at a popular cafe frequented by students and faculty.
- Via special "Spectrum Analyser" tool

## Sumary
- The campus network is **exposed to a large variety of non-wifi devices**. These ofcourse can have impact on the network.
- Controlled experiments showed that even at distances up to 30m, some interferers can have a negative impact on data throughput and voice quality.

# New Paper "Comparative Analysis of Web and P2P traffic"
Compares different statistics
"Flow Characteristics" 
- Flow Size
- Flow Inter-Arrival Time (IAT)
- Flow Duration

"Host characteristics"
- Flow Concurrency
- Transfer Volume
- Geography

## Flow
Describes sets of packets that share common characteristics and presumably represent a single transaction or communication session between end-hosts. `Start` and `End` depends on the initiator. It is described usually by a 5-tuple;

1. Src. IP
2. Src. Port
3. Dest. IP
4. Dest. Port
5. Application (which then uses some sort of protocol)

## Application Identification
We look at that last point closer, how can we identify what a flow's application is.
- Port numbers: (if they use registered numbers, eg; `:80` http).
- Signature based: look at the payload might include a 'unique string' for example. Requires unencrypted traffic.
- Statistical approach: We look at unique characteristics of applications, ie is there a lot of two way permission, traffic at regular interval, other salient features; _the defining elements that distinguish one target from another_. Works well with encrypted traffic.
- ML approach: Similar to above effectively. But out of the box use of clustering.

## Flow Size:
Refers to the total number of packets or bytes that constitute a particular flow. It can be measured in terms of packets (packet count) or bytes (byte count).

## Flow IAT (Inter-Arrival Time):
Inter-Arrival Time (IAT) refers to the time gap between the arrivals of two consecutive flows. It's a measure of how frequently new flows are initiated.

## Flow Duration:
Refers to the time taken for a flow to complete, starting from the time the first packet of the flow is observed until the time the last packet is observed.

---

## Transfer Volume
Using flow information from a host. Transfer volume would be the sum of all the flows.

## Flow Concurrency
How many simultaneous flows, usually relative to some timestamp.

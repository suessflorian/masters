## Beginning QA Session

What is the primary purpose of passive internet traffic measurement?
- To capture and analyze traffic without altering it.
- To collect basic aggregate information, such as total bytes transferred.

Which type of measurement tool allows for greater customization and offline traffic analysis.
- Open-source software-based tools

What is the main advantage of performing internet measurements at edge networks
- Ability to capture traffic from thousands of user (large data sample) with a single administrative entity

Which probing mechanism is suitable (considering ease of implementation and privacy) for understanding latency and bandwidth availability?
- Active measurement
- SNMP polling (retrieving from Management Information Base in routers)

Why is performing measurements from multiple observational viewpoints important in internet traffic analysis?
- It enhances representativeness of results and reduces skews

You won't get multiple choices in the exam, they will rather be shorter answer questions and closed book.

# Outline
- Types of Measurement (active v passive)
- Measurement platforms
- Sound measurement practices
- Ethical issues

## Types of Measurement
- Active (based on issuing probes, analyzing response)
    - RTT measurement (round trip time): Ping
- Passive (observe existing traffic, example, IP packets, routing messages)
    - RTT measurement (round trip time): TCPTrace

## Comparison
Passive
- Only way to measure traffic
- MEasure user experience/behaviour
- Measure protocol exchanges
- Raises privacy concerns

Active (complimentary, can add probes into network)
- Measurements even when tapping traffic is not possible
- Measurees network, application perf
- Probing load
- May overload network, bias inferences

## Measurement Vantage Point
- Point where measurement host connects to network
- Observations often depend on the vantage point

If you have an end-host, connected to the internet; active measurements can be used to measure end-to-end paths, and passively measure of general host traffic. Routers-host, actively get to paint the entire network path within this router. And also passively measure more generally traffic, protocol exchanges.

## Measurement Platforms
General issues, can't find good vantage points or firewalls get in the way. Solution is to explicitly add measurement platforms... like some sort of network proxies.

- We go through a few examples
    - Measurement Lab (100 servers anyone can use)
    - Ripe Atlas (~ 10k crowdsourced, dongle eth proxy)
    - Looking Glass (Multi-Router LG software for routers, also crowdsource)

## Sound measurement: Build Trust
- Know what to expect (_if failure, check assumptions/measure error_)
    - RTT > distance/speed of light
    - num. bytes in TCP connection < duration * max capacity
- Know the measurement tool
    - Timestamp precision; resolution - microsecond?
    - Some clocks only advance every 10ms (**even if precision presented is higher**)
    - Measurement Outliers
        - Outliers/Spikes (high/low vs sudden lengthed frequency increase of characteristic)
    - Confounding factors (CPU/RAM usage, monitor overload missing measurement)
    - Evaluate via synthetic data, check accuracy
    - Compare multiple methods
    - Re-calibration (changing environments)
- Know where the data comes from

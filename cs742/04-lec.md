# Continuing themes
Knowing the measurement tool

- Know the measurement tool
    - Study precision and accuracy
    - Examine outliers and spikes
    - Monitor confounding factors
        - CPU, memory, traffic
    - Evaluate synthetic data, controlled settings
    - Compare multiple methods
    - Re-calibrate as needed
        - Changing environments

## Third Principle (recall the three)
Know where data comes from

- Log metadata with traces
    - Any information required to fully understand measurements
    - Remember data often used for unexpected purposes
- Examples of metadata
    - Version of measurement tool and parameters
    - When, where trace was collected
    - Clock precision
    - Drops, missing data, gaps

# Ethic Concerns
With active measurements, there's the natural concern that you will perturb the network in an overly oppressive way.

- Avoid disruption as much as possible
    - Active probing can overload network/host
    - Denial of service attack
- **Good practices**
    - Throttling probing
    - Spread load
    - Embed contact info in probes
    - Keep blacklists of network/hosts

## Respecting Privacy
Specifically an issue with **Passive measurements**; can in overtly personal/sensitive info
- **Good practices**
    - Get user informed consent when possible
    - Comply with local data protection laws
    - Anonymize data when possible

Basic common sense really.

##  (passive)Do no harm
Measurement studies can harm
    - Individual/organization privacy, reputation, well-being
- **Good practices**
    - Identify potential harms/risks
    - Maximuze benefits, minimize risks
    - [Menlo report](https://www.caida.org/catalog/papers/2012_menlo_report_actual_formatted/menlo_report_actual_formatted.pdf)

The menlo report is a good example, written by network security pro's, explained issues re: max benefit/minimize risk. Contains nice case studies...

This concludes the discussion on internet measurements.

Some MCQ review questions;

Match measurements tasks 1-4 with measurements approaches (active and passive)
- Network path delay (active, ping) _basically RTT_
    - AND PASSIVE; `traceroute` for example can also do the same.
- End-to-end path capacity (active, ping)
    - Bandwidth testing; `iperf`
- Packet and byte count on a link (passive)
- BGP protocol exchanges (passive)
    - Border gateway protocol, refers to a gateway protocol that enables the internet to exchange routing information between autonomous systems.

Which statement regarding internet measurements is true?
- Passive measurements are ideal when tapping traffic is not possible.
    - Active is preferred if tapping is not possible
- Technical and social factors do not affect the ability to quantify the Internets properties
    - They do effect, tier 1 provider access eg...
- The internet shows a number of unusual statistical properties that complicate measurement attempts.
    - This is a motivation as to why you do extensive internet measurements
- Internet measurements can be done at various vantage points.
    - INDEED

Which one of the following measurement locations would most likely provide us with a representative understanding of internet usage behaviour at a global scale?

- Spark 5G Wi-Fi hotspots
- Auckland Internet Exchange
- Spark Network
- AT&T Network (obv.)

What is the software called that is run on routers worldwide, allowing network administrators to discover routing information available at those routers.

- M-Lab
    - covered this one, servers around the world
- RIPE Atlas
    - covered this one, physical device
- BGP Viewer
- Looking Glass
    - covered this one, OS software to install
- Route Views

Fuck so this unveils how we are expected to recall specific suites used.

_Class has 70 students_, managed to get into my very own group. Last week shouldn't have any lectures. He's speaking a little about more assignment details here.

New topic.

# Workload characterization of a large systems conference web server
Each day we'll be talking about a new paper etc... all papers will have some form of measurements involved. On canvas, link will be provided. Need to be proficient at lit review. University access to journals. Also uploaded slides. 

This paper about, web workload characterization. WWW2007 conference, using collection from server-side and client-side. Datasets collected over a year period (longitudinal) in form of server logs and google analytics client. Provide multi-layered workload analysis (??) of the WWW2007 conference web site.

30% JPG, 13% PDF, 35% Artwork. Why tf are we looking at aggregates that are almost 2 decades old?! 

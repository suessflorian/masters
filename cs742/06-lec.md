28th July (still week 2)

# Finishing off the lit review guide
How to narrow down papers from key word search; poster vs paper (poster is summarised of the paper). Papers are presented orally.

Recommended stepwise approach;

- Build list of papers (based on titles)
- Reading abstracts (summaries), discard
- Look at the introduction
- Then you read the entire paper...

Quality control; many ways identify quality, paper acceptance rate of a conference (statistic), 10-20% are top, 20-50% average, rest you have to be careful. Journal impact factor (content citations); 2+ okay, 10+ very high.

- Reference management system (latex bibliography perhaps)
    - Mandelee 
    - Refworks

# Administrative Announcements
Groups get in one... class rep. Assignment speak. Academic integrity. Recommends chatGPT as a tool.

## Pinging in the Rain (Paper)
Aaron Schulman and Neil Spring University of Maryland (UMD), IMC 2011. We look at the pre-publish paper. Impact of weather on internet connectivity. Last mile connectivity (edge) as a lot of research has been done on core.

- Links are not AS redundant as core
- Equipment updates are rare
- Equipment operates in an uncontrolled environment

### Weather-related internet outage
- Lightning and wind cause local power outtages
- Wind snaps tree limbs and stresses wires
- Water in atmosphere degrades satellite links (if no copper, fibre etc..)
    - Need direct line of sight etc...
- Water seeps into cables and equipment

Measuring weather-related failures, identify residential IP addresses that will be subject to weather, measure conectivity of internet hosts, _before, during, after_ periods of severe weather. Determine when hosts loose connectivity and categorize wheter these failures occur during sever weather events vs. clear skies.

Failures are 4x more likely during thunderstorms and 2x more likely during rain. Duration of weather induced outages is relatively small for a satellite provider.

Limitations; do not isolate weather-related power failures from network failures. Do not distinguish between actions of individuals from network failures that affect many hosts. Use of scalable data sources, but imprecise reports of weather and hosts to find correlations between the two.

Choose IP addresses ending in 1., .44, .133 for every possible /24 block. Query name of each IP addresses and look for well-known US ISP. If any three IP addresses have a matching name, then find names of all IPs in the /24 block. Found 100 million US residential IPs.

Aiming pings at severe weather spots as they come. Listening to weather events. Locating IPs covered by weather alert; locate 100 million IP addresses, use MaxMind GeoIP city database to determine longitude/latitude. Map weather alerts to these located IP addresses. Determine provider and link type (provider name and the link type). Sample IP addresses by weather alert.

### Pinging to observe failures
- Ping from 10 PlanetLab vantage points
- Ping infrequently (11min)
- Omit needless pings
- One ping is not enough (retry immediately when a ping indicates failure)

### Categorizing if the failures occurred during severe weather
Visibility, lightning detection, precipitation identification, cloud coverage, temperature, precipitation accumulation from **airport** weather stations. "Weatherunderground.com" provides an archive of this (hourly intervals).

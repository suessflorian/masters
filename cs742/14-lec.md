(17th August Week 5)

Starts out with a couple examples of topics that could be used for the group research project.

- Video conference or Zoom traffic characteristics
- VPN Ecosystem analysis [CLAIMED]
- Starlink Traffic (IAMC, ICMP) [CLAIMED]
- Censorship, and how to circuit it

## "Characterizing the File Hosting Ecosystem: A View from the Edge"
Passive measurement on a edge network. Longitudinal (~1 year). Multi-level; usage behaviour, infrastructure, content characteristics and user-perceived performance. rapidshare, megaupload, share, mediafire, hotfile.

## Contributions
- Largest, re: file hosting ecosystem
- Compare/contrast these services with each other
- Implications on caching, network management, content placement, data center provisioning.

## Vantage Point 
- End systems (clients and servers)
- Edge networks
- Core networks

This work was done at the edge network via packet capture of edge routers. Both active and passive where used.

## Datasets
- HTTP transactions collected from a large campus network with 33k users over a period of 1 year.
- Used `Bro` parsing capabilities to summarize HTTP request-response pairs in real time.
- User identifiable information such as IP and cookies are not stored.
- Aggregated the traces using the HTTP HOST header for the Top-5 services.

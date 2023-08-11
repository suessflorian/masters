# Workload characterization of a large systems conference web server
Continuation from last lecture. Longitudinal a year long, about the paper. Statistics show discrepancy between server and Google analytics. Chart breakdown of response codes.

Server logs (passive), Google Analytics (claimed active, pretty sure it's passive though, need to clarify re: Piazza). Table shown... Speaks of standard form server logs (_? I thought this is arbitrary_). 2XX success, 3XX, redirection/cache, 4XX client side error, 5XX server side error.

## Hits
- SERVER: Record hits to every file on the server, providing a more complete record of resource access patterns
- GA: Tracks pages (HTML, ASP etc..), but does not record hits to the individual resources (images etc...).

## Visitors
- Unique visitor is identified by a unique IP address in the log
- GA and other page tagging visitors and their visits by placing cookies based on session IDs on the client side.

## Visits
- Web proxies and dynamic IP addresses make it difficult to track unique visits to the site.
- Visits from search engine crawlers (spiders) are ignored by GA. 

## Traffic Volume
- Records size of request.
- Cannot measure traffic.

## Page Errors
- Provide details about server and client errors.
- Does not record page errors.

--

# Google Analytics is considered a passive measurement tool.

Here's why:

1. **Data Collection**: Google Analytics collects data by embedding a JavaScript code snippet into web pages. When users visit these web pages, their interactions (like page views, events, etc.) are tracked and sent to Google Analytics servers. This process involves monitoring existing traffic rather than introducing new traffic to make measurements.

2. **No Alteration to User Behavior**: Google Analytics tracks user interactions without influencing the users' actions or decisions. It merely observes and records what users do naturally.

3. **Concerns**: Passive tools, like Google Analytics, can raise privacy concerns, as they collect data about user behavior. However, Google Analytics anonymizes IP addresses by default and follows various privacy guidelines to protect user data.

In contrast, active measurements would involve actively sending traffic or requests to gather data, like how a speed test tool would work. Google Analytics doesn't send additional traffic to measure; it just observes existing traffic.

--

## Traffic Profile
- Basic comments on traffic volume and patterns
- Most daily/monthly/yearly visits mention

It's mostly basic analysis on time series graphs; trends (time of day/week traffic), visit duration, page errors, traffic volume, geographics (mapping IP addresses to countries, woah), traffic sources (how users are coming to the website), robot visits.

# Summary of Paper
- using both server-side and client-side measurement we analyzed usage behaviour, client errors, bandwidth, and robot activity of the site
- non-stationary traffic statistics
- Visitor activity showed no strong diurnal (circadian) pattern due to international usage
- Almost half of all visits came via search engine
- Robots were prevalent

## Words on Literature Review
How do you find certain conferences/journals (use of Google scholar), UoA has a no cost access to most of these available.

- [Auckland University Library](https://www.auckland.ac.nz/en/library.html)
- [Databases for Computer Science](https://auckland.primo.exlibrisgroup.com/discovery/dbsearch?query=contains,dbcategory,&tab=jsearch_slot&sortby=title&vid=64UAUCK_INST:NEWUI&offset=0&databases=category,Science%E2%94%80Computer%20Science)
- [ACM Digital Library](https://auckland.primo.exlibrisgroup.com/discovery/dbfulldisplay?docid=alma9988992814002091&context=L&vid=64UAUCK_INST:NEWUI&lang=en&adaptor=Local%20Search%20Engine&tab=jsearch_slot&query=contains,dbcategory,&sortby=title&offset=0&databases=category,Science%E2%94%80Computer%20Science)
- [IEEE Explore](https://auckland.primo.exlibrisgroup.com/discovery/dbfulldisplay?docid=alma9990624514002091&context=L&vid=64UAUCK_INST:NEWUI&lang=en&adaptor=Local%20Search%20Engine&tab=jsearch_slot&query=contains,dbcategory,&sortby=title&offset=0&databases=category,Science%E2%94%80Computer%20Science)
- [SpringerLink](https://auckland.primo.exlibrisgroup.com/discovery/dbfulldisplay?docid=alma99169159414002091&context=L&vid=64UAUCK_INST:NEWUI&lang=en&adaptor=Local%20Search%20Engine&tab=jsearch_slot&query=contains,dbcategory,&sortby=title&offset=0&databases=category,Science%E2%94%80Computer%20Science)
- Not visible; Science Direct.

How to access outside of university campus, [EZ proxy](https://www.library.auckland.ac.nz/services/it-essentials/access-electronic-resources).

Here; add this `http://ezproxy.auckland.ac.nz/login?url=%@` prior.

_can't really check these links, could be broken_

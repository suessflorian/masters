2nd August (week 3), assignment has been uploaded.

# PDF (Probability Distribution Function) 
And CDF graphs were covered... we don't need to really take notes here. We are very familiar with these types of graphs already. Empirical distribution functions. CDF 0.5 equates to the median value.

... Continues the review of some CDF's provided in the "Pinging in the Rain" paper.

## Future Work
- Better geolocation of IP addresses.
- Augment surface measurements from airports.
- Isolate power failures.
- Determine where the failures are in the network.
- Expand the study beyond US.

# New Paper on "Understanding Website Complexity"
## Measurement, Metrics and Implications

Authors found websites taking a while to load. We go through the network dev tab of some 2013 designed CNN site. Noted that requests are going to different domains altogether.

User surveys shows 67% of users encounter "slow" sites once a week. How long a person will wait for pages to load before navigating away (2000-2009).

_Basically, slow loading websites are bad_.

## Work done
- Comprehensive study of a website complexity.
    - Analysis of sites across rank and category.
    - Content and service level metrics.
- Key metrics that impact performance.

## Measurement Setup
- 1,700 websites from Quantcast top-20,000
- Primary focus on landing (home) page
- Annotated with Alexa Categories

### Tools
- Firefox
- Disabled local caching

### Approach
- 4 vantage points (3x EC2 instances AWS, 1x UCR (university))
- Every 60 seconds one page loaded
- ~30 measurements per site per vantage point over 9 weeks.

### Preliminary Notes
Recall html > css, images and scripts are requested in parallel (throttled by how many available parallel threads are available).

## Complexity wrt. (Content-Level and Service-Level)
- Content-Level; number of objects, size, type.
    - CDF of the number of objects grouped by class/category (news, business etc..). 
    - CDF over rank ranges, shows not too much difference.
_Note: head and tail of distributions..._
    - Types of objects broken down by class/category (bar for image, javascript etc...)
        - Normalising the results to fractions per image, js, css etc... over class/category.
- Service-Level; focus on the servers themselves that host/deliver the content.
    - CDF on number of servers grouped by class/category (anomaly for news, 30 vs 8 median)
    - CDF for top 2 level domain name (origin). TLD, 2LD (2TLD).
    - Breakdown of popular non-origin providers (GA, doubleclick, quantserve ..., facebook). Mention of the 1x1px image for tracking (shoutout to Movio)!!

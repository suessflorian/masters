(16th August Week 5)

Second assignment introduction. Group assignment (due Sept 15th). Mini lit review.

- Need to find a topic to cover (that'll be our first meeting goal).
- Access the library via that tutorial provided earlier. Need conferences.
- In our group we want to have about five different research papers.
- ...

Rest is kinda in the document provided. So just read that and build a plan.

## An Analysis of Facebook Photo Caching
There are various cache policies (LRU, TTL etc...); which is best? I'm gonna head to the original presentation, note at time of writing, 9 years old.

- Various different levels (browser is really important).
- Average. per photo popularity shifts between layers (further in the less popular).
- A partnered CDN caching approach with Akamai
- Focus: Facebook
- Edge Cache (geo-distributed) (first layer after browser), points of presence (PoP) uses the FIFO.
- Origin Cache (next layer). Then "Haystack".
- Sampling... logs needed to be gathered to monitor activity, we sample for feasibility.
    - Request-based vs. Object-based Sampling
    - It's an interesting dilemma because sampling requests will give you representation of average traffic, objects with low popularity have a low chance of being visible (relative to high popularity objects). Hence you instead sample your objects and for each object in the sample, log any activity. This gives a you more representative understanding of each object with respect to request count and popularity.

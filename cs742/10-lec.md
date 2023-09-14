(9th August week 4) 

# Continuing on "Comparative Analysis of Web and P2P traffic"
Main focus on differences between web and p2p traffic. We covered a lot of definitions last lecture.

- Flow size
    - Web: Introduces many mice and few elephant flows
    - P2P: Introduces many of both
- Flow IAT
    - Web: Typically short
    - P2P: Typically long
- Flow Duration (begins at SYN packet, ends RESET/FIN packet)
    - Web: Short-lived
    - P2P: Long lived.
- Flow Concurrency:
    - Web: Most hosts maintain more than one concurrent flow.
    - P2P: Many hosts maintain only one flow at a time.
- Transfer Volume:
    - Web: Large transfers are dominated by downstream traffic.
    - P2P: Large transfers happen in either upstream or downstream direction.
- Geographic:
    - Web: Most external hosts are located in the same geographic region.
    - P2P: External peers are globally distributed.

## Methodology
- `lindump` from the 100MB/s full duplex commercial internet connection of the university of Calgary.
- P2P use random port numbers, hence used payload signatures to identify applications.
- Used `Bro`, a network intrusion detection system, to perform payload signature matching and map network flows to traffic types.
- Due to storage limitations we used non-contiguous 1-hour traces collected each morning and evening on Thursday through Sunday Apr 6-30th, 2006.

---

Mice (<10KB) and elephant flows (> 5MB). Otherwise we have gone through the characterizations of different metrics in our last section of notes.

---
_We go over PDF (probability distribution function) again_; give a random variable X, the PDF of X is denoted as `P(X)` is the probability that X is equal to `x`, i.e, `P(x) = P[X=x]`. Then CDF measures the probability that X falls below a specific value, `F(x) = P[X<=x]`... Complement-CDF (**!**), CCDF detailed view of the **tail** of the distribution, probability of x begin above a specific value. `CCDF = P[X>x] = 1 - F(x) = F'(x) = F_c(x)`.

---
I think it's important to note that I didn't write notes for the entire class's content here. There was way too much specifics provided for a result that is quite old. The more important pieces to me were the use result portrayal and any keyword definitions needed to learn.

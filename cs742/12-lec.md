(11th August Week 4)

# Another set of questions around ZIPF distribution
A dummy distribution is given of web objects requested from a CDN. The x-axis represents the web objects requested from the CDN in ranked (ascending) order with the most popular objects on the left, and the least popular objects on the right. The y-axis shows the number of times the web objects have been requested from the CDN. Note that the graph is in log-log scale, and (1,1) is the origin. A straight line in the rank-frequency domain on a log-log scale is a distinctive feature of Zipf's law.

1. Write down the foruma of Zipf's law. `F(x) ~ 1/R^\alpha` which concretely means;`F(x) = C*R^-\alpha`.
2. Find the parameters of the Zipf distribution. `log(F) = -\alpha log (R) + log (C)` - note the similarity to the `y = mx + c` function of a linear line. The slope then determines precisely `-\alpha = -1`, and the `log(C)` value represents the intercept.
3. Is this a pure zipf distribution; answer is yes iff \alpha = 1, in our case \alpha = 1. So yes.

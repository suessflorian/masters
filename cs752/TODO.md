- well formed PGM models and their extensions
- read the entire document related to AWS DynamoDB
- Look at previous exam

# Catchup with Lin Shi
Doing concurrently a 65 point research paper which continues throughout the year.

Has prior experience with DynamoDB...

We ended up thinking "what makes DynamoDB eventually consistent". The property by itself to misleadedly describe the lack of consistency within context of being transactionally ACID.

Could be a good topic, seems straight forward and easy to motivate the reasoning as to why it's worth looking into.

```
(c1,c2) <- :buys(c1,p),:buys(c2,p)
(c1,c2) <- :buys(c1,p1),:buys(c2,p2),:buys(c,p1),:buys(c,p2)
```

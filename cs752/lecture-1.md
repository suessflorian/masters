# Course Administration
Lots of big words lecturer (Sebastian Link) 😅 - second half Ninh Pham.

- motivating the course (businesses extract value out of data)
- roughly 180 big (some based overseas)
- an actual set of industry advisors. cool
- decent set of outcomes
- lots of talk about team presentation (grrrr) 

## Grading
- Four assignments (%5 each)
- Small team presentation (%20)
- Final exam %60

## General to both 752 and 711
- 7 weeks for first half of semester
- 5 weeks for second half of semester


# TODO
Look at those topics and choose one, make a call to arms in Piazza or something equivalent.

```
Assembling a team for a deep dive into AWS DynamoDB or CouchbaseDB!

Hopefully this is the right place to do this, but I'm real keen to meet up with people with a similar interest to me - unfortunately I haven't been available in classes last week to bring this up earlier, only just recently caught up with the lectures on Monday and Tuesday last night. But now having caught up with the recent material, looking at the topics still available I'm definitely most interested in the two well known stores AWS DynamoDB and/or CouchbaseDB.

Firstly, having experience designing a few green field systems when your bounded contexts aren't quite well defined, schema flexibility I can imagine is hugely beneficial. I also resonate with the sentiment that most production systems use stores using key value lookups which seems to be quite a motivation for these stores.

Surprisingly I've run into many different limitations brought to light by more traditional relational stores like MySQL, Postgres (my fave), and AWS's Aurora DB regarding horizontal scaling. The usual way to handle increased IO load is to beef up a central instance, or separating reader (replica's) and writer instances. It's not too bad nowadays with increasing popularity of managed DBMS (AWS RDS), but it's still something that you need to be conscious off.

Although both these stores have (more or less) recently adopted transactionally ACID modes of operation, I'm interested in the whole eventual consistency issue of these DB's and how to utilise these stores to accomodate consistently high read performant applications. 
```

We did technically have a course before this which simply introduced knowledge graphs (KG). Applied it to areas such as Google's own KG, NLP. De-motivated novelty, assigned similarity to description logic (DL). Similarity to RDF's. etc...

# How to construct a KG
- extract information (from text)
- match/merge entities
- knowledge refinement

_hinting at using nlp python libs for assignment_

## What is a KG
entities, attributes and relationships. nodes, labels, edges.

So we look at extraction techniques, step 1 of four steps re: presenting a polish KG about some domain (other steps include refining etc...)

# Extraction
Looking at NLP in particular, tokenization, parsed into components which is then transformed into a graph.

1. Dependancy parsing, tagging tokens, named entity recognition (sentence)
2. Co-reference resolution (document), linking synonomous symbols
3. Named entity resolution (not trivially matching symbols), linking, relation extraction (information extraction)
Problems:
- different names for same entity
- same/similar names for different entity

Procedure 😴:
1. candidates
2. narrow by entity tyes
3. coference
4. coherence

Just seems jargonic to me. Checkout [NLTK](http://nltk.org)

There's also `NER` which is different. Classifies: `noun`.
> Structured classification to add category label (e.g. Person, Location, Organization,...) for entity mentions and entity types.

Checkout [Spacy](http://spacy.io).

The concrete sub problems of knowledge extraction given good execution of steps 1-3 are:
- Defining domain
- Learning extractors
- Scoring the facts

We introduce precision by human intervention (supervised, semi-supervised, unsupervised).

# Learning Extractors
Intervention may be defining a domain, of structured ordered entities. If unsupervised you can imagine a non-ordered set of entities. But here we loosely have our set of RDF facts that are reinforced by some inferred or introduced via supervision RDFS equivalents. (TBox inclusions of concepts and roles, ABox your memberships) 

Note that when scoring candidate facts, there may be employed many heuristics, such as pattern count that supports a fact etc...

## PART II

# Entity Matching
Identify and discover instances referring to the same entity (synonyms). **disambiguation challenge**.

## Covered Techniques
- collective resolution in linked data
- distance based models (very intuitive, per label comparison build score, vertix merge if similarity per vertex is the same... but slow)
_and not covered..._
- probabilistic matching models
- declarative matching rules and constraints

## Solutions to slowness of distance based EM models
### Inverted Index
Can reduce set of candidates to properly EM. Filters out very distant entities if there is no feature overlap.

### Locality-sensitive Hashing
We just bif around a hash map. We assume hashing function places entities with similar features to _similar_ bucket. (so hashing function takes in list of features).

## Knowledge Fusion
Now that we have a set of derived facts, how do we fuse competeing facts (to decrease model contradictions).

Solutions: intervention, or based on other sources.

## Error detection and fact inference
Functional dependency (Zip -> City)
Inconsistency rules (DOB > DO Death)

# Part III (CHALLENGES)
Challenges of using KG's for Q&A
- parsing the query, will be NL.

Challenge dimensions of a scaling KG's
- coverage
- correctness => conflicts with freshness (slower) and coverage (increasing confidence to rule out infered facts)
- freshness => conflicts with guards to garantuee correctness (avoiding slowness)

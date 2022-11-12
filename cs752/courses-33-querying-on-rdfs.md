The reading is useful btw 
[here](http://webdam.inria.fr/Jorge/files/wdm-querying-ontologies.pdf)

# Description Logic
DL is a `decidable` fragment of FOL allowing reasoning on complex logical axioms over unary and binary predicates.

```
Class = Concept
Property/Relation = Role
Schema = TBox
Instance = ABox
Ontology = TBox + ABox
```

`TBox T`, state inclusions of concepts C `subset` D and roles R `subset` Q...
`ABox A`, state memberships, `C(a)` or `R(a,b)`.

# DL knowledge base L = <T,A>
Loosely translates to the ontology right.

## Reminder
RDF => instances of classes `C(c)`, set of triplets (facts) `P(i,k)`
RDFS => class heirarchy, property heirarchy, domain & range classification

So... DL as we define it here, has a polynomial evaluation time, where as an extended variant with OWL appears to have exponential evaluation time.

_some gentle revision on inference, no real focus needed here, all intuitive_

# Saturation Algorithm
Exhaustively infer facts. Note: **only polynomial number of facts can be added**. PTIME.

Haven't really covered anything, we materialised a RDFS graph with a set of RDFS rules. We then played around with evaluating a CRPQ on top of a set of RDF facts. Evaluation on RDF vs evaluation on RDF + RDFS. Later will always have a superset of query results.

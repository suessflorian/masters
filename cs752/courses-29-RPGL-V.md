# Composability
What if the output of a graph query is a property graph itself? Plenty of benefits, composing queries, "materialized views", "access-control", "performance tuning".

1. Create vertices (with labels?)
2. Create edges (with labels?)
3. Create property values

## Syntax introduction of RPGL-V
So recall that `RPQL` has head predicate _head_ is either of the form
`p(x,y) IN C` OR `result(x1,...,xn)`... we introduce now `p() IN C`. Eg.

```
:TrainingTandem() IN c <-- :Apprentice(x),:worksFor(x,y),:Expert(y)
```

So this creates a `TrainingTandem` vertix for every pair of (apprentice, experts) such that the apprentice works for the expert.

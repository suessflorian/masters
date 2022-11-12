# Extending RPGL-V, RPGL-G then RPGL-GP

## RPGL-G, vertices with edges
Permit the head predicate head to be of the form `Hv`, `He`, or `result(x1 ,...,xn)` where:

- `Hv` is the set of head predicates `h` of the form:
`p() IN c AS v`. Note `v` does not appear in any body predicate or other simple head predicates of the same rule.
- `He` is the set of head predicates `h` of the form:
`p(x,y) IN c`, both `x` and `y` appear in a body predicate (not nessecarily the same).

## RPGL-GP, vertices with labels then edges,
- Extends the form `He` to
`p(x, y) IN c` AS `e`, which allows body predicates to act on `e`...

Something like this anyways.

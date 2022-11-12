# Specializations of PGM

# PGM incorporates four basic traits of Contemporary graph data models
Properties of PGM and it's extensions:

- **Direction (ordering of vertices, `n`)**
`codomain(n) = {{x,y} | x, y in V AND x != y}` **(undirected alternative)**

- **Multi-graph (same pair of vertices can have many edges between them, aka differing relationships)**
In contrast to simple graphs. `n: E -> V x V` required to be injective or 1-1. ie, if `n(e1) = n(e2) => e1 == e2`.

- **Multi-Labeled**
In contrast to `codomain(lambda): L` (compared to `P(L)`), note some models only allow labels for either `E` or `V`. Moreover, could be label-less. `for all x in (E U V), lambda(x) == empty set`

- **Properties**
Data-attributed graph models restrict `v`: `(V U E) x K -> N`, by `K = {0} AND N={0,1}`. (binary values).

Can restrict domain `(V U E)` to just `V` or just `E`.

---

Core message is PGM is more or less an attempt to generalise all restrictions listed above which were attributed to previous graph models.

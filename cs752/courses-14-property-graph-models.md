# Property Graph Model
XML puts data on tree's, now we turn to putting data on a graph. We'll focus on `Neo4j`. QL is called `cypher`.

## Goals
- Property graph model, LDBCs Graph Query Language Task Force.
- Number of variations of the property graph, specializations and extensions.
- How does property graph model fit in the existing family of graph models.

Def:
### Data is represented directed, attributed, multi-graph

---

**vertices AND edges are rich objects with:**
- set of labels
- set of key-value pairs, `properties`

Notation:
`O` set of objects, `L` set of labels, `K` property keys, `N` set of values

WE define a property graph with structure (V, E, n, lambda, v) where
- `V` is element of `O`, called vertices
- `E` is element of `O`, called edges
- `n`: `E -> V x V`, function assigning each edge an ordered pair of vertices
- `lambda`: `V U E -> P(L)`, function assigning each object finite set of labels (note: `P` denotes the power set).
- `v`: `(V U E) x K -> N`, partial function assigning values for properties to objects, such that the set of domain values where `v` is defined is finite.


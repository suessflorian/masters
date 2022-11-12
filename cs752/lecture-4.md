# Live lecture reviewing courses 13-20
Starts of with a focus on OPPGM-Graph, object path property graph model. Nothing massive about this other than for every path in `P`, we denote a function that yields a set of edges.

OSPG introduces the notion of well-formed. For every subgraph, that is a set of edges and vertices. Then for each vertex in the vertix set, all edges contained in the subgraph that are incident to this vertex, suggests that the source vertex is also in the subgraph. Moreover, for each of the edges in the subgraph, the vertices that are defined to be adjacent via this edge must also be contained in the subgraph.

More correctly: `For the edges contained in the subgraph, it's adjacent vertices must also be in the subgraph.`.

------

HVPGM... View these subgraphs as vertices themselves.

## Extensions
Less fundamental than structural extensions OPPGM, OSPGM, HVPGM, HEPGM.
- concern rather data properties, practically relevant and common in implmentations.

- Most PGMs have typed values (intergers and strings)
- system maintains a type system (each `N -> T`) where `T` denotes the set of types.
- systems may yield more than one value per key.
	ie; v: (V u E) x K -> N becomes v: (V u E) x K -> P(N)
- Let `I` be set of identities used by a system, `i: O -> I`

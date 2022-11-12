# Hyper Edge Property Graph Model
Hyper edge links a non-empty sequence of vertices without repititions. If all hyper edges only have two adjacent vertices, can be viewed as a bare bones PGM.

A hyper edge is an edge that contains any sequence of vertices
- so the bare bones PGM is a special case of HEPGM where each edge contains a sequence of exactly 2 vertices.
Hence HEPGM is a generalisation of PGM.

So there is a different between HEPGM and OPPGM, where HE's are contains a non-repeating seqence of vertices
	compared to a Object path that contained an "arbitrary" sequence of edges

So like OPPGM, you can associate labels and properties to each HE.

So

- `V in O` (vertices)
- `E in O` (hyper edges)
- `η: E → ⋃ X ∈ P(V)−{∅} {[π(1),...,π(|X|)]` where `π` is a bijection from `{1, ..., |X| } -> X` where each hyperedge is given a non-empty sequence of vertices without repitition.

# Regular Property Graph Algebra
More procedural compared to RPGLog

Use of algebra in the sutdy of engineering of graph queries
- compilation
- execution

RPGL is equivalent to RPGA, most likely will proove this.

Expressions think of `e` as "expression":
`e := l | e∗ | e ∪ e | |><|Φ,c posi,posj (e,...,e)`

- `l in L`
- `(e,...,e)` is of length `n>0`
- `c in C`, context identifier
- `posi,posj ∈ {src1,trg1,...,srcn,trgn}`

`Φ` is a conjunction of a finite number of terms of the form:
- `λ(pos) = l` for `pos∈{src1,trg1,...,srcn,trgn}`.
- `posk.p θ posl.q or posk.p θ val`, for `posk,posl∈{src1,trg1,...,srcn,trgn,edge1,...,edgen}` then `p,q∈K, val∈N` and `θ ∈ {==,!=,<,>,<=,>=}`.
- `posk = posl` for `posk,posl ∈ {src1,trg1,...,srcn ,trgn}`

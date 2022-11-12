# Regular Property Graph Queries
Note so far we haven't been able to query actual properties. Our querying languages have only thus far dealt with labels.

So far we have focused on graph navigation, now we focus on more the property clauses. 

### Generalises previous queries

# Two Key Formalisms (both equivalent)
## RPGL (declarative)
## RPGA (more procedural)

We begin by looking at RPGL (aka RPGLog)... fragment of non-recursive Datalog tailored to property graphs.

- RPGL, corresponds to `unions of conjunctive queries on graph`
- predicates to be binary OR unary (edge labels, node labels respectively)
- `*`
- Nesting of sub queries

`E` a set of edge labels, `V` a set of vertex labels, `E ∩ V = ∅`
roles: refer to edges and vertices in head and body predicates
`C` denotes context identifiers
role: distinguish edges created by different rules (we've seen this before)


`head <--body1,...,bodyn ,constraint1,...,constraintm` with `n > 0` and `m >= 0`

`bodyi` can be in one of the following forms: (body predicate)
- `p(x,y) AS e`
- `p*(x,y)`
- `p(x)`

Where `x,y` are in `V`, `e` are in `E`.

_Lots of focus on not allowing recursion_

`constrainti` is of one of the following forms: (body predicate constraint)
`x.pθy.q`, or
`x.pθval`
where `x,y ∈ V ∪ E`, both `x` and `y` appear in a non-constraint body predict (not
necessarily the same predict), `p,q ∈ K`, `val ∈ N` and `θ ∈ {==,!=,<,>,<=,>=}`, or,
of the form
`x = y` where `x,y ∈ V` and both `x` and `y` appear in a non-constraint body predicate (not necessarily the same predicate)

`head` (head predicate), is either of form `p(x,y) IN c` where `p∈L`, `c∈C`, and `x,y∈V`, and both `x` and `y` appear in a body predicate (not necessarily the same predicate)

OR

`result(x1,...,xn)` where `n>=0`, `result` is a reserved predicate not in `L,x1,...,xn ∈ V` and each `xi` appear in a body predicate.

# Now we need to show this is not recursive
We begin by introducing a preliminary term

## Dependancy Graph

- Given a set `R` of rules, the dependency graph of `R` is the directed graph.
- Having as node set the elements of `L` appearing in a predicate of a rule of `R`.
- With an edge from `x` to `y <=> x` appears in the head of a rule `r` and `y` appears in the body of `r`.
- `R` is recursive if the dependency graph of `R` has a cycle, otherwise `R` is non-recursive.

### So what is an RPGLog
A finite non-empty non-recursive set of rules such that at least one rule has head predicate result and all result predicates have the same arity.

# PART 2

Now to relate all of this on a `G = (V,E,η,λ,ν)`, and `q∈RPGLog`, `r∈q`:
A function `μ:V ∪ E -> O` assigning object identifiers to variables
A mapping `μ` satisfies `r` in `G` <=> `μ` satisfies each body predicate `b` of `r`.

We go an iterate through each `b` form

We also introduce a method of associating unique object identifiers:

`ωG: O×O×C --> O\(V∪E)` is an injective function

Then we step out to rule evaluation... so 
Then we define transitive closure evaluation
And a bunch of other things that are way too technical

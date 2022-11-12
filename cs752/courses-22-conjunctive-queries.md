# Conjunctive Graph Queries
`q = (a,b) <- :knows(a,u),:worksFor(a,v),:knows(v,b),:worksFor(u,b)`

Given a `G=(V,E,η,λ,ν)`, and a conjunctive query 
`q = (z1,...,zm) <- a1(x1,y1),...,an(xn,yn)`, a mapping for `q` on `G` is a function
`μ: V -> V`... such that for each `1 <= i <= n`

There is some edge `ei ∈ E` where:
- `η(ei) = (μ(xi),μ(yi))`
- `ai ∈ λ(ei)`

We say evaluating `q` over `G` is the `m`-ary relation `[[q]]G ⊆ V^m`
=> `[[q]]G = {(μ(z1),...,μ(zm)) | μ is a mapping for q on G}`

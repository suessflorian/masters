# Conjunctive Regular Path Queries
Seems to be just the squishing together of the last two courses. Essentially;

`q = (z1,...,zm) <- a1(x1,y1),...,an(xn,yn)`, a mapping for `q` on `G` is a function

Gets turned to:

`q = (z1,...,zm) <- α1(x1,y1),...,αn(xn,yn)`, a mapping for `q` on `G` is a function

Where `αi` is in `RPQ`, which suggests that for `(μ(xi),μ(yi)) ∈ [[αi]]G`

It still holds;

The semantics of evaluating `q` over `G` is the `m`-ary relation `[[q]]G⊆V^m` defined as
`[[q]]G = {(μ(z1),...,μ(zm)) | μ is a mapping for q on G}`

intuitively; keep in mind that `μ` is just that special mapping that binds vertices that fit with the expression.

Notes:
Every regular path query can be expressed as a conjunctive regular path query.

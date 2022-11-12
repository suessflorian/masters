# RPQ (regular path queries)
end results are `pairs of vertices`

- `a` in `L` => `a` in `RPQ`
- `e` in `RPQ` => `(e)-` in `RPQ`
- `e` in `RPQ` => `(e)+` in `RPQ` (transitive closure)
- `e`,`f` in `RPQ` => `(e)/(f)` in `RPQ` (concatenation)
- `e`,`f` in `RPQ` => `(e)+(f)` in `RPQ` (union)

parenthesis only for ambiguity reasons

Translates concretely via:

Given some `PGM` = `G = (V, E, η, λ, ν)`
Refresher: 
`η: E -> V X V`
`λ: V U E -> P(L)`
`v: (V U E) x K -> N`

(note: `N` are values, we use `K` keys to access them, `L` are labels)

evaluating an expression `g ∈ RPQ over G` is the set of vertex pairs:
 => `[[g]]G ⊆ V×V`

---

- `g = a ∈ L` 
 => `[[g]]G = {(s,t) | ∃e ∈ E s.t. η(e) = (s,t) ∧ a ∈ λ(e)}`

- `g = (e)− ∈ RPQ` 
 => `[[g]]G = {(t,s)|(s,t) ∈ [[e]]G}`

- `g = (e)+ ∈ RPQ` 
 => `[[g]]G = TC([[e]]G)`, `TC` is transitive closure

- `g = (e)/(f) ∈ RPQ` 
 => `[[g]]G = {(s,t) | ∃u ∈ V s.t. (s,u) ∈ [[e]]G ∧ (u,t) ∈ [[f]]G}`

- `g = (e) + (f) ∈ RPQ` 
 => `[[g]]G = [[e]]G U [[f]]G`

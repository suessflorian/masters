# Language
There's 3 main ontology languages, we're not covering OWL. Only RDF and RDFS. These are all based on `Description Logic`.

## RDF
`RDF facts` is a triple (subject, predicate, object), eg `(:Dupond, :Leads, :CSDept)`. Given a set of RDF facts, you can then go onto represent them in a graph.

We then go towards understanding that a set of facts can in fact via applying RDF semanatics produce more facts. (RDFS).

## RDF Semantics
`<subject P object>` translates to first order logic (FOL) `P(subject, object)`.

### RDFS: RDF Schema
`<TeachesTo rdf:type rdf:Property>` (declaration of relation)
`<pierre rdf:type MasterStudent>` (instance of a class)

Then heirarchy
`<Staff rdf:type rdfs:Class>`
`<AcademicStaff rdfs:subClass Staff>`
`<Professor rdfs:subClass AcademicStaff>`

(this starts producing additional facts on top of a given set of `RDF facts`).

There's also `subProperty`'s like

`<RegisteredTo rdf:type rdfs:Property>`
`<LateRegisteredTo rdfs:subPropertyOf RegisteredTo>`

Declaration of `domain` and `range` restrictions for predicates:
`<RegisteredTo rdfs:domain Student>`
`<RegisteredTo rdfs:range Course>`

---
Although we're not covering OWL, we should know it provides extra logical rules like:
- disjointness
- union
- intersection
- operation between classes
- functional constraints

## Mapping from RDFS to FOL
`<i rdf:type C>`					->			`C(i)`
`<i P j>`									-> 			`P(i,j)`
`<C rdfs:subClassOf D>`		-> 			forAll x where `C(x)` => `D(x)`
`<P rdfs:subProperty R>`	-> 			forAll x,y where `P(x,y)` => `R(x,y)`
`<P rdfs:domain C>`				-> 			forAll x,y where `P(x,y)` => `C(x)`
`<P rdfs:range C>`				-> 			forAll x,y where `P(x,y)` => `C(y)`

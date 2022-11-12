# XPath Expressions
Most important course of 4-9.

## XPath Context (?)
Definitely revise, I think it essentially pre-emptively motivates that xpath expressions are stateful. Where given an operation that encompasses some nodes, you must be evaluating from a particular point.

Revision:
Exactly right, but more concretely we should denote via a tuple, 
`{(N1, N2, ..., Nn), Context}`

Where `Ni` represents a Node, bounded by the `Context` node

## XPath Steps
`axis::node-test[P1][P2]...[Pn]`

**axis** - which direction to walk
**node-test** - indicating the kind of nodes to select
**Pi** - a predicate, any xpath expression evaluated to boolean

And yeah a step is evaluated alongside **context**

## XPath Expressions
`[/]step1/step2/.../stepn`

`/A` selects the root element A

`/descendant::A` selects all elements A
== `descendant-or-self::A`
== `//A`

Begins with `/` means absolute
Begins without means relative

Used to push the context around

Seems like description of examples go backwards, reading right to left.

## Axis
`child` is default, can be ommitted. Couple of funky ones.

### Child
Important: an attribute node has a parent, but an attribute node is not one of the children of it's parent. NEED to use the attribute axis.

### Parent
`..` is abbreviation for `parent::node()`

### Attribute
`attribute::*` (short `@*`)

### Descendant
`descendant::node()`, `descendant::*`, `descendant::text()`
Asterix only refers to element nodes

_Difference between descendant and child axis?_ Perhaps **ALL** in document order vs immediate children **ONLY**.

### Ancestor
`ancestor::node()` and so on similar to `descendant`

### Following
Document order of siblings and their descendants.

Weird looking abbreviations, look to follow directory traversals `..`, including however `//a`.

## Node tests
`node()`, `text()`, `*`, `ns:*`, `ns:toto` (on namespace filtering)

## Predicates
connectives `and`, `or`, negation `not()`
inside square brackets usually `[]`
eg.
`//B[@att1=1]`: nodes B having attribute att1 with value 1
`//B[@att1]`: nodes B having this attribute att1
`//B/descendant::text()[position()=1]`, first text node descendant of each node B
position predicate can be appreviated to `[1]`

Note: keep in mind that tree representations left to right ordering correlates to node appearance top down in a serialized XML form 

## Primitive type
`boolean`, `number`, `string`, `nodeset`, they are naturally coercable to boolean "falsey".

# converting `nodeset` to `string` (REVISE)

### Revision
The abbreviations are quite important to get intimately familiar with:

```
somename  ||  child::somename
.					||	self::node()
..        ||	parent::node()
@someattr ||	attribute::someattr
a//b      ||	a/descendant-or-self::node()/b
//a       ||	/descendant-or-self::node()/a
/         ||	/self::node()
```

The `//` in particular, `descendant-or-self`

`//B[@att1]` == `/descendant-or-self::node()/child::B/attribute::att1`

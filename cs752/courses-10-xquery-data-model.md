# XQuery Data Model

- a `value` is a sequence of 0-n `items`
- an `item` is either a node or an atomic value

Nodes (revision from `XPath`):
- `Document`, the document root
- `Element`
- `Attributes`
- `Text`
- `Comment`
- `ProcessingInstruction`
- `Namespace`

Model is very general, everything is always a `sequence of items`

Note: we call several XML Docs a `collection`

Remarks:
- no distinction between items in a sequence
- sequence cannot contain another sequence
- no such thing as null
- empty sequence exist
- heterogenous items
- sequences are ordered
- nodes have an identity, values do not
- element and attribute have type annotations
- nodes appear in the given order in their document
- attribute order is undefined
- XQuery is case-sensitive
- XQuery builds queries as composition of expressions
- Expressions always output a value, no side-effects
- Xquery comment can be put anywhere `(: This is a comment :)`

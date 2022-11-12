# XPath (foundational to XQuery, XLink) 
Essentially a tree traversal language

- expressions
`2*3`
`//*[@msg="Hello World"]` retrives all elements with certain msg attribute

They use DOM, types of node types
- `Document` (root node)
- `Element` (root element is top level element)
- `Attribute`
- `Text`

Nodes have a name, or a value, or both. Naturally where applicable. ie Text nodes don't have a name.

**Attributes are special**: They are not considered as first-class nodes in an XML tree; They must be addressed specifically when needed




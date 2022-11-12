# XPath Examples

`child::A/descendant::B:`
all B elements that are descendant to A elements child of the context node

`child::*/child::B`
all B elements that are grand children (second level children) from the context node

`descedant-or-self::B`
all B elements that are descendant of the context node, including the context node if it is of element B

`child::B[position()=last()]`
selects the B element that is a child element of the context node AND it also happens to be the last child in document order out of all children of the context node.

NOTE: I interpretted it wrong

`follow-sibling::B[1]`
the first sibling element B (document order) of the context node

and so on.... nothing fancy yet

Note if we prepended `/` in anyof those, it'd "of the document"

Going through Xpath 2.0/3.0, introduces a bunch of features but I imagine it's not really assessable. Loops, sequences, nested expressions.

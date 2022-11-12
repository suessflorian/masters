# Bunch of exercises

`child::A/descendant::B`
== `child::A/descedant-or-self::B`
== `A//B`

`child::*/child::B`
== `*/B`

`descendant-or-self::B`
== `//B`

`child::B[position()=last()]`
== `/B[last()]`

`child::A[child::C]`
== `A[C]`

`/descendant::B[@att1 OR @att2]`
== `//B[@att1 OR @att2]`


```
<a>
	<b><c /></b>
	<b id="3" di="7">
		bli 
		<c />
		<c>
			<e>
				bla
			</e>
		</c>
	</b>
	<d>bou</d>
</a>
```

`//e/preceding::text()`
text node preceding of child element `e` of document root node

Answer:o empty?
`//e/preceding::text()` == ``//child:e/preceding::text()``

**Sum of all attribute values**
`sum(//@*)` == `sum(descendant-or-self::attribute/*)`

**Text content of the document, where every “b” is replaced by a “c”:**
`translate(//text(),'b','c')`
This is an invalid XPath expression, translate takes a single string value as first arg, I returned a node list

Should be: `translate(string(/),'b','c')`

**Name of the child of the last “c” element in the tree:**
`//string(c[last()])`

Should be: `name(//c[last()]/*[1])` (chooses the first child of last "c" element) 

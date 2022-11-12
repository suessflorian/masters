# On XPath and XQuery
```
<?xml version="1.0" encoding="UTF−8"?>
<a>
	<a>
		<a/>
		<b/>
		<b/>
	</a>
	<a>
		<a/>
		<b>
			<a/>
			<a/>
		</b>
	</a>
</a>
```

Tree

```
				 doc
					|
					v
				 <a>
			 |       |
			 v       v
			<a>     <a>
	|   |   |
	v   v   v
 <a> <b> <b>

```

Idk, don't need to finish the diagram, looks good enough. We know what to do

**For each node, write down the pre- and post-identifiers.**
What are pre and post identifiers?!

- Pre: yield the ordering of opening tags, post: yield the ordering of closing tags

**select all a nodes that have a b-parent**
`//a[sum(../b)>0]`, this traverses up to the parent, and then traverses back down to the child.

**select all b nodes that have no preceding b-elements**
`//b[not(preceding::b)]`

**select all b nodes that are leaves**
`//b[not(sum(b/*))]`, recommended was `//b[not(descendant::*)]`

**select all nodes with more than one b-sibling.**
`//*/*[sum() > 1]`

Recommended is: `//∗[(count(preceding-sibling::b)+count(following-sibling::b))>1]`

**what does `//a[2]` do?**
Finds all a nodes that are **second in document order**

**`/a/*[preceding-sibling::a and preceding-sibling::b]`**
all children of root a element that have both precending siblings of element a and b

**`//*[count(a)=count(b)]`**
All elements such that the number of a children is = to the number of b children

**`//*[count(preceding::a)>3]`**
All elements that have at least 3 preceding `a` elements

**//a[not(ancestor::b)] | //b[not(ancestor::a)]**
All `a` elements such that it's ancestor is not B unioned with all `a` elements such that it's ancestor is not A.


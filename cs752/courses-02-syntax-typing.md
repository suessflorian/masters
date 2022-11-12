# XML Syntax
Really nothing crazy here...

- element (could be atomic, or recursive set of elements)
- attributes (unordered, unique)
- prologue (has to be first line, _element root_ `<? ... ?> elements...`)

# Entities
```
<!DOCTYPE a [
	<!ENTITY myName "John Doe">
	<!ENTITY mySignature SYSTEM "signature.xml">
]>

<a>
 My name is &myName;
 &mySignature;
</a>
```

There are a bunch of implicitly defined entities part of skipping mis parsing of XML, to embed these into your text you can use the following: `&lt;`, `&gt;`, `&amp;`, `&apos;`, `&quot;`.

`<!-- This is a documnet -->`

# Processing instructions
`<?xml-stylesheet href="prog.xslt" type="text/xslt"`

# Literal sections
CDATA - Character Data `<![CDATA[........]]>`

For typing; DTD can be specified in the prologue with they keyword `DOCTYPE` using an adhoc syntax.

DTD (document type definition)

_well formed_, conforming to DTD _valid_

Example of DTD

```
<!DOCTYPE email [
	<!ELEMENT email {header, body}>
	<!ELEMENT header {from, to, cc?}>
	<!ELEMENT to {#PCDATA}>
	<!ELEMENT from {#PCDATA}>
	<!ELEMENT body {paragraph*}>
	<!ELEMENT paragraph {#PCDATA}>
]>
```


## Revision

- The first line of the serialized form must always be the prologue if there is one:
`<?xml version="1.0"encoding="utf-8"?>`

- Document content always enclosed in single opening/ending tag, the element root

### Tree form
- A document is a tree with a root node (**Document node** in DOM),
- The root node has one and only one element child (**Element node** in DOM), called the element root
- Each element node is the root of a subtree which represents its structured content

- A DTD may also be specified externally using a URI
`<!DOCTYPE docname SYSTEM "DTD-URI" [local-declarations]>`

- Namespaces `something:label`

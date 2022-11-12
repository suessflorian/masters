# XPath Operators and Functions

- arithmetic operators with `div` and `mod`
- `or`, `and`, `not()`
- `!=`, `=`
- `<`, `<=`, `>=` `>`, only can compare numbers, not strings, if embedded in XML must use `&lt;`
- `|:` union of node sets (eg: `node()|@*`)

## Node functions
- `count($s)`
- `local-name($s)`
- `namespace-uri($s)`
- `name($s)`
- `concat($s1, ...)`
- `starts-with($a, $b)`
- `contains($a, $b)`
- `substring-before($a, $b)`
- `substring-after($a, $b)`
- `substring($a, $b)`
- `string-length($a)`
- `normalize-space($a)`
...

- `not`, `sum`, `floor`, `ceiling`, `round`

### Variables cannot be defined in XPath, they can only be referred to

```
<a>
  |<b>
  |  |<c/>
  |</b>
  |<b id="3" di="7">
  |  |bli
  |  |<c/>
  |  |<c>
  |  |  |<e>
	|	 |  |  |bla
	|	 |	|</e>
  |  |</c>
  |</b>
  |<d>bou</d>
</a>
```

`//c`

```
<a>
  |<b>
  |  |<c/> <!--1-->
  |</b>
  |<b id="3" di="7">
  |  |bli
  |  |<c/> <!--2-->
  |  |<c> <!--3-->
  |  |  |<e>
	|	 |  |  |bla
	|	 |	|</e>
  |  |</c>
  |</b>
  |<d>bou</d>
</a>
```

`//b/node()`

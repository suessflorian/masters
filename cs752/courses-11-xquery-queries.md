# XQuery Queries
Expressions are always evaluated with respect to a `context` (like `XPath`)

It is a slight generalization of `XPath` and `XSLT` it also includes:
```
- Bindings of namespace prefixes with namespace URI's
- Bindings for variables
- In-scope functions
- A set of available collections and a default collection
- Date and time
- Context (current) node
- Position of the context node in the context sequence
- Size of the sequence
```

An expression takes a value, returns a value (closed-form)

Expressions may take several forms
- Path expressions
- Constructors
- FLWOR expressions
- List expressions
- Conditions
- Quantified expressions
- Data types expressions
- Functions

Values are expressions:
- Literals, built values (date), variables, built sequences

An XML document is also an expression (it returns itself)

# Retrieving documents and collections
`doc()`, `collection()`, result is root node of document

### Any XPath expression is a query

```
collection('movies')/movie[@year=2005]/title
```

---------
constructors, interpolate expressions with `{}`
```
<titles>
	{collection('movies')//title}
</titles>
```

`<chapter ref="[(1 to 5, 7, 9)]">` == `<chapter ref="[(1 2 3 4 5 7 9)]">`

`<paper>{$myPaper/@id}</paper>` => `<paper id="271"></paper>`

# Variables
```
<employee empid="{$id}">
	<name>{$name}</name>
</employee>
```

This must be bound values.

# FLWOR expressions
Most powerful expressions in XQuery
- FOR, LET, WHERE, ORDER, RETURN

Basic example:
```
for $m in collection('movies')/movie
	where $m/year >= 2005
	return
	<film>
		{$m/title/text()},
		(director: {$m/director/last_name/text()})
	</film>
```

```
let $year:=1960
for $a in doc('SpiderMan.xml')//actor
where $a/birth_date >=$year
return $a/last_name
```

is equivalent to XPath: `//actor[birth_date>=1960]/last_name`

`//actor[birth_date>=1960]/last_name`
== `/descendant-or-self::actor[child::birth_date >= 1960]/child::last_name`

Only some FLWOR expressions can be rewritten in `XPath`

```
for $p in doc("parts.xml")//part[color = "Red"]
let $o := doc("orders.xml")//order[partno = $p/partno]
where count($o) >= 10
order by count($o) descending
return
<important_red_part>
	{ $p/description }
	<avg_price> {avg($o/price)} </avg_price>
</important_red_part>
```

`for` binds the input of each item in the input sequence (note the sequence can be heterogenous sequences too)
`let` binds the entire sequence

- Note variables given a scope are immutable after declaration.

# Where clause
The difference lies in the much more flexible structure of XML docs

```
for $m in collection("movies")/movie
where $m/director/last_name="Allen"
return $m/title
```

Looks like a SQL query, but predicates are interpreted according to XPATH
- if path does not exist, the result is `false`
- if path expression returns several nodes, the result is `true` if at least one match

# Return is a mandatory field
It is instantiated once for each binding of the variable in the `for` clause

## You can simualte a join
double looping through docs, create a where clause that defines the join

There are some other utilities
- `if-then-else`
- `some` expressions (`satisfies`)
- `every` expressions (`satisfies`)

```
declare namespace my="urn:my";

declare function my:mccarthy91($x as xs:integer)
	as xs:integer
{
	let $result :=
		if ($x>100) then 
			$x - 10
		else
			my:mccarthy91(my:mccarthy91($x + 11))
	return $result
}
```


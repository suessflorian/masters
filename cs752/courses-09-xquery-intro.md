# XQuery Intro
XQuery is an extension of SQL since XML is an extension of the relational model.
- Ofcourse W3C recommends it via querying

## XQuery vs XSLT
XSLT is a procedural language, good at transforming XML docs, whereas XQuery is declarative (more SQL like) hence allows room for highly efficient physical retrievals (room for query optimizer etc...).


## Principles
- **Closed-form evaluation**, XQuery relies on a 'data model', each query maps an insatnce of the model to another instance of the model.
- **Composition**, XQuery relies on expressions, which can be arbitrarily complex
- **Flexible Type awareness**, associate an XSD scheam to query interpretation, note XQuery operates also on schema-free documents
- **XPath compatible** - XPath is a valid XQuery
- **Static Analysis** - type inference, rewriting, optimization (utulize declarative nature)

There is an XQuery algebra :o, similar to how there exists relational algebra.

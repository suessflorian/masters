# Dialects and use cases
Note that the domains define the meaning of XML attributes and elements etc...

- RSS (Describes updates)
- WML (Wireless ML for Wireless Application Protocol, WAP apps)
- XSL-FO (pdf representable)
- MathML (Mathematical ML)
- XLink (XML Linking Language)
- SVG (Scalable Vector Graphics)
- SAX (Simple API for XML)
- DOM (Document Object Model)
- **XPath (Will be studied thoroughly)**
- **XQuery (Will be sudied thoroughly)**
- XSLT (Extensible Stylesheet Language Transformations) (translating XML docs -> XML docs)
- Web services (WDSL)

## DOM
tree-based, object-oriented access to content

## XPATH (generalises DOM)
language describing paths down XML documents

## XLink (XML trees + XLink => graphs)
Linking language, advanced hypertext primitives, insert in XLM descriptions of links to external web resourcese. Simple mono-directional links (HREF). XLink relies on XPath for addressing portions of XML documents.

## XSLT (procedural)
"Perl for XML", based on XPATH expressions, "template" specifies what should be produced. When pattern matched, corresponding template produces data.

## XQuery (declarative)
"SQL for XML" (more general than SQL)
```
FOR $p IN document("bib.xml")//publisher
LET $b := document("bib.xml")//book[publisher = $p]
WHERE count($b) > 100
RETURN $p
```

## Generic XML tools
- API
- Parsers and type checkers
- GUI
- Editors
- XML dif
- XML wiki
- Dev envs for particular XML dialects

### USE CASES
- Publishing, XML to XHTML
- Integration, transform different dialects to common dialect, collection for query
- Distributed Data Processing, consume/produce XML-represented data

_Lots of focus on `generic` approach to domains_

# Publishing
- Using XSLT to transform XML to human visualized form via XHTML
For WAP, XML => WML

# Integration
Via XSLT/XQuery, consume various dialects of XML to build a common dialect among all documents.

# Distrbuted Data Processing
XML encoding as a means to exchange info, WDSL is used to describe the exchange dialect between web services

[Checkout for specifications of XML](http://www.w3.org/XML)

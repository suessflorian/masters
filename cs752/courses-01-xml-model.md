# XML Model
eXtensible Markup Language, essentially a machine friendly way to describe data structure. Contrasted with relational model (being too rigid?)

## Motivation:
Lots of data, coming in all sorts of different forms. "Tremendous potential".

`We need a way make it usable`

1. Being able to describe the data coming in

## Role of XML
Exchange of data based on HTML.
- but falls short to software exploitation

Data exchange priority. (X)HTML is a specialized XML dialenct for data presentation.

# Semi-structured data model
Based on graphs; structure of labels captured by edges, values reside at leaves. **OR** vertcies represent both labels and values. (second based on the document object model (DOM)).

- **self describing (in contrast to relational - seperates schema and content)**
a) association lists (records of label-value pairs)

- **flexible typing (can be typed, not enforced)**
a) naturally extending, values can have their own structure

- **serialized form**
a) allow duplicate labels

*Remarks:* Relational data can be represented, for regular data, representation though starts appearing highly redundant.

### Notice regular vs irregular data

### Nodes can be _identified_ and refferred to later onwards (potentially introducing cycles) when graphing

- WWW Consortium (W3C)


## XML is a syntax, the interpretation of labels etc... is introduced later

## Revision
XML is a simplified version of SGML, a long-term used language for technical documents

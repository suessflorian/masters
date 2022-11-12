# On XML 

**Explain the diff in purpose of HTML and XML**
XML is a semi-structured content describing language that is generic to domain - purely syntax, HTML is an extension of XML that attaches meaning to certain elements and attributes specifically in a way to describe how to display given content.  

Lecturer:
XML - data
HTML - presentation

When XHTML was introduced, it became a full on dialect of XML, meaning that HTML itself is not an extension. Tags (element and attribuets) of dialects now have a pre specified meaning.

**Briefly explain two main application areas of XML**
- Facilitates **integration**, given many different domains described in XML, we can depend on the use of XML to reliably integrate them to a common domain (via XSLT)
- Faciliates **web service communication**. We can use XML as an encoding, used mutually by services as a means to communicate to each other. 

**Name four reasons for the success of XML** 
- Domain generic, applicable in all areas where semi-structuring data has benefit
- Relatively simple
- Human readable
- Tree like

Lecturer:
- The right time
- W3C conforming OS-agnostic etc...

**Name two basic rules that well-formed XML documents must satisfy**
- for every opening element tag there is a closing element tag
- for any element, it's opening and closing tags surround the opening AND closing tags of any of it's children (nested) elements. 

Lecturer: must have exactly one root element

**For each rule, give a simple example that violates this rule**

- `<a>`
- `<a><b></a></b>`


```
<?xml version=“1.0” encoding=“ISO-8859-1” ?>
<?xml-stylesheet href=“headlines.css” type=“text/css” ?>
<invoice>
	<product>Lenovo X201</product>
	<customer>Jack Ryan</customer>
	<amount>NZ$1822</amount>
	<data>30-03-2011</date>
</invoice>
```

**Indicate the major parts of the XML document**

- The prologue, specifies to the decoding mechanism raw decoding details
- Anything after proluge in `<?` are just additional processing instructions
- The document root node, `invoice`

**Name two ways in which DTD can assist XML parsers**
In general if the document is `valid` 
- via describing the ordering of elements
- via describing the existance of attributes

Lecturer:
- all required elements are present
- prevent the presence of undefined elements
- enforce data structure
- specifcies permitted attributes per element

(Note: not XML compliant)

```
<Movies>
	<Movie Year-released=“2009”>
		<Title>The girl with the dragon tattoo</Title>
		<Director>Niels Arden Oplev</Director>
		<Actors>
			<Actor>Noomi Rapace</Actor>
		</Actors>
	</Movie>
	<Movie Year-released=“2009”>
		<Title>The girl who played with fire</Title>
		<Writer>Jonas Frykberg</Writer>
		<Writer>Stieg Larsson</Writer>
		<Actors>
			<Actor>Noomi Rapace</Actor>
			<Actor>Michael Nyqvist</Actor>
		</Actors>
	</Movie>
</Movies>
```

**Write an associated DTD**
```
<? DOCTYPE[
	<?ENTITY Movie = (Title, Director, Actors)>
	<?ENTITY Title = #PCDATA>
	<?ENTITY Director = #PCDATA>
	<?ENTITY Actors = (Actor+)>
	<?ENTITY Actor = #PCDATA>
]>
```

Lecturer:
```
<! DOCTYPE[
	<!ENTITY Movies (Movies+)>
	<!ENTITY Movie (Title, Director?, Actors, Writer*)>
	<!ATTLIST Movie Year-released CDATA #REQUIRED>
	<!ENTITY Title (#PCDATA)>
	<!ENTITY Director (#PCDATA)>
	<!ENTITY Actors (Actor+)>
	<!ENTITY Actor (#PCDATA)>
]>
```

"PCDATA - parse character data"

**Considering that DTS are meant to model typical XML documents, what changes would you make to your original DTD to validate typical XML docs of movie domains**

```
<? DOCTYPE[
	<!ENTITY Movie (Title, Directors, Actors)>
	<!ENTITY Title (#PCDATA)>
	<!ENTITY Directors (Directors+)>
	<!ENTITY Director (#PCDATA)>
	<!ENTITY Actors (Actor+)>
	<!ENTITY Actor (#PCDATA)>
]>
```

And then add a bunch of optional fields like, censor rating etc...except how do I let an unkown and unknown number of occurances of additional complex types be represented in DTD


**Does the following XML document**
```
<enrolment> 
	<student studentID=“s01”/> 
	<class studentIDrefs=“s01 s02”> 
		<title>ELCM XML</title> 
	</class> 
</enrolment> 
```
**conform to the following DTD?**
```
<!ELEMENT enrolment (student+, class)>
<!ELEMENT student EMPTY>
<!ATTLIST student studentID ID #REQUIRED>
<!ELEMENT class (title)>
<!ATTLIST class studentIDrefs IDREFS #REQUIRED>
<!ELEMENT title (#PCDATA)>
```

- The types are weird... `ID` and `IDREFS`, are these dynamically interpretted by the decoder or do they have to be described in the DTD?
- But looks so yes

**Write down a DTD that specifies an element with mixed content**

```
<!ELEMENT student (#ANY)>
<!ATTLIST student #ANY>
```

Is there such thing?

Lecturer

```
<!ELEMENT rootelement (]PCDATA|childelement)*>
<!ELEMENT childelement (]PCDATA)>
```

With matching conforming xml document
```
<rootelement>
PCDATA Content
<childelement>Child element</childelement>
</rootelement>
```

You can actually put all of this together in one XML document via

```
<?xml version=“1.0” standalone=“yes”?>
<!DOCTYPE[
	<!ELEMENT rootelement (]PCDATA|childelement)*>
	<!ELEMENT childelement (]PCDATA)>
]>
<rootelement>
	PCDATA Content
	<childelement>Child element</childelement>
</rootelement>
```

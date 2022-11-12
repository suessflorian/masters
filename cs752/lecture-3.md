# QA session
For courses 1-3 and any admin questions.

- strategic excercise not assessed, should be done in your own time though.
- 3 courses per week, then 2 lectures revising these courses + strategic excercises.
- start working on your topic, milestone create research question, feedback will be giving re: too wide etc...
- first assignment 25th March, 1 week in advanced (18th Mar), strategic excercises help greatly with it.
- no coding excercises for at least the first half of this course
- assignments individual
- XPath, XQuery in first assignment (and final exam). Sentence to XPath/XQuery vice versa
- XML attributes are not ordered, same with `DOCTYPE` element
- 4 assignments
- all deadlines last page in course admin slides (**TODO**)
- use Google for first strategic excercises
- 10hrs a week
- rated highly, practical work for final presentation

# DTD vs XML Schema
Module 2 last slides:
DTD (document type definitions): old style type, still is very much used

There's XML Schema, which is quite expressful. This is why DTD sometimes is used if schema complexity is not that high.

```
<?xml version="1.0"?>
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
	<xs:element name="note">
		<xs:complexType>
			<xs:sequence>
				<xs:element name="to" type="xs:string" minOccurs=’1’ maxOccurs=’1’/>
				<xs:element name="from" type="xs:string"/>
				<xs:element name="heading" type="xs:string"/>
				<xs:element name="body" type="xs:string"/>
			</xs:sequence>
		</xs:complexType>
	</xs:element>
</xs:schema>
```

vs

```
<!ELEMENT note (to, from*, heading, heading, body+)>
<!ELEMENT to (#PCDATA)>
<!ELEMENT from (#PCDATA)>
<!ELEMENT heading (#PCDATA)>
<!ELEMENT body (#PCDATA)>
```

`*` 0 - many
`+` 1 - many

Important: DTD requires a different validation tool. Where XML Schema is XML itself! XML Schema has a superset of functionalities re: schema constraints vs DTD.

`PCDATA` parse character data

- DTD is in the assignments and final exam, "does XML doc conform to DTD".
- open book assignments
- can't be too technical, can't be too broad re: research question


## DEADLINES
Week 4: Assignment 1 due by Friday, 25 March
Week 5: Research question & references for presentation due by Friday, 01 April
Week 6: Assignment 2 due by Friday, 08 April
Break: 15-29 April
Week 7-11: Assignments 3 and 4 due dates tba
Week 10: Team presentation material due by Friday, 20 May

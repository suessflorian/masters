# New Lecturer, new course section
There was an introduction lecture which was largely admin and focused on course outcomes etc... Didn't write notes as I didn't see why we should.

## Semantic Web Introduction
Use Web of Data as CMS, use community for content (? struggling to understand the point). You want data in a web linked together re: relevance. This provides semantics to different sites. A concept should be linked _closely_ to sites that discuss that concept.

# Outline
- semantic web
- reasoning
- ontologies (RDF, RDFS, OWL)

## Representation of Data
Relational vs Graph, super intuitive? Parallel with internet web? Merging graphs.

I think we're motivating knowledge graphs? Common graph that is a composition of various data sources? Looks like the course is perhaps motivating why we will be fixing our attention to graph representations of data (over alternatives) because...

- graph representation is independnent of exact strucutres
- change in local db schema's, XHTML etc... do not effect the whole
- new data can be connected seeminglessly 

> Semantic Web supposedly does all of this?

# Ontologies
Formal description providing human users with a shared understanding of a given domain... controlled vocabulary.

- Purpose to be processed by `machines`
- allows for `logical semantics` empowers machines to `reason`

Goal is to allow `reasoning`, in order to answer queries.

## Classes and class heirarchies
Backbone of ontologies, similar to OOP (like vertices)

### Instances of classes
`AcademicStaff(sebastian)`, refers to `sebastian` being an instance of `AcademicStaff`...

## Relations
Relations with their signature between classes (like edges)

### Instances of a relation
`(sebastian, cs752)` is an instance of `TeachesIn(sebastian, cs752)`.

# Ontology then = Schema + Instance
- `signature` of relations have `constraints` ? (we'll see example later)

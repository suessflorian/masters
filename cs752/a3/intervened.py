import spacy
from typing import Optional
from spacy.tokens import Token, Span

nlp = spacy.load("en_core_web_sm")

# https://universaldependencies.org/u/pos/
INSIGNIFICANT_POS_TAGS = ["ADV", "ADP", "DET", "AUX", "PRON", "SPACE"]

doc = nlp(
    """
Prior to joining University of Auckland in December 2018, Ninh worked in
Copenhagen for 7 years at the University of Copenhagen and IT University of
Copenhagen.  He received his PhD at IT University of Copenhagen under the
supervision of Professor Rasmus Pagh in 2014.  After that, he spent 4 years
in postdoctoral positions in Copenhagen.  He was the recipient of the best
paper awards in WWW Conference 2014 and PKDD 2020.  AMiner has recognized
him as the 2022 AI 2000 Most Influential Scholar Honorable Mention in Data
Mining (Rising Star) for his outstanding and vibrant contributions to this
field between 2012 and 2021.
""".replace(
        "\n", " "
    )
)

ADDED_RELATIONS = ["supervision", "awards", "contributions"]
for token in doc:
    if token.text in ADDED_RELATIONS:
        token.pos_ = "VERB"

entities = [token for token in doc.ents]
relations = [token for token in doc if token.pos_ == "VERB"]


def entityOnLeft(relation: Token) -> Optional[Span]:
    for entity in entities:
        toLeftOf = relation.i - 1
        # skips insignifcant part-of-speech not part of entities
        while (
            doc[toLeftOf].pos_ in INSIGNIFICANT_POS_TAGS
            and not entity.end == toLeftOf + 1
        ):
            toLeftOf -= 1
        if entity.end == toLeftOf + 1:
            return entity


def entityOnRight(relation: Token) -> Optional[Span]:
    toRightOf = relation.i + 1
    for entity in entities:
        toRightOf = relation.i + 1
        # skips insignifcant part-of-speech not part of entities
        while (
            doc[toRightOf].pos_ in INSIGNIFICANT_POS_TAGS
            and not toRightOf == entity.start
        ):
            toRightOf += 1
        if toRightOf == entity.start:
            return entity


# will turn these into legit things soon
discovered_relations: list[tuple[Optional[str], str, Optional[str]]] = []
for relation in relations:
    # skip if not relation is found
    if entityOnLeft(relation) is None and entityOnRight(relation) is None:
        continue
    discovered_relations.append(
        (str(entityOnLeft(relation)), relation.text, str(entityOnRight(relation)))
    )

print("Entities: ", set([token.text for token in entities]))
print("Relations: ", set([token.text for token in relations]))
print("Discovered relations: ", discovered_relations)

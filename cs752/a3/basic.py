from typing import Optional
import nltk

## Uncomment to download required nltk modules, commented to hide noisy stdout
# nltk.download("punkt")
# nltk.download("averaged_perceptron_tagger")
# nltk.download("maxent_ne_chunker")
# nltk.download("words")
# nltk.download("universal_tagset")

# https://universaldependencies.org/u/pos/
INSIGNIFICANT_POS_TAGS = ["ADV", "ADP", "DET", "AUX", "PRON", "SPACE"]

paragraph = """
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

tokens = nltk.word_tokenize(paragraph)
tagged_tokens = nltk.pos_tag(tokens, tagset="universal")

# filter insignificant POS tagged tokens
stripped: list[tuple[str, str]] = [
    tagged_token
    for tagged_token in tagged_tokens
    if tagged_token[1] not in INSIGNIFICANT_POS_TAGS
]

# we want to find patterns noun, verb, noun in order to build relations
# we need a utility to find the positions of verbs
def get_position_of_verbs(stripped: list[tuple[str, str]]) -> list[int]:
    raw_position_of_verbs: list[int] = []
    for index_of, tagged in enumerate(stripped):
        (_, classification) = tagged
        if classification == "VERB":
            raw_position_of_verbs.append(index_of)
    return raw_position_of_verbs


symbols = [classed_symbol[0] for classed_symbol in stripped]

# optional to take into account verbs positioned at start or end of extracted list
discovered_relations: list[tuple[Optional[str], str, Optional[str]]] = []
min_index_of_extracted, max_index_of_extracted = 0, len(stripped) - 1
for pos in get_position_of_verbs(stripped):
    if pos == min_index_of_extracted:
        if stripped[pos + 1][1] == "NOUN":
            discovered_relations.append((None, symbols[pos], symbols[pos + 1]))
        continue
    if pos == max_index_of_extracted:
        if stripped[pos - 1][1] == "NOUN":
            discovered_relations.append((symbols[pos - 1], symbols[pos], None))
        continue
    if stripped[pos - 1][1] == "NOUN" and stripped[pos + 1][1] == "NOUN":
        discovered_relations.append((symbols[pos - 1], symbols[pos], symbols[pos + 1]))

print("Entities: ", set([token[0] for token in stripped if token[1] == "NOUN"]))
print("Relations: ", set([token[0] for token in stripped if token[1] == "VERB"]))
print("Discovered Relationships: ", discovered_relations)

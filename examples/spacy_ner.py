from simple_NER.annotators.spacy_ner import SpacyNER

ner = SpacyNER()
text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
for e in ner.extract_entities(text):
    print(e.value, e.entity_type)
    """
    Sebastian Thrun PERSON
    Google FAC
    2007 DATE
    """
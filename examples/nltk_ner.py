from simple_NER.annotators.nltk_ner import NltkNER

ner = NltkNER()
text = """The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world"."""
for r in ner.extract_entities(text):
    print(r.value, r.entity_type)
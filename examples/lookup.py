from simple_NER import SimpleNER

ner = SimpleNER()
ner.add_entity_examples("person", ["bob", "jon", "amy", "kevin"])

assert ner.is_match("jon is ugly", "person")
assert not ner.is_match("i like pizza", "person")

for ent in ner.entity_lookup("where is Kevin", as_json=True):
    assert ent == {'confidence': 1,
                   'data': {},
                   'end': 14,
                   'entity_type': 'person',
                   'rules': [],
                   'source_text': 'where is Kevin',
                   'start': 9,
                   'value': 'kevin'}

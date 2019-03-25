from simple_NER.rules.neural import NeuralNER

ner = NeuralNER()
ner.add_rule("name", "my name is {person}")

for ent in ner.extract_entities("the name is jarbas"):
    assert ent.as_json() == {'confidence': 0.5251495787186434,
                             'data': {},
                             'end': 18,
                             'entity_type': 'person',
                             'rules': [{'name': 'name',
                                        'rules': ['my name is {person}']}],
                             'source_text': 'the name is jarbas',
                             'start': 12,
                             'value': 'jarbas'}

for ent in ner.extract_entities("name is kevin"):
    assert ent.as_json() == {'confidence': 0.8363423970007801,
                             'data': {},
                             'end': 13,
                             'entity_type': 'person',
                             'rules': [{'name': 'name',
                                        'rules': ['my name is {person}']}],
                             'source_text': 'name is kevin',
                             'start': 8,
                             'value': 'kevin'}

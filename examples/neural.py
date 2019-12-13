from simple_NER.rules.neural import NeuralNER

ner = NeuralNER()
ner.add_rule("name", "my name is {person}")

for ent in ner.extract_entities("the name is jarbas"):
    assert ent.as_json()["value"] == 'jarbas'

for ent in ner.extract_entities("name is kevin"):
    # {'confidence': 0.8363423970007801,
    #                              'data': {},
    #                              'entity_type': 'person',
    #                              'rules': [{'name': 'name',
    #                                         'rules': ['my name is {person}']}],
    #                              'source_text': 'name is kevin',
    #                              'spans': [(8, 13)],
    #                              'value': 'kevin'}
    assert ent.as_json()["value"] == 'kevin'

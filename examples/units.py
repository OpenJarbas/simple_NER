from simple_NER.annotators.units import UnitsNER

ner = UnitsNER()
for r in ner.extract_entities("The LHC smashes proton beams at 12.8–13.0 TeV"):
    assert r.data_value == 12.9
    print(
        r.unit.entity_type
    )
    print(r.value)
    assert r.as_json() == \
           {'confidence': 1,
            'data': {'lang': 'en_US',
                     'span': (32, 45),
                     'spoken': 'The LHC smashes proton beams at twelve point nine '
                               'teraelectron volts',
                     'surface': '12.8–13.0 TeV',
                     'uncertainty': 0.09999999999999964,
                     'unit': {'currency_code': None,
                              'dimensions': [
                                  {'base': 'teraelectronvolt', 'power': 1}],
                              'entity': {
                                  'dimensions': [{'base': 'force', 'power': 1},
                                                 {'base': 'length',
                                                  'power': 1}],
                                  'name': 'energy',
                                  'uri': 'Energy'},
                              'lang': 'en_US',
                              'name': 'teraelectronvolt',
                              'original_dimensions': [
                                  {'base': 'teraelectronvolt',
                                   'power': 1,
                                   'surface': 'TeV'}],
                              'surfaces': ['teraelectron volt',
                                           'teraelectronvolt',
                                           'teraelectron-volt'],
                              'symbols': ['TeV'],
                              'uri': 'Electronvolt'},
                     'value': 12.9},
            'end': 45,
            'entity_type': 'Energy:Electronvolt',
            'rules': [],
            'source_text': 'The LHC smashes proton beams at 12.8–13.0 TeV',
            'start': 32,
            'value': '12.8–13.0 TeV'}

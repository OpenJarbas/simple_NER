from simple_NER.annotators.units import UnitsNER

ner = UnitsNER()
for r in ner.extract_entities("The LHC smashes proton beams at 12.8–13.0 TeV"):
    assert r.data_value == 12.9
    assert r.unit.name == "teraelectronvolt"
    assert r.value == "12.8–13.0 TeV"
    assert r.as_json() == \
           {'confidence': 1,
            'data': {'lang': 'en_US',
                     'spoken': 'twelve point nine teraelectron volts',
                     'uncertainty': 0.09999999999999964,
                     'unit': {'dimensions': [
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
            'entity_type': 'Energy:Electronvolt',
            'rules': [],
            'source_text': 'The LHC smashes proton beams at 12.8–13.0 TeV',
            'spans': [(32, 45)],
            'value': '12.8–13.0 TeV'}

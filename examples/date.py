from simple_NER.annotators.date import DateTimeNER

ner = DateTimeNER()
for r in ner.extract_entities("meeting tomorrow morning"):
    assert r.value == 'tomorrow morning'

for r in ner.extract_entities("my birthday is on december 5th"):
    assert r.value == 'on december 5th'
    assert r.name == "date"

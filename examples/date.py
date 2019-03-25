from simple_NER.annotators.date import DateTimeNER

ner = DateTimeNER()
for r in ner.extract_entities("meeting tomorrow morning"):
    assert r.value == 'tomorrow morning'
    print(r.iso_format)  # 2019-03-26T08:00:00+00:00
    print(r.timestamp)  # 1553587200.0

for r in ner.extract_entities("my birthday is on december 5th"):
    assert r.value == 'on december 5th'
    assert r.entity_type == "date"

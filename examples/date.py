from simple_NER.annotators.date import DateTimeNER

from datetime import datetime
# if not provided used datetime.now()
reference_date = datetime(2010, 5, 13)

ner = DateTimeNER(anchor_date=reference_date)

for r in ner.extract_entities("meeting tomorrow morning"):
    assert r.value == 'tomorrow morning'
    assert r.iso_format == "2010-05-14T08:00:00"
    assert r.timestamp == 1273820400.0

for r in ner.extract_entities("my birthday is on december 5th"):
    assert r.value == 'on december 5th'
    assert r.entity_type == "date"

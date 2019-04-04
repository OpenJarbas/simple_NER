from simple_NER.annotators.date import DateTimeNER

ner = DateTimeNER()

for r in ner.extract_entities("my birthday is on december 5th"):
    assert r.value == 'on december 5th'
    assert r.entity_type == "date"
    print(r.value)
    print("day:", r.day, "month:", r.month, "year:", r.year, "hour:", r.hour)

for r in ner.extract_entities("entries are due by January 4th, 2017 at "
                              "8:00pm, created 01/15/2005 by ACME Inc. and "
                              "associates."):
    print(r.value)
    print("day:", r.day,"month:", r.month, "year:", r.year, "hour:", r.hour)
    print("__")
    """
    due by January 4th, 2017 at 8:00pm,
    day: 4 month: 1 year: 2017 hour: 20
    __
    01/15/2005 by
    day: 15 month: 1 year: 2005 hour: 0
    __
    """

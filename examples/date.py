from simple_NER.annotators.date import DateTimeNER

ner = DateTimeNER()

for r in ner.extract_entities("my birthday is on december 5th"):
    assert r.value == 'on december 5th'
    assert r.entity_type == "date"
    print(r.value)
    print("day:", r.day, "month:", r.month, "year:", r.year)
    """
    on december 5th
    day: 5 month: 12 year: 2019
    """

for r in ner.extract_entities("entries are due by January 4th, 2017 at "
                              "8:30pm, created 01/15/2005 by ACME Inc. and "
                              "associates."):
    print("__")
    print(r.value)
    print("day:", r.day,"month:", r.month, "year:", r.year, "hour:", r.hour,
          "minute:", r.minute)
    """
    __
    January 4th, 2017 at 8:30pm
    day: 4 month: 1 year: 2017 hour: 20 minute: 30
    __
    01/15/2005
    day: 15 month: 1 year: 2005 hour: 0 minute: 0
    """

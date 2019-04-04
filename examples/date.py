from simple_NER.annotators.date import DateTimeNER

ner = DateTimeNER()

for r in ner.extract_entities("The movie is one hour, fifty seven and a half minutes long"):
    assert r.value == 'one hour, fifty seven and a half minutes'
    assert r.entity_type == "duration"
    assert r.total_seconds == 7050
    """
    {'confidence': 1,
     'data': {'days': 0,
              'microseconds': 0,
              'seconds': 7050,
              'spoken': 'one hour fifty seven minutes thirty seconds',
              'total_seconds': 7050.0},
     'entity_type': 'duration',
     'rules': [],
     'source_text': 'The movie is one hour, fifty seven and a half minutes long',
     'spans': [(13, 53)],
     'value': 'one hour, fifty seven and a half minutes'}
    """

for r in ner.extract_entities("my birthday is on december 5th"):
    assert r.value == 'december 5'
    assert r.entity_type == "relative_date"
    print("__")
    print("day:", r.day, "month:", r.month, "year:", r.year)
    """
    december 5th
    day: 5 month: 12 year: 2019
    """

for r in ner.extract_entities("entries are due by January 4th, 2017 at 8:30pm"):
    print("__")
    print(r.value)
    assert r.entity_type == "relative_date"
    print("day:", r.day,"month:", r.month, "year:", r.year, "hour:", r.hour,
          "minute:", r.minute)
    """
    __
    January 4th, 2017 at 8:30pm
    day: 4 month: 1 year: 2017 hour: 20 minute: 30

    """

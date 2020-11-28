from simple_NER.annotators.datetime_ner import DateTimeNER
ner = DateTimeNER()

for r in ner.extract_entities("The movie is one hour, fifty seven and a half minutes long"):
    assert r.value == '1 hour, 57.5 minutes'
    if r.entity_type == "duration":
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
    else:
        assert r.entity_type == "relative_date"
        """
        {'confidence': 1,
         'data': {'day': 29,
                  'hour': 1,
                  'isoformat': '2020-11-29T01:44:29',
                  'minute': 44,
                  'month': 11,
                  'spoken': 'tomorrow',
                  'timestamp': 1606614269.0,
                  'weekday': 7,
                  'year': 2020},
         'entity_type': 'relative_date',
         'rules': [],
         'source_text': 'the movie is 1 hour, 57.5 minutes long',
         'spans': [(13, 33)],
         'value': '1 hour, 57.5 minutes'}
        """

for r in ner.extract_entities("my birthday is on december 5th"):
    assert r.entity_type == "relative_date"
    print("day:", r.day, "month:", r.month, "year:", r.year)
    """
    day: 5 month: 12 year: 2019
    """

for r in ner.extract_entities("entries are due by January 4th, 2017 at 8:30pm"):
    assert r.entity_type == "relative_date"
    print("day:", r.day,"month:", r.month, "year:", r.year, "hour:", r.hour,
          "minute:", r.minute)
    """
    day: 4 month: 1 year: 2017 hour: 20 minute: 30
    """

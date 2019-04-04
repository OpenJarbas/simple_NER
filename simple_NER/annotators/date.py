from simple_NER.annotators import NERWrapper
from simple_NER import Entity
from dateparser.search import search_dates


class DateTimeNER(NERWrapper):
    def __init__(self, anchor_date=None):
        super().__init__()
        self.add_detector(self.annotate)

    def annotate(self, text):

        matches = search_dates(text)
        for value, date in matches:
            data = {
                "timestamp": date.timestamp(),
                "isoformat": date.isoformat(),
                "weekday": date.isoweekday(),
                "month": date.month,
                "day": date.day,
                "hour": date.hour,
                "minute": date.minute,
                "year": date.year
            }
            yield Entity(value, "date", source_text=text, data=data)

    def _old_annotate(self, text):
        # deprecated
        import datefinder
        matches = datefinder.find_dates(text, index=True)
        for date, span in matches:
            value = text[span[0]:span[1]].strip()
            data = {
                "timestamp": date.timestamp(),
                "isoformat": date.isoformat(),
                "weekday": date.isoweekday(),
                "month": date.month,
                "day": date.day,
                "hour": date.hour,
                "minute": date.minute,
                "year": date.year
            }
            yield Entity(value, "date", source_text=text, data=data)


if __name__ == "__main__":
    from pprint import pprint

    ner = DateTimeNER()
    for r in ner.extract_entities("my birthday is on december 5th"):
        pprint(r.as_json())

    """
    {'confidence': 1,
     'data': {'isoformat': '2019-04-04T04:53:27.656766',
              'timestamp': 1554350007.656766,
              'weekday': 4},
     'entity_type': 'date',
     'rules': [],
     'source_text': 'my birthday is on december 5th',
     'spans': [(14, 30)],
     'value': ' on december 5th'}
    """

from simple_NER.annotators import NERWrapper
from simple_NER import Entity
from simple_NER.annotators.utils.parse_en import extract_datetime_en


class DateTimeNER(NERWrapper):
    def __init__(self, anchor_date=None):
        super().__init__()
        self.add_detector(self.annotate)
        self.anchor_date = anchor_date

    def annotate(self, text):
        date, remainder = extract_datetime_en(text, dateNow=self.anchor_date)
        date_str = text.replace(remainder, "").strip()
        if date_str and date_str != text:
            data = {"iso_format": date.isoformat(), "timestamp": date.timestamp()}
            yield Entity(date_str, "date", source_text=text, data=data)


if __name__ == "__main__":
    from pprint import pprint

    ner = DateTimeNER()
    for r in ner.extract_entities("my birthday is on december 5th"):
        pprint(r.as_json())

    """
    {'confidence': 1,
     'data': {'iso_format': '2019-12-05T03:06:00+00:00', 'timestamp': 1575515160.0},
     'end': 30,
     'entity_type': 'date',
     'rules': [],
     'source_text': 'my birthday is on december 5th',
     'start': 14,
     'value': ' on december 5th'}
    """

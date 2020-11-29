from simple_NER.annotators import NERWrapper
from simple_NER import Entity

from datetime import datetime
from lingua_franca.parse import extract_datetime, extract_duration
from lingua_franca.lang.parse_en import _convert_words_to_numbers_en
from lingua_franca.format import nice_duration, nice_date
from lingua_franca import load_language
from simple_NER.utils.diff import TextDiff
from simple_NER.utils.log import LOG

load_language("en")


class DateTimeNER(NERWrapper):
    def __init__(self, anchor_date=None):
        super().__init__()
        self.anchor_date = anchor_date or datetime.now()
        self.add_detector(self.annotate_datetime)

    def annotate_datetime(self, text):
        # TODO don't convert to numbers... value mismatch with original string
        # spans will fail
        conv = _convert_words_to_numbers_en(text)
        if conv != text:
            LOG.debug("WARNING - text was normalized to: {t}".format(t=conv))
        dt = extract_datetime(conv, self.anchor_date)
        if dt:
            date, remainder = dt
            d = TextDiff(conv, remainder)
            for tag, span1, span2 in d.dif_tags():
                value = " ".join(conv.split()[span1[0]:span1[1]])
                # HACK for multiple dates
                date = extract_datetime(value, self.anchor_date)
                if date:
                    date = date[0]
                    data = {
                        "timestamp": date.timestamp(),
                        "isoformat": date.isoformat(),
                        "weekday": date.isoweekday(),
                        "month": date.month,
                        "day": date.day,
                        "hour": date.hour,
                        "minute": date.minute,
                        "year": date.year,
                        "spoken": nice_date(date, now=self.anchor_date)
                    }
                    yield Entity(value, "relative_date", source_text=conv,
                                 data=data)


class TimedeltaNER(NERWrapper):
    def __init__(self, anchor_date=None):
        super().__init__()
        self.anchor_date = anchor_date or datetime.now()
        self.add_detector(self.annotate_duration)

    def annotate_duration(self, text):
        # TODO don't convert to numbers... value mismatch with original string
        # spans will fail
        conv = _convert_words_to_numbers_en(text)
        if conv != text:
            LOG.debug("WARNING - text was normalized to: {t}".format(t=conv))
        delta, remainder = extract_duration(text)
        if delta:
            d = TextDiff(conv, remainder)
            for tag, span1, span2 in d.dif_tags():
                value = " ".join(conv.split()[span1[0]:span1[1]])
                # HACK for multiple durations
                delta, _ = extract_duration(value)
                data = {
                    "days": delta.days,
                    "seconds": delta.seconds,
                    "microseconds": delta.microseconds,
                    "total_seconds": delta.total_seconds(),
                    "spoken": nice_duration(delta).strip()
                }
                yield Entity(value, "duration", source_text=conv, data=data)


if __name__ == "__main__":
    from pprint import pprint

    ner = DateTimeNER()
    for r in ner.extract_entities(
            "tomorrow is X yesterday was Y in 10 days it will be Z"):
        pprint(r.as_json())
        """
        {'confidence': 1,
         'data': {'day': 29,
                  'hour': 0,
                  'isoformat': '2020-11-29T00:00:00',
                  'minute': 0,
                  'month': 11,
                  'spoken': 'tomorrow',
                  'timestamp': 1606608000.0,
                  'weekday': 7,
                  'year': 2020},
         'entity_type': 'relative_date',
         'rules': [],
         'source_text': 'tomorrow is x yesterday was y in 10 days it will be z',
         'spans': [(0, 8)],
         'value': 'tomorrow'}
        {'confidence': 1,
         'data': {'day': 27,
                  'hour': 0,
                  'isoformat': '2020-11-27T00:00:00',
                  'minute': 0,
                  'month': 11,
                  'spoken': 'yesterday',
                  'timestamp': 1606435200.0,
                  'weekday': 5,
                  'year': 2020},
         'entity_type': 'relative_date',
         'rules': [],
         'source_text': 'tomorrow is x yesterday was y in 10 days it will be z',
         'spans': [(14, 23)],
         'value': 'yesterday'}
        {'confidence': 1,
         'data': {'day': 8,
                  'hour': 0,
                  'isoformat': '2020-12-08T00:00:00',
                  'minute': 0,
                  'month': 12,
                  'spoken': 'tuesday, december eighth',
                  'timestamp': 1607385600.0,
                  'weekday': 2,
                  'year': 2020},
         'entity_type': 'relative_date',
         'rules': [],
         'source_text': 'tomorrow is x yesterday was y in 10 days it will be z',
         'spans': [(30, 40)],
         'value': 'in 10 days'}
        """

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

    ner = TimedeltaNER()
    for r in ner.extract_entities(
            "5 minutes ago was X 10 minutes from now is Y in 19 hours will "
            "be N"):
        pprint(r.as_json())
        """
        {'confidence': 1,
         'data': {'days': 0,
                  'microseconds': 0,
                  'seconds': 300,
                  'spoken': 'five minutes',
                  'total_seconds': 300.0},
         'entity_type': 'duration',
         'rules': [],
         'source_text': '5 minutes ago was x 10 minutes from now is y in 19 hours will '
                        'be n',
         'spans': [(0, 9)],
         'value': '5 minutes'}
        {'confidence': 1,
         'data': {'days': 0,
                  'microseconds': 0,
                  'seconds': 600,
                  'spoken': 'ten minutes',
                  'total_seconds': 600.0},
         'entity_type': 'duration',
         'rules': [],
         'source_text': '5 minutes ago was x 10 minutes from now is y in 19 hours will '
                        'be n',
         'spans': [(20, 30)],
         'value': '10 minutes'}
        {'confidence': 1,
         'data': {'days': 0,
                  'microseconds': 0,
                  'seconds': 68400,
                  'spoken': 'nineteen hours',
                  'total_seconds': 68400.0},
         'entity_type': 'duration',
         'rules': [],
         'source_text': '5 minutes ago was x 10 minutes from now is y in 19 hours will '
                        'be n',
         'spans': [(48, 56)],
         'value': '19 hours'}
        """

    for r in ner.extract_entities("What President served for five years six months 2 days"):
        pprint(r.as_json())
    """
    {'confidence': 1,
     'data': {'days': 2007,
              'microseconds': 0,
              'seconds': 0,
              'spoken': 'two thousand, seven days ',
              'total_seconds': 173404800.0},
     'entity_type': 'duration',
     'rules': [],
     'source_text': 'What President served for five years , six months and 2 days '
                    '?',
     'spans': [(26, 60)],
     'value': 'five years , six months and 2 days'}
    """

    for r in ner.extract_entities("starts in 5 minutes"):
        pprint(r.as_json())
    """
    {'confidence': 1,
     'data': {'days': 0,
              'microseconds': 0,
              'seconds': 300,
              'spoken': 'five minutes',
              'total_seconds': 300.0},
     'entity_type': 'duration',
     'rules': [],
     'source_text': 'starts in 5 minutes',
     'spans': [(10, 19)],
     'value': '5 minutes'}
    """

    for r in ner.extract_entities("starts in five minutes"):
        pprint(r.as_json())
    """
    {'confidence': 1,
     'data': {'days': 0,
              'microseconds': 0,
              'seconds': 300,
              'spoken': 'five minutes',
              'total_seconds': 300.0},
     'entity_type': 'duration',
     'rules': [],
     'source_text': 'starts in 5 minutes',
     'spans': [(10, 19)],
     'value': '5 minutes'}
    """



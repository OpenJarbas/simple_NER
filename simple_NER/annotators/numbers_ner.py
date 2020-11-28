from simple_NER.annotators import NERWrapper
from simple_NER import Entity
from lingua_franca.lang.parse_en import _convert_words_to_numbers_en
from lingua_franca import load_language
from simple_NER.utils.diff import TextDiff

load_language("en")


class NumberNER(NERWrapper):
    def __init__(self, ordinals=True, short_scale=True):
        super().__init__()
        self.ordinals = ordinals
        self.short_scale = short_scale
        self.add_detector(self.annotate_written_numbers)

    def annotate_written_numbers(self, text):
        if text.lower() != text:
            text = text.lower()
            print("WARNING - text was normalized to: {t}".format(t=text))

        replaced = _convert_words_to_numbers_en(text,
                                                short_scale=self.short_scale,
                                                ordinals=self.ordinals)
        d = TextDiff(text, replaced)
        for tag, span1, span2 in d.dif_tags():
            value = " ".join(text.split()[span1[0]:span1[1]])
            n = " ".join(replaced.split()[span2[0]:span2[1]])
            data = {
                "number": n
            }
            yield Entity(value, "written_number", source_text=text, data=data)


if __name__ == "__main__":
    from pprint import pprint

    ner = NumberNER()
    for r in ner.extract_entities(
            "three hundred trillion tons of spinning metal"):
        pprint(r.as_json())
        """
        {'confidence': 1,
         'data': {'number': '300000000000000.0'},
         'entity_type': 'written_number',
         'rules': [],
         'source_text': 'three hundred trillion tons of spinning metal',
         'spans': [(0, 22)],
         'value': 'three hundred trillion'}
        """

    ner = NumberNER(short_scale=False)
    for r in ner.extract_entities(
            "three hundred trillion tons of spinning metal"):
        pprint(r.as_json())
        """
       {'confidence': 1,
         'data': {'number': '3e+20'},
         'entity_type': 'written_number',
         'rules': [],
         'source_text': 'three hundred trillion tons of spinning metal',
         'spans': [(0, 22)],
         'value': 'three hundred trillion'}
        """

    ner = NumberNER()
    for r in ner.extract_entities(
            "the 5th number of the third thing"):
        pprint(r.as_json())
        """
       {'confidence': 1,
         'data': {'number': '5'},
         'entity_type': 'written_number',
         'rules': [],
         'source_text': 'the 5th number of the third thing',
         'spans': [(4, 7)],
         'value': '5th'}
        {'confidence': 1,
         'data': {'number': '3'},
         'entity_type': 'written_number',
         'rules': [],
         'source_text': 'the 5th number of the third thing',
         'spans': [(22, 27)],
         'value': 'third'}
        """

    ner = NumberNER(ordinals=False)
    for r in ner.extract_entities(
            "the 5th number of the third thing"):
        pprint(r.as_json())
        """
       {'confidence': 1,
         'data': {'number': '5'},
         'entity_type': 'written_number',
         'rules': [],
         'source_text': 'the 5th number of the third thing',
         'spans': [(4, 7)],
         'value': '5th'}
        {'confidence': 1,
         'data': {'number': '0.3333333333333333'},
         'entity_type': 'written_number',
         'rules': [],
         'source_text': 'the 5th number of the third thing',
         'spans': [(22, 27)],
         'value': 'third'}
        """


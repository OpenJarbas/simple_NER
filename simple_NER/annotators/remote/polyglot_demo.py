from simple_NER.annotators import NERWrapper
from simple_NER import Entity

import requests


def polyglot_NER(text):
    # DO NOT ABUSE THIS, dev purposes only
    # TODO improve this,
    # entities spanning more than 1 token are incorrectly handled
    data = {"text": text.replace(" ", "+"),
            "langs": "en",
            "tokenization": "tokenization",
            "min_O": 0.00
            }
    url = "https://entityextractor.appspot.com/ner"
    r = requests.post(url, data=data)

    t = r.text.replace("<br>", "")
    NER = []
    # parse colors
    candidates = [c for c in t.split("</font>") if
                  not c.startswith('<font color="black">')]
    for c in candidates:
        if not c:
            continue
        color, name = c.split(">")
        color = color.replace('<font color="', "").replace('"', "")
        name = name.strip()
        if color == "red":
            NER.append((name, "person"))
        elif color == "green":
            NER.append((name, "organization"))
        elif color == "blue":
            NER.append((name, "location"))
    return NER


class PolyglotNERdemo(NERWrapper):
    def __init__(self):
        super().__init__()
        self.add_detector(self.annotate)

    def annotate(self, text):
        for e in polyglot_NER(text):
            yield Entity(e[0], e[1], source_text=text)


if __name__ == "__main__":
    ner = PolyglotNERdemo()
    text = """The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world"."""
    ents = [r for r in ner.extract_entities(text)]
    assert ents[0].as_json() == {'confidence': 1,
                                 'data': {},
                                 'entity_type': 'person',
                                 'rules': [],
                                 'source_text': 'The Israeli Prime Minister Benjamin Netanyahu has warned that '
                                                'Iran poses a "threat to the entire world".',
                                 'spans': [(27, 35)],
                                 'value': 'Benjamin'}
    assert ents[2].as_json() == {'confidence': 1,
                                 'data': {},
                                 'entity_type': 'location',
                                 'rules': [],
                                 'source_text': 'The Israeli Prime Minister Benjamin Netanyahu has warned that '
                                                'Iran poses a "threat to the entire world".',
                                 'spans': [(62, 66)],
                                 'value': 'Iran'}

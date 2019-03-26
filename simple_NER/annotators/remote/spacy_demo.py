from simple_NER.annotators import NERWrapper
from simple_NER import Entity

import requests


def spacy_NER(text):
    data = {"model": "en_core_web_lg", "text": text}
    r = requests.post("https://api.explosion.ai/displacy/ent", data)
    return r.json()


class SpacyNERdemo(NERWrapper):
    def __init__(self):
        super().__init__()
        self.add_detector(self.annotate)

    def annotate(self, text):
        for e in spacy_NER(text):
            val = text[e["start"]:e["end"]]
            yield Entity(val, e["label"], source_text=text)


if __name__ == "__main__":
    ner = SpacyNERdemo()
    for r in ner.extract_entities("elon musk works in spaceX"):
        assert r.as_json() == {'confidence': 1,
                               'data': {},
                               'entity_type': 'ORG',
                               'rules': [],
                               'source_text': 'elon musk works in spaceX',
                               'spans': [(19, 25)],
                               'value': 'spaceX'}

from simple_NER.annotators import NERWrapper
from simple_NER import Entity

import requests


def allen_NER(text, host):
    url = host + "named-entity-recognition"
    data = {"sentence": text}
    return requests.post(url, json=data).json()


class AllenNlpNER(NERWrapper):
    def __init__(self, host="http://demo.allennlp.org/predict/"):
        super().__init__()
        self.host = host
        self.add_detector(self.annotate)

    def annotate(self, text):
        res = allen_NER(text, self.host)
        tags = res["tags"]
        words = res["words"]
        for idx, tag in enumerate(tags):
            if tag != 'O':
                yield Entity(words[idx], tag, source_text=text)


if __name__ == "__main__":
    ner = AllenNlpNER()
    ents = [r for r in
            ner.extract_entities("Lisbon is the capital of Portugal")]
    assert ents[0].as_json() == {'confidence': 1,
                                 'data': {},
                                 'entity_type': 'U-LOC',
                                 'rules': [],
                                 'source_text': 'Lisbon is the capital of Portugal',
                                 'spans': [(0, 6)],
                                 'value': 'Lisbon'}
    assert ents[1].as_json() == {'confidence': 1,
                                 'data': {},
                                 'entity_type': 'U-LOC',
                                 'rules': [],
                                 'source_text': 'Lisbon is the capital of Portugal',
                                 'spans': [(25, 33)],
                                 'value': 'Portugal'}

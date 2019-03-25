from simple_NER import SimpleNER


class NERWrapper(SimpleNER):
    def __init__(self):
        super().__init__()
        self._detectors = []

    def add_detector(self, parser):
        self._detectors.append(parser)

    def extract_entities(self, text, as_json=False):
        for parser in self._detectors:
            for e in parser(text):
                if as_json:
                    yield e.as_json()
                else:
                    yield e
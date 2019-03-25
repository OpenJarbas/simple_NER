from simple_NER.annotators import NERWrapper
from simple_NER import Entity

try:
    import spotlight
except ImportError:
    print("you need to install pyspotlight")
    print("pip install pyspotlight")
    raise


class SpotlightNER(NERWrapper):
    def __init__(self, host='http://api.dbpedia-spotlight.org/en/annotate',
                 confidence=0.4, support=20):
        super().__init__()
        self.host = host
        self.confidence = confidence
        self.support = support
        self.add_detector(self.annotate)

    def annotate(self, text):
        for e in spotlight.annotate(self.host, text,
                                    confidence=self.confidence,
                                    support=self.support):
            for e_type in e["types"].split(","):
                if e_type.startswith("DBpedia:"):
                    yield Entity(e["surfaceForm"], e_type.split(":")[-1],
                                 source_text=text,
                                 data={
                                     "uri": e["URI"],
                                     "support": e["support"],
                                     "offset": e["offset"],
                                     "percentageOfSecondRank": e[
                                         "percentageOfSecondRank"],
                                     "similarityScore": e["similarityScore"],
                                     "types": e["types"].split(",")},
                                 confidence=e["similarityScore"])


if __name__ == "__main__":
    ner = SpotlightNER()
    for r in ner.extract_entities("elon musk works in spaceX"):
        print(r.value, r.entity_type)

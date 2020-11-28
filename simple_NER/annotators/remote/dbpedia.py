from simple_NER.annotators import NERWrapper
from simple_NER import Entity
import requests


class SpotlightNER(NERWrapper):
    def __init__(self, host='http://api.dbpedia-spotlight.org/en/annotate',
                 confidence=0.5, support=0, spotter="Default",
                 disambiguator="Default", policy="whitelist"):
        super().__init__()
        self.host = host
        self.confidence = confidence
        self.support = support
        self.spotter = spotter
        self.policy = policy
        self.disambiguator=disambiguator
        self.add_detector(self.annotate)

    def annotate(self, text):
        r = requests.get(self.host, params={
            "text": text,
            "confidence": self.confidence,
            "support": self.support,
            "spotter": self.spotter,
            "disambiguator": self.disambiguator,
            "policy": self.policy

        }, headers={"Accept": "application/json"}).json()
        for e in r["Resources"]:
            for e_type in e["@types"].split(","):
                if e_type:
                    yield Entity(e["@surfaceForm"], e_type,
                                 source_text=text,
                                 data={
                                     "uri": e["@URI"],
                                     "support": e["@support"],
                                     "offset": e["@offset"],
                                     "percentageOfSecondRank": e[
                                         "@percentageOfSecondRank"],
                                     "similarityScore": e["@similarityScore"],
                                     "types": e["@types"].split(",")},
                                 confidence=e["@similarityScore"])


if __name__ == "__main__":
    ner = SpotlightNER()
    for r in ner.extract_entities("Elon Musk works in spaceX"):
        print(r.value, r.entity_type)

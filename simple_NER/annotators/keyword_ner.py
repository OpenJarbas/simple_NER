from simple_NER.annotators import NERWrapper
from simple_NER import Entity
from RAKEkeywords import Rake


class KeywordNER(NERWrapper):
    def __init__(self, lang="en"):
        super().__init__()
        self.add_detector(self.annotate)
        self.lang = lang
        self.rake = Rake(lang=self.lang)

    def annotate(self, text):
        results = self.rake.extract_keywords(text)
        total = sum(x[1] for x in results)
        for x in results:
            confidence = x[1] / total
            data = {"score": x[1]}
            yield Entity(x[0],
                         "keyword",
                         confidence=confidence,
                         source_text=text,
                         data=data)


if __name__ == "__main__":
    from pprint import pprint

    ner = KeywordNER()
    text = """The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world"."""
    for r in ner.extract_entities(text):
        #print(r.value, r.score)
        pprint(r.as_json())
        """
        Israeli GPE
        Benjamin Netanyahu PERSON
        Iran GPE
        """

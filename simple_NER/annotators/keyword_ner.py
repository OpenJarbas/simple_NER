from simple_NER.annotators import NERWrapper
from simple_NER import Entity
from simple_NER.annotators.utils.keywords.rake import Rake


class KeywordNER(NERWrapper):
    def __init__(self):
        super().__init__()
        self.add_detector(self.annotate)
        self.rake = Rake()

    def annotate(self, text):
        for x in self.rake.run(text):
            data = {"score": x[1]}
            yield Entity(x[0],
                         "keyword",
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

from simple_NER.annotators import NERWrapper
from simple_NER.rules.rx import Rule
from simple_NER import Entity
import re


class NamesNER(NERWrapper):
    def __init__(self):
        super().__init__()

        self.regex_string = r"\b((?:[A-Z][a-z][-A-Za-z']*(?: *[A-Z][a-z][-A-Za-z']*)*)\b|\b(?:[A-Z][a-z][-A-Za-z']*))\b"
        self.rule = Rule(name="names_rx", rules=[self.regex_string]) # Fake RegexNer
        self.add_detector(self.annotate)

    def annotate(self, text):
        for word in re.findall(self.regex_string,  text):
            yield Entity(word,
                         "Noun",
                         rules=[self.rule],
                         source_text=text,
                         confidence=0.8)


if __name__ == "__main__":

    ner = NamesNER()
    text = "I am JarbasAI , but my real name is Casimiro"
    for e in ner.extract_entities(text):
        print(e.as_json())
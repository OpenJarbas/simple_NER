from simple_NER.annotators import NERWrapper
from simple_NER import Entity

try:
    from quantulum3 import parser
except ImportError:
    print("you need to install quantulum3")
    print("pip install quantulum3")
    raise


class UnitsNER(NERWrapper):
    def __init__(self):
        super().__init__()
        self.add_detector(self.annotate)

    def annotate(self, text):
        spoken = parser.inline_parse_and_expand(text)
        for e in parser.parse(text):
            data = e.__dict__
            data["unit"] = e.unit.__dict__
            data["unit"]["entity"] = e.unit["entity"].__dict__
            e_type = e.unit["entity"]["uri"]
            if e.unit["uri"] != e.unit["entity"]["uri"]:
                e_type = e.unit["entity"]["uri"] + ":" + e.unit["uri"]
            data["spoken"] = spoken
            yield Entity(e.surface, e_type, source_text=text, data=data)


if __name__ == "__main__":
    from pprint import pprint

    ner = UnitsNER()
    for r in ner.extract_entities(
            "The LHC smashes proton beams at 12.8–13.0 TeV"):
        pprint(r.as_json())

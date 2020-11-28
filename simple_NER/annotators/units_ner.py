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

        for e in parser.parse(text):
            spoken = e.to_spoken()
            data = e.__dict__
            data["unit"] = e.unit.__dict__
            data["unit"]["entity"] = e.unit["entity"].__dict__
            e_type = e.unit["entity"]["uri"]
            if e.unit["uri"] != e.unit["entity"]["uri"]:
                e_type = e.unit["entity"]["uri"] + ":" + e.unit["uri"]
            data["spoken"] = spoken
            data.pop("span")
            if data["unit"]["currency_code"] is None:
                data["unit"].pop("currency_code")
            data = data.copy()
            data.pop("surface")
            yield Entity(e.surface, e_type, source_text=text, data=data)


if __name__ == "__main__":
    from pprint import pprint

    ner = UnitsNER()
    for r in ner.extract_entities(
            "The LHC smashes proton beams at 12.8–13.0 TeV"):
        pprint(r.as_json())

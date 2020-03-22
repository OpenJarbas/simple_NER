from simple_NER.annotators import NERWrapper
from simple_NER import Entity
from simple_NER.util import resolve_resource_file
import json


class LocationNER(NERWrapper):
    def __init__(self, lowercase=False):
        super().__init__()
        self.countries = {}
        self.lowercase = lowercase
        self.add_detector(self.annotate)
        self.load_vocab()

    def load_vocab(self):
        vocab_json = resolve_resource_file("countries.json")
        if vocab_json:
            with open(vocab_json) as f:
                self.countries = json.load(f)
        else:
            print("Could not find countries.json")

    def annotate(self, text):
        if self.lowercase:
            words = text.lower().split()
        else:
            words = text.split()

        for word in words:
            for country in self.countries:

                if "latlng" in country:
                    lat, lon = country.pop("latlng")
                    country["latitude"] = lat
                    country["longitude"] = lon

                name = country["name"]
                code = country["country_code"]
                capital = country["capital"]

                if country["latitude"] < 0:
                    hemisphere = "south"
                else:
                    hemisphere = "north"

                country["hemisphere"] = hemisphere

                if word == name:
                    data = country
                    yield Entity(word,
                                 "Country",
                                 source_text=text,
                                 data=data)
                elif word == code:
                    data = country
                    yield Entity(word,
                                 "Country_code",
                                 source_text=text,
                                 data=data)
                elif word == capital:
                    data = {"country_name": name,
                            "country_code": code,
                            "name": capital,
                            "hemisphere": hemisphere}
                    yield Entity(word,
                                 "Capital City",
                                 source_text=text,
                                 data=data)


class CitiesNER(NERWrapper):
    def __init__(self, lowercase=False):
        super().__init__()
        self.cities = {}
        self.lowercase = lowercase
        self.add_detector(self.annotate)
        self.load_vocab()

    def load_vocab(self):

        vocab_json = resolve_resource_file("cities.json")
        if vocab_json:
            with open(vocab_json) as f:
                self.cities = json.load(f)
        else:
            print("Could not find cities.json")

    def annotate(self, text):
        if self.lowercase:
            words = text.lower().split()
        else:
            words = text.split()

        for word in words:
            for city in self.cities:
                code = city["country"]
                name = city["name"]

                if float(city["lat"]) < 0:
                    hemisphere = "south"
                else:
                    hemisphere = "north"

                data = {"name": name,
                        "country_code": code,
                        "latitude": float(city["lat"]),
                        "longitude": float(city["lng"]),
                        "hemisphere": hemisphere}

                if self.lowercase:
                    name = name.lower()

                if word == name:
                    yield Entity(data["name"],
                                 "City",
                                 source_text=text,
                                 data=data)


if __name__ == "__main__":
    from pprint import pprint

    ner = CitiesNER()
    text = """Portugal was born in Guimarães"""
    for r in ner.extract_entities(text):
        print(r.value, "-", r.entity_type)
        pprint(r.as_json())
        """
        Guimarães - City
        {'confidence': 1,
         'data': {'country_code': 'PT',
                  'hemisphere': 'north',
                  'latitude': 41.44443,
                  'longitude': -8.29619,
                  'name': 'Guimarães'},
         'entity_type': 'City',
         'rules': [],
         'source_text': 'Portugal was born in Guimarães',
         'spans': [(21, 30)],
         'value': 'Guimarães'}
        """

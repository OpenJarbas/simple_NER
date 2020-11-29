# Simple NER

simple rule based named entity recognition

* [Install](#install)
* [Usage](#usage)
    + [Rule Based NER](#rule-based-ner)
    + [Regex NER](#regex-ner)
    + [Neural NER](#neural-ner)
    + [Annotators](#annotators)
      - [Email](#email)
      - [Names](#names)
      - [Locations](#locations)
      - [Datetime](#date-time)
      - [Timedelta](#durations)
      - [Units](#units)
      - [Keywords](#keywords)
      - [Numbers](#numbers)
    + [Remote annotators](#remote-annotators)
      - [Spotlight](#spotlight)
    + [NER wrappers](#ner-wrappers)
      - [Snips](#snips)
      - [NLTK](#nltk)
  
  
## Install

Available on pip

```bash
pip install simple_NER
```

## Usage

### Rule Based NER

Entities can be extracted with simple rules using [Padaos](https://github.com/MycroftAI/padaos), a dead simple regex parser

```python
from simple_NER.rules import RuleNER

ner = RuleNER()
ner.add_rule("name", "my name is {person}")

for ent in ner.extract_entities("my name is jarbas"):
    assert ent.as_json() == {'confidence': 1,
                             'data': {},
                             'entity_type': 'person',
                             'rules': [{'name': 'name',
                                        'rules': ['my name is {person}']}],
                             'source_text': 'my name is jarbas',
                             'spans': [(11, 17)],
                             'value': 'jarbas'}
```

### Regex NER

regex can also be used

```python
from simple_NER.rules.rx import RegexNER

ner = RegexNER()
text = "i went to japan in 12/10/1996"

regex = r'((0?[13578]|10|12)(-|\/)((0[0-9])|([12])([0-9]?)|(3[01]?))(-|\/)((\d{4})|(\d{2}))|(0?[2469]|11)(-|\/)((0[0-9])|([12])([0-9]?)|(3[0]?))(-|\/)((\d{4}|\d{2})))'

ner.add_rule("date", regex)

for e in ner.extract_entities(text):
    assert e.as_json() == {'confidence': 1,
                           'data': {},
                           'entity_type': 'date',
                           'rules': [{'name': 'date',
                                      'rules': [
                                          '((0?[13578]|10|12)(-|\\/)((0[0-9])|([12])([0-9]?)|(3[01]?))(-|\\/)((\\d{4})|(\\d{2}))|(0?[2469]|11)(-|\\/)((0[0-9])|([12])([0-9]?)|(3[0]?))(-|\\/)((\\d{4}|\\d{2})))']}],
                           'source_text': 'i went to japan in 12/10/1996',
                           'spans': [(19, 29)],
                           'value': '12/10/1996'}
```

### Neural NER

Entities are extracted using [Padatious](https://github.com/MycroftAI/padatious), An efficient and agile neural network  intent parser
 
This will learn from the rules and extract more variations

```python
from simple_NER.rules.neural import NeuralNER

ner = NeuralNER()
ner.add_rule("name", "my name is {person}")

for ent in ner.extract_entities("the name is jarbas"):
    assert ent.as_json() == {'confidence': 0.5251495787186434,
                             'data': {},
                             'entity_type': 'person',
                             'rules': [{'name': 'name',
                                        'rules': ['my name is {person}']}],
                             'source_text': 'the name is jarbas',
                             'spans': [(12, 18)],
                             'value': 'jarbas'}

for ent in ner.extract_entities("name is kevin"):
    assert ent.as_json() == {'confidence': 0.8363423970007801,
                             'data': {},
                             'entity_type': 'person',
                             'rules': [{'name': 'name',
                                        'rules': ['my name is {person}']}],
                             'source_text': 'name is kevin',
                             'spans': [(8, 13)],
                             'value': 'kevin'}
```

### Annotators

#### Email

Extracting emails using regex rules

```python
from simple_NER.annotators.email_ner import EmailNER

ner = EmailNER()
text = "my email is jarbasai@mailfence.com"
for ent in ner.extract_entities(text):
    assert ent.as_json() == {'confidence': 1,
                             'data': {},
                             'entity_type': 'email',
                             'rules': [{'name': 'email',
                                        'rules': [
                                            '(?:[a-z0-9!#$%&\\\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\\\'*+/=?^_`{|}~-]+)*|"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])']}],
                             'source_text': 'my email is jarbasai@mailfence.com',
                             'spans': [(12, 34)],
                             'value': 'jarbasai@mailfence.com'}
```

#### Names

Extracting Proper Nouns with regex

```python
from simple_NER.annotators.names_ner import NamesNER

ner = NamesNER()
text = "I am JarbasAI , but my real name is Casimiro"
for e in ner.extract_entities(text):
    print(e.as_json())
    
"""
{'entity_type': 'Noun', 'spans': [(5, 13)], 'value': 'JarbasAI', 'source_text': 'I am JarbasAI , but my real name is Casimiro', 'confidence': 0.8, 'data': {}, 'rules': [{'name': 'names_rx', 'rules': ["\\b((?:[A-Z][a-z][-A-Za-z']*(?: *[A-Z][a-z][-A-Za-z']*)*)\\b|\\b(?:[A-Z][a-z][-A-Za-z']*))\\b"]}]}
{'entity_type': 'Noun', 'spans': [(36, 44)], 'value': 'Casimiro', 'source_text': 'I am JarbasAI , but my real name is Casimiro', 'confidence': 0.8, 'data': {}, 'rules': [{'name': 'names_rx', 'rules': ["\\b((?:[A-Z][a-z][-A-Za-z']*(?: *[A-Z][a-z][-A-Za-z']*)*)\\b|\\b(?:[A-Z][a-z][-A-Za-z']*))\\b"]}]}
"""
```

#### Locations

Countries, Capital Cities and Cities can be looked up from a wordlist

```python
from simple_NER.annotators.locations_ner import LocationNER, CitiesNER


ner = LocationNER()
# NOTE: case sensitive, enable detection of lowercase cities/countries
# ner = LocationNER(lowercase=True)


text = """The Capital of Portugal is Lisbon"""
for r in ner.extract_entities(text):
    print(r.value, "-", r.entity_type)
    print(r.as_json())

    """
    Portugal - Country
    {'confidence': 1,
     'data': {'capital': 'Lisbon',
              'country_code': 'PT',
              'hemisphere': 'north',
              'latitude': 39.5,
              'longitude': -8,
              'name': 'Portugal',
              'timezones': ['Europe/Lisbon',
                            'Atlantic/Madeira',
                            'Atlantic/Azores']},
     'entity_type': 'Country',
     'rules': [],
     'source_text': 'The Capital of Portugal is Lisbon',
     'spans': [(15, 23)],
     'value': 'Portugal'}
     
    Lisbon - Capital City
    {'confidence': 1,
     'data': {'country_code': 'PT',
              'country_name': 'Portugal',
              'hemisphere': 'north',
              'name': 'Lisbon'},
     'entity_type': 'Capital City',
     'rules': [],
     'source_text': 'The Capital of Portugal is Lisbon',
     'spans': [(27, 33)],
     'value': 'Lisbon'}
    """


ner = CitiesNER()
# NOTE: case sensitive
# ner = CitiesNER(lowercase=True)

text = """Braga is in northern portugal"""
for r in ner.extract_entities(text):
    print(r.value, "-", r.entity_type)
    print(r.as_json())
    """
     Braga - City
    {'confidence': 1,
     'data': {'country_code': 'PT',
              'hemisphere': 'north',
              'latitude': 41.55032,
              'longitude': -8.42005,
              'name': 'Braga'},
     'entity_type': 'City',
     'rules': [],
     'source_text': 'Braga is in northern portugal',
     'spans': [(0, 5)],
     'value': 'Braga'}
    """
```

#### Date Time

Datetime extraction is powered by [lingua_franca](https://github.com/MycroftAI/lingua-franca)

```python
from simple_NER.annotators.datetime_ner import DateTimeNER

ner = DateTimeNER()

for r in ner.extract_entities("my birthday is on december 5th"):
    assert r.entity_type == "relative_date"
    print("day:", r.day, "month:", r.month, "year:", r.year)
    """
    day: 5 month: 12 year: 2019
    """

for r in ner.extract_entities("entries are due by January 4th, 2017 at 8:30pm"):
    assert r.entity_type == "relative_date"
    print("day:", r.day,"month:", r.month, "year:", r.year, "hour:", r.hour,
          "minute:", r.minute)
    """
    day: 4 month: 1 year: 2017 hour: 20 minute: 30
    """

for r in ner.extract_entities(
        "tomorrow is X yesterday was Y in 10 days it will be Z"):
    assert r.entity_type == "relative_date"
    print(r.value,
          "day:", r.day, "month:", r.month, "year:", r.year,
          "hour:", r.hour, "minute:", r.minute)
    """
    tomorrow day: 30 month: 11 year: 2020 hour: 0 minute: 0
    yesterday day: 28 month: 11 year: 2020 hour: 0 minute: 0
    in 10 days day: 9 month: 12 year: 2020 hour: 0 minute: 0
    """
```

#### Durations

durations/timedeltas extraction is powered by [lingua_franca](https://github.com/MycroftAI/lingua-franca)

```python
from simple_NER.annotators.datetime_ner import TimedeltaNER

ner = TimedeltaNER()

for r in ner.extract_entities(
        "5 minutes ago was X 10 minutes from now is Y in 19 hours will "
        "be N"):
    assert r.entity_type == "duration"
    print(r.value, r.total_seconds)
    """
    5 minutes 300.0
    10 minutes 600.0
    19 hours 68400.0
    """

for r in ner.extract_entities(
        "What President served for five years six months 2 days"):
    # NOTE months/years are not supported because they are not explicit
    # how many days is 1 month? how many days is 1 year?
    assert r.entity_type == "duration"
    print(r.value, r.total_seconds)
    """2 days 172800.0"""

for r in ner.extract_entities("starts in 5 minutes"):
    assert r.entity_type == "duration"
    print(r.value, r.total_seconds)
    """5 minutes 300.0"""

for r in ner.extract_entities("starts in five minutes"):
    assert r.entity_type == "duration"
    print(r.value, r.total_seconds)
    """5 minutes 300.0"""

```

#### Units

Using [Quantulum3](https://github.com/nielstron/quantulum3) for information extraction of quantities, measurements and their units from unstructured text

    
```python
from simple_NER.annotators.units_ner import UnitsNER

ner = UnitsNER()
for r in ner.extract_entities("The LHC smashes proton beams at 12.8–13.0 TeV"):
    assert r.data_value == 12.9
    assert r.unit.name == "teraelectronvolt"
    assert r.value == "12.8–13.0 TeV"
    assert r.as_json() == \
           {'confidence': 1,
            'data': {'lang': 'en_US',
                     'spoken': 'twelve point nine teraelectron volts',
                     'uncertainty': 0.09999999999999964,
                     'unit': {'dimensions': [
                         {'base': 'teraelectronvolt', 'power': 1}],
                         'entity': {
                             'dimensions': [{'base': 'force', 'power': 1},
                                            {'base': 'length',
                                             'power': 1}],
                             'name': 'energy',
                             'uri': 'Energy'},
                         'lang': 'en_US',
                         'name': 'teraelectronvolt',
                         'original_dimensions': [
                             {'base': 'teraelectronvolt',
                              'power': 1,
                              'surface': 'TeV'}],
                         'surfaces': ['teraelectron volt',
                                      'teraelectronvolt',
                                      'teraelectron-volt'],
                         'symbols': ['TeV'],
                         'uri': 'Electronvolt'},
                     'value': 12.9},
            'entity_type': 'Energy:Electronvolt',
            'rules': [],
            'source_text': 'The LHC smashes proton beams at 12.8–13.0 TeV',
            'spans': [(32, 45)],
            'value': '12.8–13.0 TeV'}
```

#### Keywords

The most relevant keywords can be annotated using [Rake](https://github.com/aneesha/RAKE)

```python
from simple_NER.annotators.keyword_ner import KeywordNER

ner = KeywordNER()
text = "Mycroft is a free and open-source voice assistant for Linux-based operating systems that uses a natural language user interface"

# extract keywords
ents = list(ner.extract_entities(text))  # generator, needs list()

# group into tuples of (keyword, score)
keywords = [(ent.value, ent.score) for ent in ents]
keywords = sorted(keywords)  # sort alphabetically


assert sorted(keywords) == [('free', 1.0),
                            ('linux-based operating systems', 9.0),
                            ('mycroft', 1.0),
                            ('natural language user interface', 16.0),
                            ('open-source voice assistant', 9.0)]

```

#### Numbers

Extraction of written numbers is powered by [lingua_franca](https://github.com/MycroftAI/lingua-franca)

```python
from simple_NER.annotators.numbers_ner import NumberNER

ner = NumberNER()
for r in ner.extract_entities("three hundred trillion tons of spinning metal"):
    """
    {'confidence': 1,
     'data': {'number': '300000000000000.0'},
     'entity_type': 'written_number',
     'rules': [],
     'source_text': 'three hundred trillion tons of spinning metal',
     'spans': [(0, 22)],
     'value': 'three hundred trillion'}
    """

ner = NumberNER(short_scale=False)
for r in ner.extract_entities("three hundred trillion tons of spinning metal"):
    """
   {'confidence': 1,
     'data': {'number': '3e+20'},
     'entity_type': 'written_number',
     'rules': [],
     'source_text': 'three hundred trillion tons of spinning metal',
     'spans': [(0, 22)],
     'value': 'three hundred trillion'}
    """

ner = NumberNER()
for r in ner.extract_entities("the 5th number of the third thing"):
    """
   {'confidence': 1,
     'data': {'number': '5'},
     'entity_type': 'written_number',
     'rules': [],
     'source_text': 'the 5th number of the third thing',
     'spans': [(4, 7)],
     'value': '5th'}
    {'confidence': 1,
     'data': {'number': '3'},
     'entity_type': 'written_number',
     'rules': [],
     'source_text': 'the 5th number of the third thing',
     'spans': [(22, 27)],
     'value': 'third'}
    """

ner = NumberNER(ordinals=False)
for r in ner.extract_entities("the 5th number of the third thing"):
    """
   {'confidence': 1,
     'data': {'number': '5'},
     'entity_type': 'written_number',
     'rules': [],
     'source_text': 'the 5th number of the third thing',
     'spans': [(4, 7)],
     'value': '5th'}
    {'confidence': 1,
     'data': {'number': '0.3333333333333333'},
     'entity_type': 'written_number',
     'rules': [],
     'source_text': 'the 5th number of the third thing',
     'spans': [(22, 27)],
     'value': 'third'}
    """
```

### Remote annotators

Some web based annotators are also provided

#### Spotlight

Using [spotlight](https://www.dbpedia-spotlight.org/demo/) we can annotate entities from dbpedia

```python
from simple_NER.annotators.remote.dbpedia import SpotlightNER

# you can also self host
host='http://api.dbpedia-spotlight.org/en/annotate'

ner = SpotlightNER(host)
for r in ner.extract_entities("London was founded by the Romans"):
    print(r.value, r.entity_type, r.uri)
    score = r.similarityScore
    """
    London Wikidata:Q515 http://dbpedia.org/resource/London
    London Wikidata:Q486972 http://dbpedia.org/resource/London
    London Schema:Place http://dbpedia.org/resource/London
    London Schema:City http://dbpedia.org/resource/London
    London DBpedia:Settlement http://dbpedia.org/resource/London
    London DBpedia:PopulatedPlace http://dbpedia.org/resource/London
    London DBpedia:Place http://dbpedia.org/resource/London
    London DBpedia:Location http://dbpedia.org/resource/London
    London DBpedia:City http://dbpedia.org/resource/London
    Romans Wikidata:Q6256 http://dbpedia.org/resource/Ancient_Rome
    Romans Schema:Place http://dbpedia.org/resource/Ancient_Rome
    Romans Schema:Country http://dbpedia.org/resource/Ancient_Rome
    Romans DBpedia:PopulatedPlace http://dbpedia.org/resource/Ancient_Rome
    Romans DBpedia:Place http://dbpedia.org/resource/Ancient_Rome
    Romans DBpedia:Location http://dbpedia.org/resource/Ancient_Rome
    Romans DBpedia:Country http://dbpedia.org/resource/Ancient_Rome
    """
```

### NER wrappers

wrappers are also provided for performing NER with external libs

#### Snips

If you have snips_nlu installed you can extract the [builtin entities](https://snips-nlu.readthedocs.io/en/latest/builtin_entities.html)

```python
from simple_NER.annotators.snips_ner import SnipsNER

ner = SnipsNER()

text = "The farmer had 2 cows, The cows died after 5 days."
for e in ner.extract_entities(text):
    print(e.value, e.entity_type)
    """
    2 snips/number
    after 5 days snips/date
    """
```

#### NLTK

```python
from simple_NER.annotators.nltk_ner import NltkNER

ner = NltkNER()
text = """The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world"."""
for r in ner.extract_entities(text):
    print(r.value, r.entity_type)
    """
    Israeli GPE
    Benjamin Netanyahu PERSON
    Iran GPE
    """
```
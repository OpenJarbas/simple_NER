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
      - [Date Time](#date-time)
      - [Units](#units)
      - [Keywords](#keywords)
    + [Remote annotators](#remote-annotators)
      - [Spotlight](#spotlight)
      - [AllenNLP](#allennlp)
    + [NER wrappers](#ner-wrappers)
      - [Snips](#snips)
      - [NLTK](#nltk)
      - [Spacy](#spacy)
      - [Cogcomp](#cogcomp)
  
  
## Install

Available on pip

    pip install simple_NER
    
from source

    git clone https://github.com/JarbasAl/simple_NER
    cd simple_NER
    pip install -r requirements.txt
    pip install .
    
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
from simple_NER.rules.regex import RegexNER

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

Emails can be annotated using regex rules

```python
from simple_NER.annotators.mail import EmailNER

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
from simple_NER.annotators.names import NamesNER

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
from simple_NER.annotators.locations import LocationNER, CitiesNER


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

dates and durations can be annotated using [lingua_franca](https://github.com/MycroftAI/lingua-franca)

```python
from simple_NER.annotators.date import DateTimeNER

ner = DateTimeNER()

for r in ner.extract_entities("The movie is one hour, fifty seven and a half minutes long"):
    assert r.value == 'one hour, fifty seven and a half minutes'
    assert r.entity_type == "duration"
    assert r.total_seconds == 7050
    assert r.spoken == 'one hour fifty seven minutes thirty seconds'   

for r in ner.extract_entities("my birthday is on december 5th"):
    assert r.value == 'december 5'
    assert r.entity_type == "relative_date"
    print("day:", r.day, "month:", r.month, "year:", r.year)
    """
    december 5th
    day: 5 month: 12 year: 2019
    """

for r in ner.extract_entities("entries are due by January 4th, 2017 at 8:30pm"):
    print(r.value)
    assert r.entity_type == "relative_date"
    print("day:", r.day,"month:", r.month, "year:", r.year, "hour:", r.hour,
          "minute:", r.minute)
    """
    January 4th, 2017 at 8:30pm
    day: 4 month: 1 year: 2017 hour: 20 minute: 30

    """

```

#### Units

Using [Quantulum3](https://github.com/nielstron/quantulum3) for information extraction of quantities, measurements and their units from unstructured text

    
```python
from simple_NER.annotators.units import UnitsNER

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

### Remote annotators

Some web based annotators are also provided

#### Spotlight

Using [pyspotlight](https://github.com/ubergrape/pyspotlight) we can annotate entities from dbpedia

    
```python
from simple_NER.annotators.remote.dbpedia import SpotlightNER

# you can also self host
host='http://api.dbpedia-spotlight.org/en/annotate'

ner = SpotlightNER(host)
for r in ner.extract_entities("elon musk works in spaceX"):
    print(r.value, r.entity_type, r.uri)
    score = r.similarityScore
    """
    elon musk Person http://dbpedia.org/resource/Elon_Musk
    elon musk Agent http://dbpedia.org/resource/Elon_Musk
    spaceX Organisation http://dbpedia.org/resource/SpaceX
    spaceX Company http://dbpedia.org/resource/SpaceX
    spaceX Agent http://dbpedia.org/resource/SpaceX
    """
```

#### AllenNLP

using the [AllenNLP demo](https://github.com/allenai/allennlp-demo)

```python
from simple_NER.annotators.remote.allenai import AllenNlpNER

# you can also self host
host = "http://demo.allennlp.org/predict/"

ner = AllenNlpNER(host)
ents = [r for r in ner.extract_entities("Lisbon is the capital of Portugal")]
assert ents[0].as_json() == {'confidence': 1,
                             'data': {},
                             'entity_type': 'U-LOC',
                             'rules': [],
                             'source_text': 'Lisbon is the capital of Portugal',
                             'spans': [(0, 6)],
                             'value': 'Lisbon'}
```

### NER wrappers

wrappers are also provided for performing NER with external libs

#### Snips

If you have snips_nlu installed you can extract the [builtin entities](https://snips-nlu.readthedocs.io/en/latest/builtin_entities.html)

```python
from simple_NER.annotators.snips import SnipsNER

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

#### Spacy

Wrapper for [Spacy](https://github.com/explosion/spaCy) Industrial-strength Natural Language Processing

```python
from simple_NER.annotators.spacy_ner import SpacyNER
ner = SpacyNER()
text = "When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously."
for e in ner.extract_entities(text):
    print(e.value, e.entity_type)
    """
    Sebastian Thrun PERSON
    Google FAC
    2007 DATE
    """
```

You might be interested in the [lookup extension](https://github.com/mpuig/spacy-lookup) for spacy 

#### Cogcomp

wrapper for [cogcomp-nlpy](https://github.com/CogComp/cogcomp-nlpy)

You can run the local pipeline

```python
from simple_NER.annotators.cogcomp_ner import CogcompNER

ner = CogcompNER() # use ontonotes model
# ner = CogcompNER(ontonotes=False)  # use connl model

text = """"Helicopters will patrol the temporary no-fly zone around 
New Jersey's MetLife Stadium Sunday, with F-16s based in Atlantic City 
ready to be scrambled if an unauthorized aircraft does enter the 
restricted airspace"""

for r in ner.extract_entities(text):
    print(r.value, r.entity_type)
    """
    New Jersey 's GPE
    MetLife Stadium ORG
    Sunday DATE
    Atlantic City GPE
    """

```

or the remote pipeline

```python
from simple_NER.annotators.remote.cogcomp import CogcompNER

# you may use you own server, demo is limited to 100 queries/day
host = None
ner = CogcompNER(host) # use ontonotes model
# ner = CogcompNER(host, ontonotes=False)  # use connl model

text = """"Helicopters will patrol the temporary no-fly zone around 
New Jersey's MetLife Stadium Sunday, with F-16s based in Atlantic City 
ready to be scrambled if an unauthorized aircraft does enter the 
restricted airspace"""

for r in ner.extract_entities(text):
    print(r.value, r.entity_type)
    """
    New Jersey 's GPE
    MetLife Stadium ORG
    Sunday DATE
    Atlantic City GPE
    """
```

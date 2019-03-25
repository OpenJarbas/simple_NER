# Simple NER

simple rule based named entity recognition

- [Simple NER](#simple-ner)
  * [Install](#install)
  * [Usage](#usage)
    + [Word Lookup NER](#word-lookup-ner)
    + [Rule Based NER](#rule-based-ner)
    + [Regex NER](#regex-ner)
    + [Neural NER](#neural-ner)
    + [Custom Annotators](#custom-annotators)
      - [Date Time](#date-time)
      - [Spotlight](#spotlight)
      - [Units](#units)
  * [Similar Projects](#similar-projects)
  
  
## Install

Available on pip

    pip install simple_NER
    
from source

    git clone https://github.com/JarbasAl/simple_NER
    cd simple_NER
    pip install -r requirements.txt
    pip install .
    
## Usage
    
### Word Lookup NER

the simplest possible NER is checking for the existence of a word in text


```python
from simple_NER import SimpleNER

ner = SimpleNER()
ner.add_entity_examples("person", ["bob", "jon", "amy", "kevin"])

for ent in ner.entity_lookup("where is Kevin", as_json=True):
    assert ent == {'confidence': 1,
                 'end': 14,
                 'entity_type': 'person',
                 'rules': [],
                 'source_text': 'where is Kevin',
                 'start': 9,
                 'value': 'kevin'}
                 
assert ner.is_match("jon is ugly", "person")
assert not ner.is_match("i like pizza", "person")

```

### Rule Based NER

Entities can be extracted with simple rules using [Padaos](https://github.com/MycroftAI/padaos), a dead simple regex parser

```python
from simple_NER.rules import RuleNER

ner = RuleNER()
ner.add_rule("name", "my name is {person}")

for ent in ner.extract_entities("my name is jarbas"):
    assert ent.as_json() == {'confidence': 1,
                             'end': 17,
                             'entity_type': 'person',
                             'rules': [{'name': 'name',
                                        'rules': ['my name is {person}']}],
                             'source_text': 'my name is jarbas',
                             'start': 11,
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
                           'end': 29,
                           'entity_type': 'date',
                           'rules': [{'name': 'date',
                                      'rules': [
                                          '((0?[13578]|10|12)(-|\\/)((0[0-9])|([12])([0-9]?)|(3[01]?))(-|\\/)((\\d{4})|(\\d{2}))|(0?[2469]|11)(-|\\/)((0[0-9])|([12])([0-9]?)|(3[0]?))(-|\\/)((\\d{4}|\\d{2})))']}],
                           'source_text': 'i went to japan in 12/10/1996',
                           'start': 19,
                           'value': '12/10/1996'}

```


### Neural NER

Entities are extracted using [Padatious](https://github.com/MycroftAI/padatious), An efficient and agile neural network  intent parser
 
You need an extra install step in order to use this

    pip install fann2==1.0.7
    pip install padatious==0.4.5

This will learn from the rules and extract more variations

```python
from simple_NER.rules.neural import NeuralNER

ner = NeuralNER()
ner.add_rule("name", "my name is {person}")

for ent in ner.extract_entities("the name is jarbas"):
    assert ent.as_json() == {'confidence': 0.6327182657104353,
                             'end': 18,
                             'entity_type': 'person',
                             'rules': [{'name': 'name',
                                        'rules': ['my name is {person}']}],
                             'source_text': 'the name is jarbas',
                             'start': 12,
                             'value': 'jarbas'}
                             
for ent in ner.extract_entities("name is kevin"):
    assert ent.as_json() == {'confidence': 0.8290174158328332,
                             'end': 13,
                             'entity_type': 'person',
                             'rules': [{'name': 'name',
                                        'rules': ['my name is {person}']}],
                             'source_text': 'name is kevin',
                             'start': 8,
                             'value': 'kevin'}
```

### Custom Annotators

you can create your own annotators

```python
from simple_NER.annotators import NERWrapper
from simple_NER import Entity


def extract_hitler(text):
    if "hitler" in text.lower():
        yield Entity("hitler", "bad_guy", source_text=text, data={
            "known_for": ["killing jews", "world war 2"]})


ner = NERWrapper()
ner.add_detector(extract_hitler)

for ent in ner.extract_entities("hitler only had one ball"):
    assert ent.as_json() == {'confidence': 1,
                             'data': {
                                 'known_for': ['killing jews', 'world war 2']},
                             'end': 6,
                             'entity_type': 'bad_guy',
                             'rules': [],
                             'source_text': 'hitler only had one ball',
                             'start': 0,
                             'value': 'hitler'}
```

#### Date Time

relative date times can be annotated

```python
from simple_NER.annotators.date import DateTimeNER

ner = DateTimeNER()
for r in ner.extract_entities("meeting tomorrow morning"):
    assert r.value == 'tomorrow morning'

for r in ner.extract_entities("my birthday is on december 5th"):
    assert r.value == 'on december 5th'
    assert r.name == "date"
```

#### Spotlight

Using [pyspotlight](https://github.com/ubergrape/pyspotlight) we can annotate entities from dbpedia

extra install step

    pip install pyspotlight
    
    
```python
from simple_NER.annotators.dbpedia import SpotlightNER

ner = SpotlightNER()
for r in ner.extract_entities("elon musk works in spaceX"):
    print(r.value, r.name)

    """
    elon musk Person
    elon musk Agent
    spaceX Organisation
    spaceX Company
    spaceX Agent
    """
```

#### Units

Using [Quantulum3](https://github.com/nielstron/quantulum3) for information extraction of quantities, measurements and their units from unstructured text

extra install step

    pip install quantulum3
    
    
```python
from simple_NER.annotators.units import UnitsNER

ner = UnitsNER()
for r in ner.extract_entities("The LHC smashes proton beams at 12.8–13.0 TeV"):
    assert r.as_json() == \
           {'confidence': 1,
            'data': {'lang': 'en_US',
                     'span': (32, 45),
                     'spoken': 'The LHC smashes proton beams at twelve point nine '
                               'teraelectron volts',
                     'surface': '12.8–13.0 TeV',
                     'uncertainty': 0.09999999999999964,
                     'unit': {'currency_code': None,
                              'dimensions': [
                                  {'base': 'teraelectronvolt', 'power': 1}],
                              'entity': {'dimensions': [
                                  {'base': 'force', 'power': 1},
                                  {'base': 'length', 'power': 1}],
                                  'name': 'energy',
                                  'uri': 'Energy'},
                              'lang': 'en_US',
                              'name': 'teraelectronvolt',
                              'original_dimensions': [
                                  {'base': 'teraelectronvolt', 'power': 1,
                                   'surface': 'TeV'}],
                              'surfaces': ['teraelectron volt', 
                                           'teraelectronvolt',
                                           'teraelectron-volt'],
                              'symbols': ['TeV'],
                              'uri': 'Electronvolt'},
                     'value': 12.9},
            'end': 45,
            'entity_type': 'Energy:Electronvolt',
            'rules': [],
            'source_text': 'The LHC smashes proton beams at 12.8–13.0 TeV',
            'start': 32,
            'value': '12.8–13.0 TeV'}

```

## Similar Projects

This is a rule based NER library, if you are looking for a out of the box solution check these projects

- [Polyglot](https://github.com/aboSamoor/polyglot) - Multilingual text (NLP) processing toolkit
- [Spacy](https://github.com/explosion/spaCy) and the [lookup extension](https://github.com/mpuig/spacy-lookup) - Industrial-strength Natural Language Processing
- [NeuroNER](https://github.com/Franck-Dernoncourt/NeuroNER) - Named-entity recognition using neural networks. Easy-to-use and state-of-the-art results.
- [Chatbot NER](https://github.com/hellohaptik/chatbot_ner) - Named Entity Recognition for chatbots
- [EpiTator](https://github.com/ecohealthalliance/EpiTator) - Annotators for extracting epidemiological information from text.


[![Donate with Bitcoin](https://en.cryptobadges.io/badge/micro/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)](https://en.cryptobadges.io/donate/1QJNhKM8tVv62XSUrST2vnaMXh5ADSyYP8)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://paypal.me/jarbasai)
<span class="badge-patreon"><a href="https://www.patreon.com/jarbasAI" title="Donate to this project using Patreon"><img src="https://img.shields.io/badge/patreon-donate-yellow.svg" alt="Patreon donate button" /></a></span>
[![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-!-1EAEDB.svg)](https://saythanks.io/to/JarbasAl)

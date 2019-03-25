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
      - [Email](#email)
      - [Date Time](#date-time)
      - [Units](#units)
    + [Remote annotators](#remote-annotators)
      - [Spotlight](#spotlight)
      - [Spacy Demo](#spacy-demo)
      - [Polyglot Demo](#polyglot-demo)
      - [AllenAi Nlp](#allenai-nlp)
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

assert ner.is_match("jon is ugly", "person")
assert not ner.is_match("i like pizza", "person")

for ent in ner.entity_lookup("where is Kevin", as_json=True):
    assert ent == {'confidence': 1,
                   'data': {},
                   'entity_type': 'person',
                   'rules': [],
                   'source_text': 'where is Kevin',
                   'spans': [(9, 14)],
                   'value': 'kevin'}
```

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
 
You need an extra install step in order to use this

    pip install fann2==1.0.7
    pip install padatious==0.4.5

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
    assert ent.known_for == ['killing jews', 'world war 2']
    assert ent.value == "hitler"
    assert ent.entity_type == "bad_guy"
    assert ent.as_json() == {'confidence': 1,
                             'data': {
                                 'known_for': ['killing jews', 'world war 2']},
                             'entity_type': 'bad_guy',
                             'rules': [],
                             'source_text': 'hitler only had one ball',
                             'spans': [(0, 6)],
                             'value': 'hitler'}
```

#### Email

Emails can be annotated using regex rules

```python
from simple_NER.annotators.email import EmailNER

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

#### Date Time

date times can be annotated using [MycroftAI parsers](https://github.com/MycroftAI/mycroft-core/blob/dev/mycroft/util/lang/parse_en.py#L667)

annotated entities will have timestamp and iso_format properties

a anchor date can be provided for relative times

```python
from simple_NER.annotators.date import DateTimeNER

from datetime import datetime
# if not provided used datetime.now()
reference_date = datetime(2010, 5, 13)

ner = DateTimeNER(anchor_date=reference_date)

for r in ner.extract_entities("meeting tomorrow morning"):
    assert r.value == 'tomorrow morning'
    assert r.iso_format == "2010-05-14T08:00:00"
    assert r.timestamp == 1273820400.0

for r in ner.extract_entities("my birthday is on december 5th"):
    assert r.value == 'on december 5th'
    assert r.entity_type == "date"

```

#### Units

Using [Quantulum3](https://github.com/nielstron/quantulum3) for information extraction of quantities, measurements and their units from unstructured text

extra install step

    pip install quantulum3
    
    
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

### Remote annotators

Some web based annotators are also provided

#### Spotlight

Using [pyspotlight](https://github.com/ubergrape/pyspotlight) we can annotate entities from dbpedia

extra install step

    pip install pyspotlight
    
    
```python
from simple_NER.annotators.remote.dbpedia import SpotlightNER

ner = SpotlightNER()
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

#### Spacy Demo

webscrapping the [spacy NER demo](https://explosion.ai/demos/displacy-ent)

```python
from simple_NER.annotators.remote.spacy import SpacyNER

ner = SpacyNER()
for r in ner.extract_entities("elon musk works in spaceX"):
    assert r.as_json() == {'confidence': 1,
                           'data': {},
                           'entity_type': 'ORG',
                           'rules': [],
                           'source_text': 'elon musk works in spaceX',
                           'spans': [(19, 25)],
                           'value': 'spaceX'}
```

#### Polyglot Demo

webscrapping the [polyglot NER demo](https://sites.google.com/site/rmyeid/projects/polylgot-ner#h.p_ID_63)

```python
from simple_NER.annotators.remote.polyglot import PolyglotNER

ner = PolyglotNER()
text = """The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world"."""
ents = [r for r in ner.extract_entities(text)]
assert ents[0].as_json() == {'confidence': 1,
                             'data': {},
                             'entity_type': 'person',
                             'rules': [],
                             'source_text': 'The Israeli Prime Minister Benjamin Netanyahu has warned that '
                                            'Iran poses a "threat to the entire world".',
                             'spans': [(27, 35)],
                             'value': 'Benjamin'}
assert ents[2].as_json() == {'confidence': 1,
                             'data': {},
                             'entity_type': 'location',
                             'rules': [],
                             'source_text': 'The Israeli Prime Minister Benjamin Netanyahu has warned that '
                                            'Iran poses a "threat to the entire world".',
                             'spans': [(62, 66)],
                             'value': 'Iran'}
```

#### AllenAi Nlp

using the [AllenNLP demo](https://github.com/allenai/allennlp-demo)

```python
from simple_NER.annotators.remote.allenai import AllenNlpNER

host = "http://demo.allennlp.org/predict/"

ner = AllenNlpNER(host)
ents = [r for r in
        ner.extract_entities("Lisbon is the capital of Portugal")]
assert ents[0].as_json() == {'confidence': 1,
                             'data': {},
                             'entity_type': 'U-LOC',
                             'rules': [],
                             'source_text': 'Lisbon is the capital of Portugal',
                             'spans': [(0, 6)],
                             'value': 'Lisbon'}
assert ents[1].as_json() == {'confidence': 1,
                             'data': {},
                             'entity_type': 'U-LOC',
                             'rules': [],
                             'source_text': 'Lisbon is the capital of Portugal',
                             'spans': [(25, 33)],
                             'value': 'Portugal'}
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

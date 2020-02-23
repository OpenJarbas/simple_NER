from simple_NER.annotators.snips import SnipsNER

ner = SnipsNER()

text = "The farmer had 2 cows, The cows died after 5 days."
for e in ner.extract_entities(text):
    print(e.value, e.entity_type)
    """
    2 snips/number
    after 5 days snips/date
    """
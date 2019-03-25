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
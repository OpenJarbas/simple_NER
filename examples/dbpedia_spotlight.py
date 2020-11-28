from simple_NER.annotators.remote.dbpedia import SpotlightNER

ner = SpotlightNER()
for r in ner.extract_entities("elon musk works in spaceX"):
    score = r.similarityScore
    print(r.value, r.entity_type, r.uri, score)
    """
    elon musk Person http://dbpedia.org/resource/Elon_Musk
    elon musk Agent http://dbpedia.org/resource/Elon_Musk
    spaceX Organisation http://dbpedia.org/resource/SpaceX
    spaceX Company http://dbpedia.org/resource/SpaceX
    spaceX Agent http://dbpedia.org/resource/SpaceX
    """
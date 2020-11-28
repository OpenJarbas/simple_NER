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
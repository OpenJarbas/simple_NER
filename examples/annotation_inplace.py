from simple_NER.annotators.remote.dbpedia import SpotlightNER

ner = SpotlightNER()
text = "stephen hawking was a physicist"
assert ner.in_place_annotation(text) == "stephen hawking(Scientist|Person|Agent) was a physicist"

text = "elon musk works for spaceX"
assert ner.in_place_annotation(text) == "elon musk(Person|Agent) works for spaceX(Organisation|Company|Agent)"

text = "lisbon is a city, lisbon is the capital of Portugal"
assert ner.in_place_annotation(text) == "lisbon(Place|Location) is a city, lisbon(Place|Location) is the capital of Portugal(PopulatedPlace|Place|Location|Country)"
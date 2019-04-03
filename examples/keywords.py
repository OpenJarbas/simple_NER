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

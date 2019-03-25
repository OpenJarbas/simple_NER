import re
from simple_NER import Entity
from simple_NER.rules import Rule, RuleNER


class RegexNER(RuleNER):
    def __init__(self):
        self._rules = {}
        self._examples = {}

    def _create_regex(self, rule):
        """ Create regex and return. If error occurs returns None. """
        return re.compile(rule, re.IGNORECASE)

    def extract_entities(self, query):
        for r in self._rules:
            for rule in self._rules[r]:
                for rul in rule.rules:
                    regex = self._create_regex(rul)
                    match = regex.findall(query)
                    for ent in match:
                        ent = ent[0]
                        yield Entity(ent, rule.name, source_text=query,
                                     rules=self._rules[r])

    def add_entity_examples(self, name, examples):
        if isinstance(examples, str):
            examples = [examples]
        if name not in self._examples:
            self._examples[name] = []
        for e in examples:
            rules = r'\b' + e.lower() + r"\b"
            self._examples[name].append(Entity(e, name,
                                               rules=Rule(name, rules)))

    def add_rule(self, name, rules):
        if isinstance(rules, str):
            rules = [rules]
        if name not in self._rules:
            self._rules[name] = []
        self._rules[name].append(Rule(name, rules))


if __name__ == "__main__":
    from pprint import pprint

    n = RegexNER()
    text = "hello there"
    word = "hello"
    rules = r'(\W*'+word+'\W*\!?\W*)'
    n.add_rule("greeting", rules)
    for e in n.extract_entities(text):
        pprint(e.as_json())

    n.add_entity_examples("person", ["bob", "joe", "amy"])
    text = "hello amy"
    for e in n.entity_lookup(text):
        pprint(e.as_json())

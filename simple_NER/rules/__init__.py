from padaos import IntentContainer
from simple_NER import Entity, SimpleNER


class Rule(object):
    def __init__(self, name, rules):
        self._name = name
        self._rules = rules

    @property
    def rules(self):
        return self._rules

    @property
    def name(self):
        return self._name

    def __repr__(self):
        return self.name

    def as_json(self):
        return {"name": self.name, "rules": self._rules}


class RuleNER(SimpleNER):
    def __init__(self):
        self._container = IntentContainer()
        self._rules = {}
        self._examples = {}

    @property
    def rules(self):
        return self._rules

    @property
    def examples(self):
        return self._examples

    def add_rule(self, name, rules):
        if isinstance(rules, str):
            rules = [rules]
        self._container.add_intent(name, rules)
        if name not in self._rules:
            self._rules[name] = []

        # NOTE, there is a bug, entities need to be lower case
        # n.add_rule("name", "my name is {Person}") <- won't work
        rules = [r.lower() for r in rules]
        self._rules[name].append(Rule(name, rules))

    def add_entity_examples(self, name, examples):
        if isinstance(examples, str):
            examples = [examples]
        self._container.add_entity(name, examples)
        if name not in self._examples:
            self._examples[name] = []
        for e in examples:
            self._examples[name].append(Entity(e, name))

    def extract_entities(self, text, as_json=False):
        for rule in self._container.calc_intents(text):
            for e in rule["entities"]:
                if as_json:
                    yield Entity(rule["entities"][e], entity_type=e,
                                 source_text=text,
                                 rules=self._rules[rule["name"]]).as_json()
                else:
                    yield Entity(rule["entities"][e], entity_type=e,
                                 source_text=text,
                                 rules=self._rules[rule["name"]])


if __name__ == "__main__":
    from pprint import pprint
    n = RuleNER()
    n.add_rule("name", "my name is {person}")
    for ent in n.extract_entities("my name is jarbas"):
        print("TEXT:", ent.source_text)
        print("ENTITY TYPE: ", ent.entity_type, "ENTITY_VALUE: ", ent.value)
        print("RULES:", ent.rules)

    n.add_entity_examples("person", "jon doe")
    for ent in n.entity_lookup("who is jon doe?", as_json=True):
        pprint(ent)
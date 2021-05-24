import simplematch as sm
from simple_NER import Entity, SimpleNER
from quebra_frases.list_utils import flatten


class Rule:
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
        if name not in self._rules:
            self._rules[name] = []

        rules = [r.lower() for r in rules]
        self._rules[name].append(Rule(name, rules))

    def add_entity_examples(self, name, examples):
        if isinstance(examples, str):
            examples = [examples]
        if name not in self._examples:
            self._examples[name] = []
        for e in examples:
            self._examples[name].append(Entity(e, name))

    def extract_entities(self, text, as_json=False):
        for name, rules in self._rules.items():
            regexes = flatten([r.rules for r in rules])

            for r in regexes:
                entities = sm.match(r, text, case_sensitive=True)
                if entities is None:
                    entities = sm.match(r, text, case_sensitive=False)

                if entities is not None:
                    for k, v in entities.items():
                        ent = Entity(v, entity_type=k,
                                     source_text=text,
                                     rules=r)
                        if as_json:
                            yield ent.as_json()
                        else:
                            yield ent


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
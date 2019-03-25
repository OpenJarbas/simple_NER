try:
    from padatious import IntentContainer
except ImportError:
    print("padatious not found, run")
    print("pip install fann2==1.0.7")
    print("pip install padatious==0.4.5")
    raise

from simple_NER.rules import RuleNER
from simple_NER import Entity
from os.path import expanduser, isdir, join
from os import makedirs


class NeuralNER(RuleNER):
    def __init__(self):
        cache = expanduser("~/.simple_NER")
        if not isdir(cache):
            makedirs(cache)
        self._container = IntentContainer(join(cache, "rule_cache"))
        self._rules = {}
        self._examples = {}

    def extract_entities(self, text, as_json=False):
        for rule in self._container.calc_intents(text):
            for e in rule.matches:
                if as_json:
                    yield Entity(rule.matches[e], entity_type=e,
                                 source_text=text, confidence=rule.conf,
                                 rules=self._rules[rule.name]).as_json()
                else:
                    yield Entity(rule.matches[e], entity_type=e,
                                 source_text=text, confidence=rule.conf,
                                 rules=self._rules[rule.name])


if __name__ == "__main__":
    from pprint import pprint

    n = NeuralNER()
    n.add_rule("name", "my name is {Person}")
    for ent in n.extract_entities("the name is jarbas"):
        print("TEXT:", ent.source_text)
        print("ENTITY TYPE: ", ent.name, "ENTITY_VALUE: ", ent.value)
        print("RULES:", ent.rules)
    for ent in n.extract_entities("my name is chatterbox", as_json=True):
        pprint(ent)

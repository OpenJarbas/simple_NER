import re
import types


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += len(sub)  # use start += 1 to find overlapping matches


class Entity:
    _name = "entity"

    def __init__(self, value, entity_type=None, source_text="", rules=None,
                 confidence=1, data=None):
        if entity_type:
            self._name = entity_type
        self._index = source_text.lower().find(value.lower())
        self._value = value
        self._source_text = source_text
        self._all_indexes = [i for i in find_all(source_text.lower(),
                                                 value.lower())]
        if rules and not isinstance(rules, list) and not isinstance(rules,
                                                                    tuple):
            rules = [rules]
        self._rules = rules or []
        self._confidence = confidence
        self.data = data or {}

        # set properties so they can be accessed with dot notation
        for k in self.data:
            if isinstance(self.data[k], dict):
                clazz = types.new_class(k, (Entity,))
                for k2 in self.data[k]:
                    setattr(clazz, k2, self.data[k][k2])
                setattr(self, k, clazz(k))
            elif k == "value":
                setattr(self, "data_value", self.data[k])
            else:
                setattr(self, k, self.data[k])

    @property
    def indexes(self):
        return self._all_indexes

    @property
    def occurrence_number(self):
        return len(self._all_indexes)

    @property
    def confidence(self):
        return self._confidence

    @property
    def rules(self):
        return self._rules

    @property
    def entity_type(self):
        return self._name

    @property
    def value(self):
        return self._value

    @property
    def source_text(self):
        return self._source_text

    @property
    def spans(self):
        return [(i, i + len(self.value)) for i in self.indexes]

    def as_json(self):
        return {"entity_type": self.entity_type, "spans": self.spans,
                "value": self.value, "source_text": self.source_text,
                "confidence": self.confidence, "data": self.data,
                "rules": [r.as_json() for r in self.rules]}

    def __repr__(self):
        return self.entity_type + ":" + self.value


class SimpleNER:
    def __init__(self):
        self._examples = {}

    def is_match(self, text, entity):
        entities = []
        if isinstance(entity, str):
            entities = self._examples[entity]
        if isinstance(entity, Entity):
            entities = [entity]
        for ent in entities:
            if re.findall(r'\b' + ent.value.lower() + r"\b", text.lower()):
                return True
        return False

    @property
    def examples(self):
        return self._examples

    def add_entity_examples(self, name, examples):
        if isinstance(examples, str):
            examples = [examples]
        if name not in self._examples:
            self._examples[name] = []
        for e in examples:
            self._examples[name].append(Entity(e, name))

    def in_place_annotation(self, text):
        new_text = text
        indexes = {}
        # map ents to indexes
        for ent in self.extract_entities(text):
            indexs = ent.indexes
            for index in indexs:
                index += len(ent.value)
                if index not in indexes:
                    indexes[index] = []
                if (ent.value, ent.entity_type) not in indexes[index]:
                    indexes[index] += [(ent.value, ent.entity_type)]
        # generate annotation
        for index in indexes:
            ano = "(" + "|".join([i[1] for i in indexes[index]]) + ")"
            indexes[index] = ano
        # replace, last index first
        sor = sorted(indexes.keys(), reverse=True)
        for i in sor:
            new_text = new_text[:i] + indexes[i] + new_text[i:]
        return new_text

    def entity_lookup(self, text, as_json=False):
        for ent_name in self.examples:
            for ent in self.examples[ent_name]:

                if re.findall(r'\b' + ent.value.lower() + r"\b", text.lower()):
                    if as_json:
                        yield Entity(value=ent.value,
                                     entity_type=ent.entity_type,
                                     source_text=text).as_json()
                    else:
                        yield Entity(value=ent.value,
                                     entity_type=ent.entity_type,
                                     source_text=text)

    def extract_entities(self, text, as_json=False):
        for e in self.entity_lookup(text, as_json):
            yield e


if __name__ == "__main__":
    from pprint import pprint

    n = SimpleNER()
    n.add_entity_examples("person", ["jarbas", "kevin"])
    pprint(n.examples)
    for ent in n.entity_lookup("my name is Jarbas"):
        print("TEXT:", ent.source_text)
        print("ENTITY TYPE: ", ent.entity_type, "ENTITY_VALUE: ", ent.value)
    for ent in n.entity_lookup("where is Kevin", as_json=True):
        pprint(ent)

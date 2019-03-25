from simple_NER.rules.regex import RegexNER


class EmailNER(RegexNER):
    def __init__(self):
        super().__init__()
        regex_string = r'(?:[a-z0-9!#$%&\'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&\'*+/=?^_`{|}~-]+)*|' + \
                       r'"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")' + \
                       r'@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|' + \
                       r'\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|' + \
                       r'[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|' + \
                       r'\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])'
        self.add_rule("email", regex_string)


if __name__ == "__main__":

    ner = EmailNER()
    text = "my email is jarbasai@mailfence.com"
    for ent in ner.extract_entities(text):
        assert ent.as_json() == {'confidence': 1,
                                 'data': {},
                                 'end': 34,
                                 'entity_type': 'email',
                                 'rules': [{'name': 'email',
                                            'rules': [
                                                '(?:[a-z0-9!#$%&\\\'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&\\\'*+/=?^_`{|}~-]+)*|"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21-\\x5a\\x53-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])+)\\])']}],
                                 'source_text': 'my email is jarbasai@mailfence.com',
                                 'start': 12,
                                 'value': 'jarbasai@mailfence.com'}

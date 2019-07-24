from simple_NER.annotators.medacy_ner import MedacyNER

ner = MedacyNER()
text = "The patient was prescribed 1 capsule of Advil for 5 days."
for e in ner.extract_entities(text):
    print(e.value, e.entity_type)
    """
    1 Dosage
    capsule Form
    Advil Drug
    for 5 days Duration
    """
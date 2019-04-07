from simple_NER.annotators import NERWrapper
from simple_NER import Entity

try:
    from ccg_nlpy import local_pipeline
except ImportError:
    print("you need to install cogcomp nlpy")
    print("pip install cython")
    print("sudo apt-get install openjdk-8-jdk")
    print("pip install ccg_nlpy")
    print("")
    print("install maven: https://maven.apache.org/install.html")
    print("and download the models: python -m ccg_nlpy download")
    raise


class CogcompNER(NERWrapper):
    def __init__(self, ontonotes=True):
        super().__init__()
        self.connl = not ontonotes
        self.ontonotes = ontonotes
        self.pipeline = local_pipeline.LocalPipeline()
        self.add_detector(self.annotate)

    def annotate(self, text, pretokenized=False):
        doc = self.pipeline.doc(text, pretokenized=pretokenized)
        if doc is not None:
            cons_list = []
            if self.connl:
                ents = doc.get_ner_conll
                if ents.cons_list:
                    cons_list += ents.cons_list
            elif self.ontonotes:
                ents = doc.get_ner_ontonotes
                if ents.cons_list:
                    cons_list += ents.cons_list
            for e in cons_list:
                yield Entity(e["tokens"],
                             e["label"],
                             source_text=text,
                             data=e)


if __name__ == "__main__":

    ner = CogcompNER()  # use ontonotes model
    # ner = CogcompNER(ontonotes=False)  # use connl model

    text = """"Helicopters will patrol the temporary no-fly zone around 
    New Jersey's MetLife Stadium Sunday, with F-16s based in Atlantic City 
    ready to be scrambled if an unauthorized aircraft does enter the 
    restricted airspace"""

    for r in ner.extract_entities(text):
        print(r.value, r.entity_type)
        """
        New Jersey 's GPE
        MetLife Stadium ORG
        Sunday DATE
        Atlantic City GPE
        """

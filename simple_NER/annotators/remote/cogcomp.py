from simple_NER.annotators import NERWrapper
from simple_NER import Entity

try:
    from ccg_nlpy import remote_pipeline
except ImportError:
    print("you need to install cogcomp nlpy")
    print("pip install cython")
    print("sudo apt-get install openjdk-8-jdk")
    print("pip install ccg_nlpy")
    raise


class CogcompNER(NERWrapper):
    def __init__(self, host=None, ontonotes=True):
        super().__init__()
        self.host = host
        self.connl = not ontonotes
        self.ontonotes = ontonotes
        self.pipeline = remote_pipeline.RemotePipeline(server_api=host)
        self.add_detector(self.annotate)

    def annotate(self, text):
        doc = self.pipeline.doc(text, pretokenized=False)
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

    # you may use you own server, demo is limited to 100 queries/day
    host = None
    ner = CogcompNER(host) # use ontonotes model
    # ner = CogcompNER(host, ontonotes=False)  # use connl model

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

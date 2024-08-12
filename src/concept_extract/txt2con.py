from rdflib import Graph
import os
from sentence_transformers import SentenceTransformer

from term_embd import graph_parse


class con_extr():

    def __init__(self, gsm_dscrp : dict, go_path : str, use_vpn = False) -> None:
        if use_vpn:
            os.environ["http_proxy"] = "http://127.0.0.1:7890"
            os.environ["https_proxy"] = "http://127.0.0.1:7890"
            
        self.gsm2dscrp = gsm_dscrp
        self.graph = Graph()
        print('\n----- parsing GO owl -----')
        self.graph.parse(go_path)
        print('----- GO owl parse completed -----\n')

        self.gsm_embeddings = []
        self.term_embeddings = []

        self.embd_model = SentenceTransformer("all-MiniLM-L6-v2")

    def txt_embd(self):
        pass

    def term_embd(self, label_predicates = None):
        con_descrp = graph_parse(self.graph)


    def similar(self):
        pass

    def get_unlabel(self):
        # TODO: unlabel instances?
        pass

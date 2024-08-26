from rdflib import Graph
import numpy as np
import os
from sentence_transformers import SentenceTransformer

from term_embd import graph_parse


class EmbeddingConverter():

    def __init__(self, owl_path : str, use_vpn = False) -> None:
        if use_vpn:
            os.environ["http_proxy"] = "http://127.0.0.1:7890"
            os.environ["https_proxy"] = "http://127.0.0.1:7890"
            
        #self.text_dict = text_dict

        self.graph = Graph()
        print('\n----- parsing owl -----')
        self.graph.parse(owl_path)
        print('----- owl parse completed -----\n')

        self.embd_model = SentenceTransformer("all-MiniLM-L6-v2")

        self.term_dict = graph_parse(self.graph)
        texts = list(self.term_dict.values())
        self.term_embeddings = self.embd_model.encode(texts)
        self.text_embeddings = []

        self.sim = None


    def similar_matrix(self, text : str):
        #keys = list(self.text_dict.keys())
        #texts = list(self.text_dict.values())
        text_embeddings = self.embd_model.encode([text])
        self.text_embeddings = text_embeddings

        #self.sim = self.embd_model.similarity(text_embeddings, self.term_embeddings)
        return self.sim


    def max_sim(self, top_cnt : int, sim_mat = None):
        if sim_mat == None:
            sim_mat = self.sim
        if sim_mat == None:
            raise Exception('need to specify similarity matrix')

        if len(sim_mat[0]) != len(self.term_dict.keys()):
            raise Exception('similarity matrix should have same length with concept dict')

        _, sorted_term = zip(*sorted(zip(sim_mat[0], self.term_dict.keys()), reverse=True))

        return sorted_term[:top_cnt]
        #max_idx = np.argmax(self.sim, axis=1)
        #max_con = [(list(self.term_dict.keys())[i], list(self.term_dict.values())[i]) for i in max_idx]
        #print(max_con)

    def get_con_desc(self, c : str):
        return self.term_dict[c]

    def get_term_embd(self):
        return self.term_embeddings

    def get_text_embd(self):
        return self.text_embeddings

    def get_unlabel(self):
        # TODO: unlabel instances?
        pass

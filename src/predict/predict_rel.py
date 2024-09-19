import sys, getopt
import pandas as pd
import joblib
import glob
import re
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
import os
from sentence_transformers import SentenceTransformer
#from graph_plot import graph_plot

def predict(in_pth, out_dir, rel_gene_lst):
    ##################################################
    
    ''' initialize text embedding converter '''
    os.environ["http_proxy"] = "http://127.0.0.1:7890"
    os.environ["https_proxy"] = "http://127.0.0.1:7890"
    embd_model = SentenceTransformer("all-MiniLM-L6-v2")
    term_embeddings = np.load('dataset/embedding/go_txt_embd.npy')
    with open('dataset/embedding/go_embd_idx.txt', 'r') as f:
        term_idx = eval(f.readline())

    
    ''' initialize concept lists '''
    TOP_CNT = 10
    concepts = []
    #con_descps = [[] for _ in range(TOP_CNT)]
    
    ''' read descriptions from input file '''
    descriptions = []
    n_inputs = 0
    with open(in_pth, 'r') as f:
        descriptions = f.readlines()
        n_inputs = len(descriptions)
    
    ''' iterate instances '''
    for i, d in enumerate(descriptions):
            ''' compute similarity matrix & most similar concept list '''
            #sim = embd.similar_matrix(d)
            text_embeddings = embd_model.encode(d)
            sim = embd_model.similarity(text_embeddings, term_embeddings)
            #sorted_sim = embd.max_sim(TOP_CNT)
            _, sorted_term = zip(*sorted(zip(sim[0], term_idx), reverse=True))
    
            concepts.append(list(sorted_term[:TOP_CNT]))

    ''' TMP: print concept - label list of inputs '''
    with open('dataset/concepts/concept_label.txt', 'r') as f:
        concept_label = eval(f.readline())
    with open('predict/results/res_concepts.txt', 'w') as f:
        for i, c_lst in enumerate(concepts):
            f.write(f'input concepts of experiment {i}:\n')
            for c in c_lst:
                f.write(f'{c} - {concept_label[c]}\n')
            f.write('\n')
    with open('predict/results/res_concept_lst.txt', 'w') as f:
        f.write(str(concepts))
    
    ''' load gene - product mapping '''
    gene_mapping = {}
    with open('predict/gene_mapping.txt', 'r') as f:
        gene_mapping = eval(f.readline())

    ''' tmp: load concepts from target gene GOA '''
    #with open('predict/plsm_goa/concept_lst.txt', 'r') as f:
    #    concepts = eval(f.readline())
    #with open('predict/prelim_concept_lst.txt', 'r') as f:
    #    concepts = eval(f.readline())
    
   ################################################## 
    
    ''' load pretrained model for each single gene '''
    models = []
    name_list = []
    model_files = glob.glob('models/SO_*_model.joblib')

    i = 1
    for gene_id in tqdm(range(1, 4759), 'loading pretrained models'):
    #for gene_id in [3077]:
        i += 1
        model_file = f'models/SO_{gene_id:04d}_model.joblib'
        name_list.append(f'SO_{gene_id:04d}')
        if model_file in model_files:
            model = joblib.load(model_file)
            models.append(model)
        else:
            models.append(None)  

    ''' predict for each input with pretrained model '''
    #for i in tqdm(range(n_inputs), 'processing input'):
    for i in range(n_inputs):

        concept_ids = [int(re.sub(r'GO_*', '', c)) for c in concepts[i]]
        
        predictions = []
        for model in models:
            if model is not None:
                prediction = model.predict_proba([concept_ids])[0]
                predictions.append(prediction)
            else:
                predictions.append([0,0])
        
        ''' zip name & pred prob as lst '''
        result = [(name, pred[1]) for name, pred in zip(name_list, predictions)]
        result.sort(key= lambda x: x[1], reverse=True)
        
        with open(f'{out_dir}/res_{i}.txt', 'w') as f:
            f.write('gene_id\tconf\tproduct\n')
            for g in result:
                #prod = gene_mapping[g[0]]
                #if 'unknown' in prod or 'uncharacterized' in prod:
                #    continue
                if g[0] not in gene_mapping.keys():
                    continue
    
                f.write(f'{g[0]}\t{g[1]:.2f}\t{gene_mapping[g[0]]}\n')

            #f.write('----------\n')

            #for g in result:
            #    if g[0] in rel_gene_lst:
            #        f.write(f'{g[0]}\t{g[1]:.2f}\t{gene_mapping[g[0]]}\n')

        #''' plot the regulation graph '''
        #pred_res = [g[0] for g in result[:20]]
        #graph_plot(pred_res, f'{out_dir}/res_{i}_graph.png', False)


################################################################################################

def main(argv):

    ''' parse in & out arg '''

    in_pth = 'predict/input.txt'
    out_dir = 'predict/results'
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","odir="])
    except getopt.GetoptError:
        print ('test.py -i <input_dir> -o <output_dir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -i <input_file> -o <output_dir>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            in_pth = arg
        elif opt in ("-o", "--odir"):
            out_dir = arg

    with open('predict/rel_gene_lst.txt', 'r') as f:
        rel_gene_lst = eval(f.readline())

    with open('predict/wetlab_gene_lst.txt', 'r') as f:
        rel_gene_lst = rel_gene_lst.union(eval(f.readline()))
    
    predict(in_pth, out_dir, rel_gene_lst)
    

    ##################################################

if __name__ == "__main__":
    main(sys.argv[1:])

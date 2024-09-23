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
from pywebio.input import select, input
from pywebio.output import *
from graph_plot import graph_plot

def predict(in_pth, out_dir, use_gui=False, use_embd=True):
    ##################################################
    
    if use_embd:
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
        
        if use_gui:
            put_text('Read description from input:')
            put_processbar('description')
        ''' iterate instances '''
        for i, d in enumerate(descriptions):
                set_processbar('description',i/len(descriptions))
                ''' compute similarity matrix & most similar concept list '''
                #sim = embd.similar_matrix(d)
                text_embeddings = embd_model.encode(d)
                sim = embd_model.similarity(text_embeddings, term_embeddings)
                #sorted_sim = embd.max_sim(TOP_CNT)
                _, sorted_term = zip(*sorted(zip(sim[0], term_idx), reverse=True))
        
                concepts.append(list(sorted_term[:TOP_CNT]))
    else:
        ''' input concepts directly '''
        concepts = [[]]
        n_inputs = 1
        with open(in_pth, 'r') as f:
            for i in range(10):
                concepts[0].append(f.readline())

    if use_gui:
        set_processbar('description', 1)
    
    ''' load gene - product mapping '''
    gene_mapping = {}
    with open('predict/gene_mapping.txt', 'r') as f:
        gene_mapping = eval(f.readline())
    
   ################################################## 
    
    ''' load pretrained model for each single gene '''
    models = []
    name_list = []
    model_files = glob.glob('models/SO_*_model.joblib')

    if use_gui:
        put_text('Load model for single gene:')
        put_processbar('loading')
    i = 1
    for gene_id in tqdm(range(1, 4759), 'loading pretrained models'):
        if use_gui:
            set_processbar('loading',i/4759)
        i += 1
        model_file = f'models/SO_{gene_id:04d}_model.joblib'
        name_list.append(f'SO_{gene_id:04d}')
        if model_file in model_files:
            model = joblib.load(model_file)
            models.append(model)
        else:
            models.append(None)  
    if use_gui:
        set_processbar('loading',1)

    ''' predict for each input with pretrained model '''
    if use_gui:
        put_text('Processing input:')
        put_processbar('processing')
    for i in tqdm(range(n_inputs), 'processing input'):
        if use_gui:
            set_processbar('processing',i/n_inputs)
        concept_ids = [int(re.sub(r'GO_0*', '', c)) for c in concepts[i]]
        
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
            for g in result[:20]:
                prod = gene_mapping[g[0]]
                if 'unknown' in prod or 'uncharacterized' in prod:
                    continue
    
                f.write(f'{g[0]}\t{g[1]:.2f}\t{gene_mapping[g[0]]}\n')


        ''' plot the regulation graph '''
        graph_plot(f'{out_dir}/res_{i}.txt', f'{out_dir}/res_{i}_graph.png', False)
    if use_gui:
        set_processbar('processing',1)


################################################################################################

def main(argv):

    ''' parse in & out arg '''

    in_pth = 'predict/input.txt'
    out_dir = 'predict/results'
    use_embd = True
    try:
        opts, args = getopt.getopt(argv,"hd:i:o:",["direct_mode=","ifile=","odir="])
    except getopt.GetoptError:
        print ('test.py -i <input_dir> -o <output_dir>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print ('test.py -d <optional for direct mode> -i <input_file> -o <output_dir>')
            sys.exit()
        elif opt in ("-i", "--ifile"):
            in_pth = arg
        elif opt in ("-o", "--odir"):
            out_dir = arg
        elif opt in ("-d", "--direct_mode"):
            use_embd = not eval(arg)
            #TODO: remove required input value

    
    predict(in_pth, out_dir, use_embd=use_embd)
    

    ##################################################

if __name__ == "__main__":
    main(sys.argv[1:])

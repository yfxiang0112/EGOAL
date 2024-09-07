import argparse
import os
import os.path as osp
from types import NoneType

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from ablkit.bridge import SimpleBridge
from ablkit.data.evaluation import ReasoningMetric, SymbolAccuracy
from ablkit.learning import ABLModel
from ablkit.reasoning import Reasoner
from ablkit.utils import ABLLogger, avg_confidence_dist, print_log, tab_data_to_tuple

from joblib import dump
from manage_dataset import load_and_process_dataset,split_dataset
from kb import GO
import tqdm
import time

''' consistency score = confidence + rule weights '''
def consitency(data_example, candidates, candidate_idxs, reasoning_results):
    pred_prob = data_example.pred_prob
    model_scores = avg_confidence_dist(pred_prob, candidate_idxs)
    rule_scores = np.array(reasoning_results)
    scores = model_scores + rule_scores
    return scores

'''
def print_log(message, logger=sg_logger, log_file_path=None):
    print(message)
    if log_file_path:
        with open(log_file_path, 'a') as log_file:
            log_file.write(message + '\n')
'''
def build_log(sg_name:str) -> ABLLogger:

    local_time = time.strftime("%Y%m%d_%H_%M_%S", time.localtime())
    
    log_dir = os.path.join('log', sg_name)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = osp.join(log_dir, local_time + ".log")

    return ABLLogger(f'{sg_name}-log', log_file=log_file)
            
##########################################################

def train(id: int):
    sg_logger = build_log(f'SO_{(id+1):04}')

    print_log("---------------------- Single gene training start --------------------------------", logger=sg_logger)

    ''' Specify gene name of each round ''' 
    sg_idx = id
    sg_name = f'SO_{(sg_idx+1):04}'

    #TODO: handle argument parse
    parser = argparse.ArgumentParser(description="GO example")
    parser.add_argument(
        "--loops", type=int, default=3, help="number of loop iterations (default : 3)"
    )
    args = parser.parse_args()


    # TODO: integrate path into argparse
    annotation_path = 'rules/goa_gene2go.csv'
    rule_path = 'rules/single_genes/' + sg_name + '_sg_rule.csv'
    #rule_path = 'rules/ruleConFree.csv'

    if not os.path.exists(rule_path):
        ''' skip if ruleset not exists '''
        print_log(f'Skipped train of gene {sg_name}: rule set not found')
        return


    ''' Build Logger '''
    print_log(f"Abductive Learning on single gene {sg_name}.", logger=sg_logger)


    ''' Split dataset with current single gene column '''
    print_log("Working with Data.", logger=sg_logger)

    X, y, X_u, y_u = load_and_process_dataset(sg_name)

    if type(X) == NoneType:
        ''' skip if current gene not exists '''
        print_log(f'Skipped train of gene {sg_name}: not in data column')
        return

    X_label, y_label, X_unlabel, y_unlabel, X_test, y_test = split_dataset(X, y, X_u, y_u, test_size=0.5) 
    label_data = tab_data_to_tuple(X_label, y_label)
    test_data = tab_data_to_tuple(X_test, y_test)
    train_data = tab_data_to_tuple(X_unlabel, y_unlabel)

    
    ''' Build base model(Here we could change the basic model we use) ''' 
    print_log("Building the Learning Part.", logger=sg_logger)
    base_model = RandomForestClassifier()
    # base_model = SVC()
    

    ''' Initialize ABL model '''
    model = ABLModel(base_model)


    ''' Build KB & reasoner based on defined GO rules '''
    print_log("Building the Reasoning Part.", logger=sg_logger)

    try:
        kb = GO(sg_name, rule_path, annotation_path, logger=sg_logger)
    except FileNotFoundError:
        print(f"Rule file not found: {rule_path}. Skipping...")
        return 

    reasoner = Reasoner(kb, dist_func=consitency, idx_to_label=None)


    ''' Build Evaluation Metrics '''
    print_log("Building Evaluation Metrics.", logger=sg_logger)
    metric_list = [SymbolAccuracy(prefix="GO"), ReasoningMetric(kb=kb, prefix="GO")]


    ''' Initialize learning & reasoning bridge '''
    print_log("Bridge Learning and Reasoning.", logger=sg_logger)
    bridge = SimpleBridge(model, reasoner, metric_list)


    ''' Pretrain & test base model '''
    print_log("------- Use labeled data to pretrain the model -----------", logger=sg_logger)
    base_model.fit(X_label, y_label)
    #res = base_model.predict(X_unlabel)
    #prob = base_model.predict_proba(X_unlabel)

    print_log("------- Test the initial model -----------", logger=sg_logger)
    bridge.test(test_data, logger=sg_logger)

    ''' Train model with ABL '''
    print_log("------- Use ABL to train the model -----------", logger=sg_logger)
    bridge.train(
        train_data=train_data,
        label_data=label_data,
        loops=args.loops,
        segment_size=len(X_unlabel),
        logger=sg_logger
    )
    print_log("------- Test the final model -----------", logger=sg_logger)
    bridge.test(test_data, logger=sg_logger)


    print_log("------- Save the final model -----------", logger=sg_logger)
    ''' Save the model '''
    model_dir = 'models'
    if not os.path.exists(model_dir):
        os.makedirs(model_dir)

    model_path = f'models/{sg_name}_model.joblib'
    dump(base_model, model_path)

    print_log("---------------------- Single gene training end --------------------------------", logger=sg_logger)

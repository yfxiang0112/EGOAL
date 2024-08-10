import argparse
import os.path as osp

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from ablkit.bridge import SimpleBridge
from ablkit.data.evaluation import ReasoningMetric, SymbolAccuracy
from ablkit.learning import ABLModel
from ablkit.reasoning import Reasoner
from ablkit.utils import ABLLogger, avg_confidence_dist, print_log, tab_data_to_tuple

from manage_dataset import load_and_process_dataset,split_dataset
from kb import GO
import tqdm

# From example Zoo, maybe help.
def consitency(data_example, candidates, candidate_idxs, reasoning_results):
    pred_prob = data_example.pred_prob
    model_scores = avg_confidence_dist(pred_prob, candidate_idxs)
    rule_scores = np.array(reasoning_results)
    scores = model_scores + rule_scores
    # print(scores)
    return scores

def main():
    parser = argparse.ArgumentParser(description="GO example")
    # Add argument loops of the test, here is 3
    parser.add_argument(
        "--loops", type=int, default=3, help="number of loop iterations (default : 3)"
    )
    # TODO() Add other argument we need:
    args = parser.parse_args()
    #TODO: added to argparse
    rule_path = 'rules/ruleConFree.csv'
    annotation_path = 'rules/goa_gene2go.csv'
    domain_path = 'dataset/concepts/concept_domain.csv'

    # Build logger
    print_log("Abductive Learning on the GO example.", logger="current")

    # -- Working with Data ------------------------------
    print_log("Working with Data.", logger="current")

    X, y = load_and_process_dataset()
    # TODO() need to complete the function
    X_label, y_label, X_unlabel, y_unlabel, X_test, y_test = split_dataset(X, y, test_size=0.2) 
    label_data = tab_data_to_tuple(X_label, y_label)
    test_data = tab_data_to_tuple(X_test, y_test)
    train_data = tab_data_to_tuple(X_unlabel, y_unlabel)
    # print(type(label_data), type(test_data), type(train_data))
    # assert(0)

    # -- Building the Learning Part ---------------------
    print_log("Building the Learning Part.", logger="current")
    
    # Build base model(Here we could change the basic model we use)
    # base_model = RandomForestClassifier()
    base_model = SVC()
    
    # Build ABLModel
    model = ABLModel(base_model)



    # -- Building the Reasoning Part --------------------
    print_log("Building the Reasoning Part.", logger="current")

    # Build knowledge base
    kb = GO(rule_path, annotation_path, domain_path)
    
    # Create reasoner(need to complete the consistency function)
    reasoner = Reasoner(kb, dist_func=consitency, idx_to_label=None)



    # -- Building Evaluation Metrics --------------------
    print_log("Building Evaluation Metrics.", logger="current")
    metric_list = [SymbolAccuracy(prefix="GO"), ReasoningMetric(kb=kb, prefix="GO")]

    # -- Bridging Learning and Reasoning ----------------
    print_log("Bridge Learning and Reasoning.", logger="current")
    bridge = SimpleBridge(model, reasoner, metric_list)


    # Performing training and testing
    # Need to complete
    print_log("------- Use labeled data to pretrain the model -----------", logger="current")
    #print('\n\n', X_label, '\n', y_label)
    base_model.fit(X_label, y_label)
    #res = base_model.predict(X_unlabel)
    #print(res.shape)
    #prob = base_model.predict_proba(X_unlabel)
    #print(prob, type(prob))
    #for arr in prob:
    #    print(arr.shape, arr[0].shape)
    print_log("------- Test the initial model -----------", logger="current")
    # print(type(test_data))
    # print(test_data)
    # test_data = np.array(list(test_data))
    bridge.test(test_data)
    print_log("------- Use ABL to train the model -----------", logger="current")
    bridge.train(
        train_data=train_data,
        label_data=label_data,
        loops=args.loops,
        segment_size=len(X_unlabel),
    )
    print_log("------- Test the final model -----------", logger="current")
    bridge.test(test_data)

if __name__ == "__main__":
    main()

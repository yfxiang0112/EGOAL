import argparse
import os.path as osp

import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC

from ablkit.bridge import SimpleBridge
from ablkit.data.evaluation import ReasoningMetric, SymbolAccuracy
from ablkit.learning import ABLModel
from ablkit.reasoning import Reasoner
from ablkit.utils import ABLLogger, avg_confidence_dist, print_log, tab_data_to_tuple

from manage_dataset import load_and_process_dataset, split_dataset
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

# Define a simple neural network model
class SimpleNN(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_dim, hidden_dim)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_dim, output_dim)
    
    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out
    
    def fit(self, X, y, epochs=10, batch_size=32, lr=0.001):
        optimizer = optim.Adam(self.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()
        
        X_tensor = torch.tensor(X, dtype=torch.float32)
        y_tensor = torch.tensor(y, dtype=torch.long)
        
        for epoch in range(epochs):
            for i in range(0, len(X), batch_size):
                X_batch = X_tensor[i:i+batch_size]
                y_batch = y_tensor[i:i+batch_size]
                
                optimizer.zero_grad()
                outputs = self(X_batch)
                loss = criterion(outputs, y_batch)
                loss.backward()
                optimizer.step()
    
    def predict(self, X):
        X_tensor = torch.tensor(X, dtype=torch.float32)
        with torch.no_grad():
            outputs = self(X_tensor)
            _, predicted = torch.max(outputs, 1)
        return predicted.numpy()

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
    input_dim = X_label.shape[1]
    hidden_dim = 128
    output_dim = len(np.unique(y_label))
    base_model = SimpleNN(input_dim, hidden_dim, output_dim)
    
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
    # Convert data to torch tensors
    X_label_tensor = torch.tensor(X_label, dtype=torch.float32)
    y_label_tensor = torch.tensor(y_label, dtype=torch.long)
    X_unlabel_tensor = torch.tensor(X_unlabel, dtype=torch.float32)
    y_unlabel_tensor = torch.tensor(y_unlabel, dtype=torch.long)
    X_test_tensor = torch.tensor(X_test, dtype=torch.float32)
    y_test_tensor = torch.tensor(y_test, dtype=torch.long)

    # Define optimizer and loss function
    optimizer = optim.Adam(base_model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    # Pretrain the model
    base_model.train()
    for epoch in range(10):  # Number of epochs for pretraining
        optimizer.zero_grad()
        outputs = base_model(X_label_tensor)
        loss = criterion(outputs, y_label_tensor)
        loss.backward()
        optimizer.step()

    print_log("------- Test the initial model -----------", logger="current")
    base_model.eval()
    with torch.no_grad():
        test_outputs = base_model(X_test_tensor)
        _, predicted = torch.max(test_outputs, 1)
        accuracy = (predicted == y_test_tensor).sum().item() / y_test_tensor.size(0)
        print_log(f"Initial test accuracy: {accuracy}", logger="current")

    print_log("------- Use ABL to train the model -----------", logger="current")
    bridge.train(
        train_data=train_data,
        label_data=label_data,
        loops=args.loops,
        segment_size=len(X_unlabel),
    )

    print_log("------- Test the final model -----------", logger="current")
    base_model.eval()
    with torch.no_grad():
        test_outputs = base_model(X_test_tensor)
        _, predicted = torch.max(test_outputs, 1)
        accuracy = (predicted == y_test_tensor).sum().item() / y_test_tensor.size(0)
        print_log(f"Final test accuracy: {accuracy}", logger="current")

if __name__ == "__main__":
    main()
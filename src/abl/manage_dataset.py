import numpy as np
import pandas as pd
from ablkit.utils import ABLLogger, avg_confidence_dist, print_log, tab_data_to_tuple
import random

# Function to load and process the dataset
def load_and_process_dataset():
    '''
    Input:
        None

    Output:
        X: features after process, list
        y: labels after process, list
    '''
    # Read all datasets
    df_1 = pd.read_csv('../../dataset/importance/processed_dataset_with_importance.csv')
    df_2 = pd.read_csv('../../dataset/concepts/concept_domain.csv')

    # Change into numpy
    # Extract the features
    X_init = df_1.iloc[:, 1:2].values
    # Extract the importance values (20 columns starting from the 103rd column)
    y_init = df_1.iloc[:, 102:122].values
    
    # Change X and y form
    X = [eval(item[0]) for item in X_init]
    y = [[eval(item) for item in sublist] for sublist in y_init]

    # Add ramdom 20 concepts as pseudo label
    selected_concepts = df_2.sample(n=20, replace=False).values.flatten().tolist()
    selected_concepts_formatted = [[concept] for concept in selected_concepts]
    X.extend(selected_concepts_formatted)

    # print(type(X), type(y))
    # X = np.array(X)
    return X, y

def split_dataset(X, y, test_size=0.2):
    '''
    Input:
        X: features, list
        y: labels, list of tuples
        test_size: float

    Output:
        X_label: features with label, list
        y_label: labels with label, list
        X_unlabel: features without label, list
        y_unlabel: labels without label, list
        X_test: test features with label, list
        y_test: test labels with label, list
    '''
    # 1. Initialize label_indices, unlabel_indices, test_indices.
    label_indices, unlabel_indices, test_indices = [], [], []
    
    # 2. Convert tuples to hashable strings
    labels = [str(item) for item in y]
    
    # 3. Compute the labels, unlabels, and test indices for each class
    unique_labels = list(set(labels))
    for class_label in unique_labels:
        idxs = [i for i, label in enumerate(labels) if label == class_label]
        random.shuffle(idxs)
        n_train_unlabel = int((1 - test_size) * (len(idxs) - 1))
        label_indices.append(idxs[0])
        unlabel_indices.extend(idxs[1 : 1 + n_train_unlabel])
        test_indices.extend(idxs[1 + n_train_unlabel :])
    
    # 4. Extract the corresponding features and labels
    X_label = [X[i] for i in label_indices]
    y_label = [y[i] for i in label_indices]
    X_unlabel = [X[i] for i in unlabel_indices]
    y_unlabel = [y[i] for i in unlabel_indices]
    X_test = [X[i] for i in test_indices]
    y_test = [y[i] for i in test_indices]
    
    return X_label, y_label, X_unlabel, y_unlabel, X_test, y_test


# X, y = load_and_process_dataset()
# X_label, y_label, X_unlabel, y_unlabel, X_test, y_test = split_dataset(X, y, test_size=0.2) 
# label_data = tab_data_to_tuple(X_label, y_label)
# test_data = tab_data_to_tuple(X_test, y_test)
# train_data = tab_data_to_tuple(X_unlabel, y_unlabel)
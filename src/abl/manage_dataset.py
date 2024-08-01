import numpy as np
import pandas as pd

# Function to load and process the dataset
def load_and_process_dataset():
    '''
    Input:
        None

    Output:
        X: features after process, numpy array
        y: labels after process, numpy array
    '''
    # Read all datasets
    df_1 = pd.read_csv('../../dataset/importance/processed_dataset_with_importance.csv')
    df_2 = pd.read_csv('../../dataset/concepts/all_concept_name.txt', header=None)

    # Change into numpy
    # Extract the features
    X_init = df_1.iloc[:, 1:2].values
    # Extract the importance values (20 columns starting from the 103rd column)
    y_init = df_1.iloc[:, 102:122].values
    
    X = [eval(item[0]) for item in X_init]
    # print(X)
    # print(y_init)
    y = [[eval(item) for item in sublist] for sublist in y_init]
    print(y)
    # print(selected_concepts)
    return X, y

# Function to split the data:
def split_dataset(X, y, test_size = 0.2):
    '''
    Input:
        X: features, numpy array
        y: labels, numpy array
        test_size: float

    Output:
        X_label: features with label, numpy array
        y_label: labels with label, numpy array
        X_unlabel: features without label, numpy array
        y_unlabel: labels without label, numpy array
        X_test: test features with label, numpy array
        y_test: test labels with label, numpy array
    '''
    # TODO()
    # 1.Initial labels_indices, unlabel_indices, test_indices.

    # 2.Compute the labels, 

    X_label, y_label = [], []
    X_unlabel, y_unlabel = [], []
    X_test, y_test = [], []
    return X_label, y_label, X_unlabel, y_unlabel, X_test, y_test


load_and_process_dataset()
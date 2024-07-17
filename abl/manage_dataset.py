import numpy as np

# Function to load and process the dataset
def load_and_process_dataset():
    '''
    Input:
        None

    Output:
        X: features after process, numpy array
        y: labels after process, numpy array
    '''
    # Change into numpy
    # TODO()
    
    X, y = X.to_numpy(), y.to_numpy()
    return X, y

# Function to split the data:
def split_dataset(X, y, test_size = 0.2):
    '''
    Input:
        X: features, numpy array
        y: labels, numpy array
        test_size: int

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
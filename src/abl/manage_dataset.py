import numpy as np
import pandas as pd
from ablkit.utils import ABLLogger, avg_confidence_dist, print_log, tab_data_to_tuple
import random
import re

from geneset2idx import label2idx

MAX_GENE_NUM = 4807

#class GeneSet():
#    def __init__(self, lst) -> None:
#        self.lst = list(lst)
#        self.idx = -1
#
#    def __hash__(self) -> int:
#        s = ''
#        for i in self.lst:
#            s += str(i)
#        return hash(s)
#
#    def __iter__(self):
#        return self
#
#    def __getitem__(self, index):
#        return self.lst[index]
#
#    def __next__(self):
#        self.idx += 1
#        if self.idx >= len(self.lst):
#            raise StopIteration
#        return self.lst[self.idx]
#
#    def __lt__(self, other):
#        return hash(self) < hash(other)

# Function to load and process the dataset
def filter_id_lst(lst):
    res = []
    for s in lst:
        res.append(filter_id(s))
    return np.array(res)

def filter_id(s):
    #s = s[0] #NOTE:temp
    p = r'\d+'
    res = re.findall(p,s)
    if len(res) != 1:
        print(s, res)
        raise Exception('invalid ID')
    return int(res[0])

def load_and_process_dataset():
    '''
    Input:
        None

    Output:
        X: features after process, numpy array 
        y: labels after process, numpy array 
    '''
    # Read all datasets
    #df_1 = pd.read_csv('dataset/one-hot/one_hot_pro_y.csv')
    df_1 = pd.read_csv('dataset/importance/processed_dataset_with_importance.csv')
    # print(df_1)

    # Change into numpy
    # Extract the features
    # print(df_1.iloc[:, 1:2])
    #X_init = df_1.iloc[:, 1: 2].map(eval).map(filter_id_lst)
    X_init = df_1.iloc[:,1].apply(eval).apply(filter_id_lst)
    #y_init = df_1.iloc[:, 102:].map(lambda x:eval(x)[0]).map(filter_id)
    y_init = df_1.iloc[:, 102:104].map(lambda x:eval(x)[0]).map(filter_id)

    #X, y = X_init.to_numpy(), y_init.to_numpy()
    X = np.array(list(X_init))
    y = y_init.to_numpy()
    y = np.array([label2idx(row) for row in y])
    print('X_init=\n', X)
    print('y_init=\n', y)
    print(X.shape, y.shape)
    for row in X:
        for elem in row:
            assert(type(elem) == np.int64)
    #for row in y:
    #    for elem in row:
    #        assert(type(elem) == np.int64)
    return X, y

def split_dataset(X, y, test_size=0.3):
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
    # X = X.astype(np.int8)
    # y = y.astype(np.int8)
    # print(type(X),type(y)) <class 'numpy.ndarray'> <class 'numpy.ndarray'>
    label_indices, unlabel_indices, test_indices = [], [], []
    for class_label in np.unique(y):
        idxs = np.where(y == class_label)[0]
        # print(np.unique(y))
        # print(idxs)
        np.random.shuffle(idxs)
        n_train_unlabel = int((1 - test_size) * (len(idxs) - 1))
        # print(n_train_unlabel, len(idxs))
        label_indices.append(idxs[0])
        unlabel_indices.extend(idxs[1 : 1 + n_train_unlabel])
       #  print(unlabel_indices)
        test_indices.extend(idxs[1 + n_train_unlabel :])
        # assert(0)
    X_label, y_label = X[label_indices], y[label_indices]
    #print('label', X_label, y_label)
    # assert(0)
    X_unlabel, y_unlabel = X[unlabel_indices], y[unlabel_indices]
    print('unlabel', X_unlabel, y_unlabel, X_unlabel.shape, y_unlabel.shape)
    # X_unlabel, y_unlabel = [0], [0]
    # print(X_unlabel, y_unlabel)
    # print(X_unlabel)
    X_test, y_test = X[test_indices], y[test_indices]
    #print('test', X_test, y_test)
    return X_label, y_label, X_unlabel, y_unlabel, X_test, y_test


if __name__ == '__main__':
    X, y = load_and_process_dataset()
    # print(X)
    # print(y)
    X_label, y_label, X_unlabel, y_unlabel, X_test, y_test = split_dataset(X, y, test_size=0.2) 
    label_data = tab_data_to_tuple(X_label, y_label)
    test_data = tab_data_to_tuple(X_test, y_test)
    train_data = tab_data_to_tuple(X_unlabel, y_unlabel)
    #print(label_data)
    #print(test_data)
    #print(X_test)
    #print(y_test)
    #print(type(X_test), type(X_test[0]))
    #print(train_data)
    # X_label, y_label, X_unlabel, y_unlabel, X_test, y_test = split_dataset(X, y, test_size=0.2) 
    # label_data = tab_data_to_tuple(X_label, y_label)
    # test_data = tab_data_to_tuple(X_test, y_test)
    # train_data = tab_data_to_tuple(X_unlabel, y_unlabel)
    # print(label_data)
    # print(test_data)
    # print(train_data)

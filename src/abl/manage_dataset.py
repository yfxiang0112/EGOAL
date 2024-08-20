import numpy as np
import pandas as pd
from ablkit.utils import ABLLogger, avg_confidence_dist, print_log, tab_data_to_tuple
import random
import re
import ast

''' ID preprocess utils '''
def filter_id_lst(lst):
    res = []
    for s in lst[:10]:
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

##########################################################


def load_and_process_dataset(sg_col : str):
    '''
    Input:
        sg_col, int 

    Output:
        X: features after process, numpy array 
        y: labels after process, numpy array 
    '''

    ''' Read all datasets '''
    # df_1 = pd.read_csv('dataset/importance/processed_dataset_with_importance.csv')
    df_1 = pd.read_csv('dataset/one-hot/one_hot_pro_y_allone.csv')

    ''' skip if current gene name not exists '''
    if sg_col not in df_1.columns:
        return None, None

    ''' convert list & bitmap dataset into np array '''
    X_init = df_1.iloc[:,2].apply(eval).apply(filter_id_lst)
    #y_init = df_1.iloc[:, 3729:]
    y_init = df_1.loc[:, sg_col]
    X = np.array(list(X_init))
    y = y_init.to_numpy()

    ''' get single gene label column of current gene id ''' 
    #y = y[:,sg_col]

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
    ''' Seperate the dataset into label, unlabel, test dataset '''
    label_indices, unlabel_indices, test_indices = [], [], []
    for class_label in np.unique(y):
        idxs = np.where(y == class_label)[0]
        np.random.shuffle(idxs)
        n_train_unlabel = int((1 - test_size) * (len(idxs) - 1))
        label_indices.append(idxs[0])
        unlabel_indices.extend(idxs[1 : 1 + n_train_unlabel])
        test_indices.extend(idxs[1 + n_train_unlabel :])

    X_label, y_label = X[label_indices], y[label_indices]
    X_unlabel, y_unlabel = X[unlabel_indices], y[unlabel_indices]
    X_test, y_test = X[test_indices], y[test_indices]

    ''' Convert their label into the abl form '''
    label_to_index = {label: index for index, label in enumerate(y_label)}

    for i in range(len(y_unlabel)):
        if y_unlabel[i] in label_to_index:
            y_unlabel[i] = label_to_index[y_unlabel[i]]

    for i in range(len(y_test)):
        if y_test[i] in label_to_index:
            y_test[i] = label_to_index[y_test[i]]

    for i in range(len(y_label)):
        if y_label[i] in label_to_index:
            y_label[i] = label_to_index[y_label[i]]
            
    #print('----------------------------------------------------')
    #print(len(y_label), y_label)
    #print('----------------------------------------------------')
    #print(len(y_unlabel),y_unlabel)
    #print('----------------------------------------------------')
    #print(len(y_test), y_test)
    #print('----------------------------------------------------')
    return X_label, y_label, X_unlabel, y_unlabel, X_test, y_test

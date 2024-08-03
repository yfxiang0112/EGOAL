import numpy as np
#TODO: handle id SO_Axxxx

#class IdxConvert():
#    def __init__(self) -> None:
MAX_GENE_ID = 4807
GENE_SET_LEN = 2
MAX_LABEL_IDX = MAX_GENE_ID * GENE_SET_LEN
    
def label2idx(lst):
    if len(lst) != GENE_SET_LEN:
        raise Exception('length of label error')
    idx = np.int64(0)
    for d in lst:
        idx += (d-1)
        idx *= MAX_GENE_ID
    return idx

def idx2label(idx):
    lst = []
    for i in range(GENE_SET_LEN):
        id_val = idx % MAX_GENE_ID + 1
        idx /= MAX_GENE_ID
        lst.insert(0, id_val)
    return lst

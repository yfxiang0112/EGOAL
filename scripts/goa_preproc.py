import pandas as pd
import re
import numpy as np

def find_id(s):
    s = str(s)
    pattern = r'SO_A*\d+'
    res = re.findall(pattern, s)

    #if len(res) == 1:
    #    return res[0]
    #else:
    #    print(res)
    #    return np.NaN
    return res

goa = pd.read_csv('rules/S_oneidensis.goa.csv', header=None, on_bad_lines='skip')
goa_mapping = pd.concat([goa[4], goa[10].apply(find_id)], axis=1)
print(goa_mapping)
goa_mapping.to_csv('rules/goa_mapping.csv', header=False, index=False)

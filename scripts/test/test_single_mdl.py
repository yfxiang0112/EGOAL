import os
import pandas as pd
import joblib
import re
from tqdm import tqdm

dataset = pd.read_csv('dataset/importance/dataset_onehot.csv')

gene = 'SO_0030'
model_file = f'models/{gene}_model.joblib'
model = joblib.load(model_file)

pred_cnt = 0
for i,row in dataset.iterrows():
    concepts = eval(row['CONCEPTS'])
    concept_ids = [int(re.sub(r'GO_0*', '', c)) for c in concepts]
    prediction = model.predict_proba([concept_ids])[0]
    #print(prediction[1])
    if prediction[1] > .5:
        pred_cnt += 1

    if prediction[1] > 0:
        print(prediction)

print(pred_cnt)
print(dataset[gene].sum())

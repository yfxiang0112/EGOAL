import os
import pandas as pd
import joblib
import re
from tqdm import tqdm

dataset = pd.read_csv('dataset/importance/dataset_onehot.csv')

gene = 'SO_1523'
model_file = f'models/{gene}_model.joblib'
model = joblib.load(model_file)

pred_cnt = 0
pred_95_cnt = 0
for i,row in dataset.iterrows():
    concepts = eval(row['CONCEPTS'])
    concept_ids = [int(re.sub(r'GO_0*', '', c)) for c in concepts]
    prediction = model.predict_proba([concept_ids])[0]
    #print(prediction[1])
    if prediction[1] > .5:
        pred_cnt += 1
    if prediction[1] > .95:
        pred_95_cnt += 1

    #if prediction[1] > 0:
    #    print(prediction)

print(pred_cnt)
print()
print(f'in gene {gene},\n{dataset[gene].sum()} positive results in {len(dataset)} dataset entries,\n{pred_cnt} predicted positive, {pred_95_cnt} with conf>0.95')

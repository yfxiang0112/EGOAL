import pandas as pd
import joblib
import glob
import re
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc

''' Preparation for data '''
df = pd.read_csv('dataset/one-hot/one_hot_pro_y_allone.csv')
df_subset = df.iloc[1, 2798:]

#input_concept = ['GO_0009631', 'GO_0042309', 'GO_0080190', 'GO_0080192', 'GO_0046079', 'GO_0140739', 'GO_0140454', 'GO_0106379', 'GO_0050825', 'GO_0010346']

input_concept = ['GO_0008976', 'GO_0039586', 'GO_0043751', 'GO_0016772', 'GO_0016781', 'GO_0017023', 'GO_0016776', 'GO_0061569', 'GO_0140358', 'GO_0016775']
input_concept_numbers = [int(re.sub(r'GO_0*', '', concept)) for concept in input_concept]

model_files = glob.glob('models/SO_*_model.joblib')
model_numbers = [int(file.split('_')[1]) for file in model_files]
model_numbers.sort()

models = []
name_list = []

for number in tqdm(range(1, 4759)):
    model_file = f'models/SO_{number:04d}_model.joblib'
    name_list.append(f'SO_{number:04d}')
    if model_file in model_files:
        model = joblib.load(model_file)
        models.append(model)
    else:
        models.append(None)  

predictions = []
for model in tqdm(models):
    if model is not None:
        prediction = model.predict([input_concept_numbers])[0]
        predictions.append(prediction)
    else:
        predictions.append(None)  

result = {name: pred for name, pred in zip(name_list, predictions)}
name_1 = [name for name, pred in result.items() if pred == 1]

''' Analysis '''
all_names = df_subset.keys()
#
## 初始化 TP, FN, FP, TN
expr = []
#FN = []
#FP = []
#TN = []
#
# 遍历所有样本
for name in all_names:
    actual = df_subset.get(name, 0)
    predicted = result.get(name, None)
    
    if predicted == 1:
        #if actual == 1:
        expr.append(name)
        #print(name)
        #else:
        #    FP.append(name)
        #    print(name)
    #else:
        #if actual == 1:
        #FN.append(name)
        #    print(name)
        #else:
        #    TN.append(name)
        #    print(name)
#
## 计算准确率
#accuracy = len(TP) / len(name_1) if name_1 else 0
#print(f'Accuracy: {accuracy:.2%}')
#
#accuracy_all_name = len(TP) + len(TN) / len(all_names)
#print(f'accuracy_all_name: {accuracy:.2%}')
## 定义文件名
output_file = 'src/predict/classification_results.txt'
# 写入文件
with open(output_file, 'w') as f:
#    f.write(f'Accuracy: {accuracy:.2%}\n')
#    f.write(f'accuracy_all_name: {accuracy:.2%}\n')
    f.write(f'Expressed Genes: {expr}\n')
    #f.write(f'False Negatives: {FN}\n')
#    f.write(f'False Positives: {FP}\n')
#    f.write(f'True Negatives: {TN}\n')
#
print(f'Results have been saved to {output_file}')
#
#''' Draw auc pic '''
#actual_values = [df_subset.get(name, 0) for name in all_names]
#predicted_probabilities = [result.get(name, None) for name in all_names]
#
## 确保预测概率不为 None
#predicted_probabilities = [p if p is not None else 0 for p in predicted_probabilities]
#
## 计算 ROC 曲线
#fpr, tpr, thresholds = roc_curve(actual_values, predicted_probabilities)
#
## 计算 AUC
#roc_auc = auc(fpr, tpr)
#
## 绘制 ROC 曲线
#plt.figure()
#plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
#plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
#plt.xlim([0.0, 1.0])
#plt.ylim([0.0, 1.05])
#plt.xlabel('False Positive Rate')
#plt.ylabel('True Positive Rate')
#plt.title('Receiver Operating Characteristic')
#plt.legend(loc="lower right")
#plt.savefig('src/predict/auc.png')
#plt.show()

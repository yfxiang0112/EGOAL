import pandas as pd
import joblib
import glob
import re
from tqdm import tqdm

df = pd.read_csv('dataset/one-hot/one_hot_pro_y_allone.csv')
df_subset = df.iloc[1, 2798:]

input_concept = ['GO_0009631', 'GO_0042309', 'GO_0080190', 'GO_0080192', 'GO_0046079', 'GO_0140739', 'GO_0140454', 'GO_0106379', 'GO_0050825', 'GO_0010346']
input_concept_numbers = [int(re.sub(r'GO_0*', '', concept)) for concept in input_concept]

model_files = glob.glob('models/SO_*_model.joblib')
model_numbers = [int(file.split('_')[1]) for file in model_files]
model_numbers.sort()

models = []
name_list = []

for number in range(1, 4759):
    model_file = f'models/SO_{number:04d}_model.joblib'
    name_list.append(f'SO_{number:04d}')
    if model_file in model_files:
        model = joblib.load(model_file)
        models.append(model)
    else:
        print(f'Warning: Model SO_{number:04d}_model.joblib not found.')
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

# 对比预测结果与实际值
correct_predictions = [name for name in name_1 if df_subset.get(name, 0) == 1]
print(correct_predictions)

# 计算准确率
accuracy = len(correct_predictions) / len(name_1) if name_1 else 0

print(f'Accuracy: {accuracy:.2%}')
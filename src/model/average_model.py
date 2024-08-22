import joblib
import glob
import numpy as np

model_files = glob.glob('models/SO_*_model.joblib')
model_numbers = [int(file.split('_')[1]) for file in model_files]
model_numbers.sort()

models = []
for number in range(1, 4759):  
    model_file = f'models/SO_{number:04d}_model.joblib'
    if model_file in model_files:
        model = joblib.load(model_file)
        models.append(model)
    else:
        print(f'Warning: Model SO_{number:04d}_model.joblib not found.')

def average_predict(models, X):
    predictions = np.array([model.predict(X) for model in models])
    return np.mean(predictions, axis=0)

joblib.dump(average_predict, 'ensemble_model/average_ensemble_model.joblib')
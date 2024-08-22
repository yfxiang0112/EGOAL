import joblib
import glob
from sklearn.ensemble import VotingClassifier

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

voting_classifier = VotingClassifier(estimators=[(f'model_{i}', model) for i, model in enumerate(models)], voting='hard')

joblib.dump(voting_classifier, 'ensemble_model/voting_ensemble_model.joblib')
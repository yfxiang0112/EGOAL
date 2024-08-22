import joblib
import glob
from sklearn.ensemble import StackingClassifier
from sklearn.linear_model import LogisticRegression

model_files = glob.glob('models/SO_*_model.joblib')
model_numbers = [int(file.split('_')[1]) for file in model_files]
model_numbers.sort()

models = []
for number in range(1, 4759):  # 从1到4758
    model_file = f'models/SO_{number:04d}_model.joblib'
    if model_file in model_files:
        model = joblib.load(model_file)
        models.append(model)
    else:
        print(f'Warning: Model SO_{number:04d}_model.joblib not found.')

stacking_classifier = StackingClassifier(
    estimators=[(f'model_{i}', model) for i, model in enumerate(models)],
    final_estimator=LogisticRegression()
)

joblib.dump(stacking_classifier, 'ensemble_model/stacking_ensemble_model.joblib')
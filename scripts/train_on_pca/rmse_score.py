import numpy as np
import pandas as pd

from sklearn.multioutput import MultiOutputRegressor

from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, MaxAbsScaler, PowerTransformer, \
    QuantileTransformer

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold

from sklearn.tree import DecisionTreeRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from xgboost import XGBRegressor
from sklearn.metrics import mean_squared_error

scalers = [
    ('StandardScaler', StandardScaler()),
    ('MinMaxScaler', MinMaxScaler()),
    ('RobustScaler', RobustScaler()),
    ('MaxAbsScaler', MaxAbsScaler()),
    ('PowerTransformer', PowerTransformer()),
    ('QuantileTransformer', QuantileTransformer())
]

models = [
    ('DecisionTree', MultiOutputRegressor(DecisionTreeRegressor())),
    ('LinearRegression', MultiOutputRegressor(LinearRegression())),
    ('SVR', MultiOutputRegressor(SVR())),
    ('KNeighborsRegressor', MultiOutputRegressor(KNeighborsRegressor())),
    ('RandomForest', MultiOutputRegressor(RandomForestRegressor())),
    ('GradientBoosting', MultiOutputRegressor(GradientBoostingRegressor())),
    ('AdaBoostRegressor', MultiOutputRegressor(AdaBoostRegressor())),
    ('XGBRegressor', MultiOutputRegressor(XGBRegressor()))
]

def load_data():
    df = pd.read_csv("processed_dataset_with_10_components.csv", encoding="utf-8")

    # Print the dataframe to see the data structure
    print(f"Loading Dataframe:\n{df}\n")

    y = df.iloc[:, 102:].to_numpy(dtype=np.float64)
    X = df.iloc[:, 2:102].to_numpy(dtype=np.float64)

    return X, y

if __name__ == "__main__":
    X, y = load_data()
    for scaler_name, scaler in scalers:
        print(f"Scaling method: {scaler_name}")
        X_scaled = scaler.fit_transform(X)
        y_scaled = scaler.fit_transform(y)

        # K-fold Cross-Validation
        kf = KFold(n_splits=10, shuffle=True, random_state=42)
        rmse_values = []

        for model_name, model in models:
            print(f"Model: {model_name}")

            for train_index, test_index in kf.split(X_scaled):
                X_train, X_test = X_scaled[train_index], X_scaled[test_index]
                y_train, y_test = y_scaled[train_index], y_scaled[test_index]
                model.fit(X_train, y_train)
                y_pred = model.predict(X_test)
                rmse = mean_squared_error(y_test, y_pred)
                rmse_values.append(rmse)

            avg_rmse = np.mean(rmse_values)
            print(f"Average RMSE across all folds: {avg_rmse}")
        print("\n")

        # hold-out Method
        '''
        X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_scaled, test_size=0.3, random_state=42)
        for model_name, model in models:
            print(f"Model: {model_name}")
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            rmse = mean_squared_error(y_test, y_pred)
            print(f"RMSE: {rmse}")
        print("\n")
        '''
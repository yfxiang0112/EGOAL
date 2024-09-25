import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import ParameterGrid
import matplotlib.pyplot as plt

df = pd.read_csv('plots/simple_nn/processed_dataset_with_importance.csv')

features = df.iloc[:, 2:102].values  # 421 × 100
labels1 = []
yc = df.iloc[:, 102:122]
for i in range(421):
    for j in range(20):
        label = yc.iloc[i, j].strip().strip('()').split(', ')[0]
        labels1.append(label)
samples = [labels1[i:i + 20] for i in range(0, len(labels1), 20)]  # 421 × 20
unique_labels = sorted(set(label for sample in samples for label in sample))
num_classes = len(unique_labels)
label_to_idx = {label: idx for idx, label in enumerate(unique_labels)}

targets_onehot = torch.zeros(len(samples), len(samples[0]), num_classes, dtype=torch.float32)  # 421 × 20 × 1553
for i in range(len(samples)):
    for j in range(len(samples[0])):
        idx = label_to_idx[samples[i][j]]
        targets_onehot[i, j, idx] = 1

X_train, X_test, y_train, y_test = train_test_split(features, targets_onehot, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Convert to torch tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)
y_train = torch.tensor(y_train.numpy(), dtype=torch.float32)
y_test = torch.tensor(y_test.numpy(), dtype=torch.float32)


class SimpleNN(nn.Module):
    def __init__(self, input_size, output_size, hidden_size, times):
        super(SimpleNN, self).__init__()
        self.input_size = input_size  # 100
        self.output_size = output_size  # 1553
        self.hidden_size = hidden_size
        self.times = times  # 20
        self.simplenns = nn.ModuleList(
            [nn.Sequential(
                nn.Linear(self.input_size, self.hidden_size),
                nn.ReLU(),
                nn.Linear(self.hidden_size, self.output_size),
                nn.Softmax(dim=-1)
            ) for _ in range(self.times)]
        )

    def forward(self, x):
        outputs = [simplenn(x) for simplenn in self.simplenns]  # 20 (336 × 1553)
        outputs = torch.stack(outputs, dim=1)  # 336 × 20 × 1553

        return outputs


model = SimpleNN(input_size=len(features[0]), output_size=num_classes, hidden_size=num_classes, times=len(samples[0]))

criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.01)

num_epochs = 20
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train)

    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

    print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

torch.save(model.state_dict(), 'model.pth')


def evaluate_model(model, X_test, y_test):
    model.eval()
    with torch.no_grad():
        outputs = model(X_test)
        _, predicted_test = torch.max(outputs, -1)  # 85 × 20
        _, real_y_test = torch.max(y_test, -1)  # 85 × 20

        correct = 0
        for i in range(len(predicted_test)):
            for j in range(len(predicted_test[0])):
                predict = predicted_test[i][j]
                if predict in real_y_test[i]:
                    correct += 1
                    evaluate_dict[unique_labels[predict]][0] += 1
                evaluate_dict[unique_labels[predict]][1] += 1

        total = len(real_y_test) * len(real_y_test[0])

        accuracy = correct / total

        return accuracy

evaluate_dict = {}
for label in unique_labels:
    evaluate_dict[label] = [0, 0]

accuracy = evaluate_model(model, X_test, y_test)

for label in unique_labels:
    a, b = evaluate_dict[label]
    if b == 0:
        evaluate_dict.pop(label)
    else:
        evaluate_dict[label] = a / b

print(f'Accuracy: {accuracy:.4f}')
print(evaluate_dict)
with open('plots/simple_nn/eval.txt', 'w') as f:
    f.write(str(evaluate_dict))


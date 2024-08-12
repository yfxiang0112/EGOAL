import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df = pd.read_csv('processed_dataset_with_importance.csv')

features = df.iloc[:, 2:102].values
labels1 = []
yc = df.iloc[:, -20: ]
for i in range(421):
    for j in range(20):
        label = yc.iloc[i, j].strip().strip('()').split(', ')[0]
        labels1.append(label)
samples = [labels1[i:i + 20] for i in range(0, len(labels1), 20)]
unique_labels = sorted(set(label for sample in samples for label in sample))
num_classes = len(unique_labels)
label_to_idx = {label: idx for idx, label in enumerate(unique_labels)}
targets_onehot = torch.zeros(len(samples), num_classes, dtype=torch.long)

for i, sample in enumerate(samples):
    for label in sample:
        idx = label_to_idx[label]
        targets_onehot[i, idx] = 1

X_train, X_test, y_train, y_test = train_test_split(features, targets_onehot, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# 转换为torch tensors
X_train = torch.tensor(X_train, dtype=torch.float32)
X_test = torch.tensor(X_test, dtype=torch.float32)


class SimpleNN(nn.Module):
    def __init__(self, input_size, num_classes):
        super(SimpleNN, self).__init__()
        self.fc1 = nn.Linear(input_size, 100)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(100, num_classes)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        return out



model = SimpleNN(input_size=100, num_classes=len(unique_labels))

criterion = nn.MultiLabelSoftMarginLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

num_epochs = 2
for epoch in range(num_epochs):
    model.train()
    optimizer.zero_grad()
    outputs = model(X_train)
    loss = criterion(outputs, y_train)
    loss.backward()
    optimizer.step()

    if (epoch + 1) % 2 == 0:
        print(f'Epoch [{epoch + 1}/{num_epochs}], Loss: {loss.item():.4f}')

torch.save(model.state_dict(), 'model.pth')



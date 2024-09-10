import re
import matplotlib.pyplot as plt
import numpy as np

text_path = 'src/predict/evaluation_results_before.txt'
with open(text_path, 'r') as file:
    text = file.read()

pattern = re.compile(r'(SO_\d+): GO/character_accuracy: (\d+\.\d+) GO/reasoning_accuracy: (\d+\.\d+)')

matches = pattern.findall(text)

id_set = []
character_accuracy_set = []
reasoning_accuracy_set = []

for match in matches:
    so_id, character_accuracy, reasoning_accuracy = match
    # print(f"ID: {so_id}, Character Accuracy: {character_accuracy}, Reasoning Accuracy: {reasoning_accuracy}")
    id_set.append(so_id)
    character_accuracy_set.append(character_accuracy)
    reasoning_accuracy_set.append(reasoning_accuracy)

x_values = range(len(id_set))

character_accuracy_set = [float(s) for s in character_accuracy_set]
reasoning_accuracy_set = [float(s) for s in reasoning_accuracy_set]

mean_character_accuracy = np.mean(character_accuracy_set)
mean_reasoning_accuracy = np.mean(reasoning_accuracy_set)

print('cha_acc, rea_acc',mean_character_accuracy, mean_reasoning_accuracy)

plt.figure(figsize=(20, 16))
# 调整线条宽度和标记大小
plt.plot(x_values, reasoning_accuracy_set, marker='o', linestyle='-', color='r', label='Reasoning Accuracy', linewidth=0.5, markersize=3)
plt.axhline(y=mean_reasoning_accuracy, color='r', linestyle='--', label=f'Mean Reasoning Accuracy: {mean_reasoning_accuracy:.3f}', linewidth=0.5)
plt.xlabel('SO ID')
plt.ylabel('Accuracy')
plt.title('Evaluation Results')
plt.xticks(x_values, id_set, rotation=45)
plt.legend()
plt.savefig('src/predict/reasoning_acc_bfe.png')


plt.figure(figsize=(20, 16))
plt.plot(x_values, character_accuracy_set, marker='o', linestyle='-', color='b', label='Character Accuracy', linewidth=0.5, markersize=3)
plt.axhline(y=mean_character_accuracy, color='b', linestyle='--', label=f'Mean Character Accuracy: {mean_character_accuracy:.3f}', linewidth=0.5)
plt.xlabel('SO ID')
plt.ylabel('Accuracy')
plt.title('Evaluation Results')
plt.xticks(x_values, id_set, rotation=45)
plt.legend()
plt.savefig('src/predict/character_acc_bfe.png')
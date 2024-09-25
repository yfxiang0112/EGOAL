import re
import matplotlib.pyplot as plt
import numpy as np

aft_path = 'plots/train_acc/evaluation_results_after.txt'
bfe_path = 'plots/train_acc/evaluation_results_before.txt'
aft_path_new = 'plots/train_acc/new_model_after.txt'
with open(aft_path, 'r') as file:
    text_aft = file.read()
with open(bfe_path, 'r') as file:
    text_bfe = file.read()
with open(aft_path_new, 'r') as file:
    text_aft_new = file.read()

pattern = re.compile(r'(SO_\d+): GO/character_accuracy: (\d+\.\d+) GO/reasoning_accuracy: (\d+\.\d+)')

matches_aft = pattern.findall(text_aft)
matches_bfe = pattern.findall(text_bfe)

matches_new = pattern.findall(text_aft_new)
matches_new.sort(key=lambda x: x[0])


id_set = []
character_accuracy_aft = []
reasoning_accuracy_aft = []
character_accuracy_bfe = []
reasoning_accuracy_bfe = []

for match in matches_new:
    so_id, character_accuracy, reasoning_accuracy = match
    id_set.append(so_id)
    character_accuracy_aft.append(character_accuracy)
    #reasoning_accuracy_aft.append(reasoning_accuracy)

for match in matches_aft:
    so_id, character_accuracy, reasoning_accuracy = match
    if so_id in id_set:
        #character_accuracy_aft.append(character_accuracy)
        reasoning_accuracy_aft.append(reasoning_accuracy)
for match in matches_bfe:
    so_id, character_accuracy, reasoning_accuracy = match
    if so_id in id_set:
        character_accuracy_bfe.append(character_accuracy)
        reasoning_accuracy_bfe.append(reasoning_accuracy)

x_values = range(len(id_set))

character_accuracy_aft = [float(s) for s in character_accuracy_aft]
reasoning_accuracy_aft = [float(s) for s in reasoning_accuracy_aft]
character_accuracy_bfe = [float(s) for s in character_accuracy_bfe]
reasoning_accuracy_bfe = [float(s) for s in reasoning_accuracy_bfe]

mean_character_aft = np.mean(character_accuracy_aft)
mean_reasoning_aft = np.mean(reasoning_accuracy_aft)
mean_character_bfe = np.mean(character_accuracy_bfe)
mean_reasoning_bfe = np.mean(reasoning_accuracy_bfe)

#print('cha_acc, rea_acc',mean_character_accuracy, mean_reasoning_accuracy)

plt.figure(figsize=(8, 6))
# 调整线条宽度和标记大小
plt.bar(x_values, reasoning_accuracy_aft, width=1, color='darkgreen', label='Before ABL')
plt.bar(x_values, reasoning_accuracy_bfe, width=1, color='mediumaquamarine', label='After ABL')
plt.axhline(y=mean_reasoning_bfe, color='dimgray', linestyle='--', label=f'Mean Acc Before ABL: {mean_reasoning_bfe:.3f}', linewidth=2)
plt.axhline(y=mean_reasoning_aft, color='black', linestyle='--', label=f'Mean Acc After ABL: {mean_reasoning_aft:.3f}', linewidth=2)
plt.xlabel('Single Gene Subtasks')
plt.ylabel('Reasoning Accuracy')
plt.title('Reasoning Part Evaluation Results')
#plt.xticks(x_values, id_set, rotation=45)
plt.legend()
plt.savefig('plots/train_acc/reasoning_acc.png')
plt.show()


plt.figure(figsize=(8, 6))
plt.bar(x_values, character_accuracy_aft, width=1, color='navy', label='After ABL')
plt.bar(x_values, character_accuracy_bfe, width=1, color='royalblue', label='Before ABL')
plt.axhline(y=mean_character_bfe, color='dimgray', linestyle='--', label=f'Mean Acc Before ABL: {mean_character_bfe:.3f}', linewidth=2)
plt.axhline(y=mean_character_aft, color='black', linestyle='--', label=f'Mean Acc After ABL: {mean_character_aft:.3f}', linewidth=2)
plt.xlabel('Single Gene Subtasks')
plt.ylabel('Character Accuracy')
plt.title('Learning Part Evaluation Results')
#plt.xticks(x_values, id_set, rotation=45)
plt.legend()
plt.savefig('plots/train_acc/character_acc.png')
plt.show()

import pandas as pd

df = pd.read_csv('../../dataset/dataset.csv')
concept_column = df['CONCEPTS']
concepts = []
for i in range(len(concept_column)):
    concepts.append(eval(concept_column[i]))

go_dict = {}
with open('../../dataset/embeddings_preprocess_modified.txt', 'r') as file:
    for line in file:
        parts = line.strip().split() 
        if len(parts) > 1:
            go_term = parts[0]
            values = parts[1:]
            go_dict[go_term] = values

new_rows = []
not_found = 0
count_all = 0

for i in range(len(concepts)):
    concept_list = concepts[i]
    j = 0
    while j < len(concept_list):
        count_all += 1
        go_term = concept_list[j]
        values = go_dict.get(go_term, None) 
        
        if values is None:
            not_found += 1
            # print(f"Missing go_term: {go_term}")  
            concept_list.pop(j)  
        else:
            j += 1 

    for j in range(len(concept_list)):
        go_term = concept_list[j]
        values = go_dict[go_term]  
        new_row = [concept_list, go_term] 
        new_row.extend(values)
        new_rows.append(new_row)

num_vectors = len(values)
column_names = ['CONCEPTS', 'CONCEPT'] + [f'vector{i+1}' for i in range(num_vectors)]

new_df = pd.DataFrame(new_rows, columns=column_names)
new_df.to_csv('../../dataset/new_dataset.csv', index=False)

print('All, not found, found: ', count_all, not_found, count_all - not_found)
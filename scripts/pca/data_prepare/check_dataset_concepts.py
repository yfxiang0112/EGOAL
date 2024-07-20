import pandas as pd

processed_df = pd.read_csv('./dataset/processed_dataset.csv')
processed_concepts = processed_df['CONCEPTS']

reduced_df = pd.read_csv('./dataset/reduced_dataset.csv')
reduced_concepts = reduced_df['CONCEPTS']

print(len(processed_concepts),len(reduced_concepts))

for i in range(len(processed_concepts)):
    flag = 0
    for j in range(len(reduced_concepts)):
        if processed_concepts[i] == reduced_concepts[j]:
            flag = 1
    if flag == 0:
        print('diff!')
        assert(0)
    print(flag, i)

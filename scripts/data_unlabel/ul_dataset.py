import pandas as pd

#label_df = pd.read_csv('dataset/importance/dataset_onehot.csv', index_col=0)

with open('dataset/unlabel/concepts.txt', 'r') as f:
    con_lst = eval(f.readline())

len_ul_data = len(con_lst)
print(len_ul_data)

unlabel_df = {'CONCEPTS':con_lst}
#for c in label_df.columns[1:]:
#    unlabel_df.update({c: [0]*len_ul_data})

unlabel_df = pd.DataFrame(unlabel_df)
print(unlabel_df)
unlabel_df.to_csv('dataset/unlabel/dataset_unlabel.csv', index=False)

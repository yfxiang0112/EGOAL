import pandas as pd

with open('dataset/unlabel/concepts.txt', 'r') as f:
    con_lst = eval(f.readline())

print(len(con_lst))

import re

pat = r'Accession: GSE\d*'
acc_set = set()
with open('dataset/unlabel/gds_result.txt', 'r') as f:
    line = f.readline()
    res = re.findall(pat, line)
    for r in res:
        acc_set.add(r)
    while line:
        line = f.readline()
        res = re.findall(pat, line)
        for r in res:
            acc_set.add(r)

acc_set = set(s[11:] for s in acc_set)
#print(acc_set)
with open('dataset/unlabel/accessions', 'w') as f:
    f.write('accession\n')
    for acc in acc_set:
        f.write(f'{acc}\n')


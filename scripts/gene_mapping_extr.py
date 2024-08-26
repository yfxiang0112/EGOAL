import re

#p_tag = r'locus_tag=\"SO_\d{4}\"'
#p_prod = r'product=\".*\"'
pat = r'/locus_tag=\"SO_\d{4}\"\n      	/codon_start=\d*\n      	/transl_table=\d*\n      	/product=\"[\w\s\n]*\"'
genome = ''
pred_gene = []


with open('predict/SO_genome.txt', 'r') as f:
    genome = f.read()

res = genome.split(sep='CDS')

#res = re.findall(pat, genome)
#res_prod = re.findall(p_prod, genome)

#print(len(res_tag), len(res_prod))
#assert len(res_tag) == len(res_prod)

tags = [re.findall(r'SO_\d{4}',s)[0] for s in res]

gene_prods = []
for s in res:
    res_prod = re.findall(r'product=\"[\w\s\n\(\)-/]*\"', s)
    if len(res_prod) > 0:
        string = res_prod[0][9:-1].replace('\n      \t', ' ')
        gene_prods.append(string)
    else:
        gene_prods.append('')

gene_mapping = {z[0] : z[1] for z in zip(tags, gene_prods)}
#print(gene_mapping)
#print(len(gene_mapping))

with open('predict/gene_mapping.txt', 'w') as f:
    f.write(str(gene_mapping))

with open('src/predict/classification_results.txt', 'r') as f:
    s = f.read()
    s = re.findall(r'\[.*\]', s)[0]
    pred_gene = eval(s)

with open('predict/pred_gene_with_name.txt', 'w') as f:
    f.write(f'predicted {len(pred_gene)} genes:\n')
    for g in pred_gene:
        f.write(f'{g} - {gene_mapping[g]}\n')

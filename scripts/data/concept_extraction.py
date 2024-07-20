import pandas as pd
from tqdm import tqdm
import re

def GOID_regu(s):
    res = []
    for goid in s:
        d = re.findall(r'\d+', goid)
        d = 'GO:'+d[0]
        res.append(d)
    res.sort()
    return res


gsm_df = pd.read_csv('dataset/GSE_concepts.csv')
concepts = []
#gsm_df.drop(['Unnamed: 0', 'Unnamed: 0.1'], axis=1, inplace=True)
#gsm_df.rename(columns={'description':'DESCRIP', 'openai_ans':'OPENAI_ANS', 'concepts':'CONCEPTS'}, inplace=True)

test_str = '''
- Strain: MR-1(pBBR-glk-galP)
- Treatment: Grown under a fumarate-respiring condition
- Cell suspension centrifuged at 13,000 rpm for 1 min
- Growth medium: GMM supplemented with fumarate (40 mM) as an electron acceptor
- Cells harvested at the logarithmic growth phase (OD600 0.2–0.3)
- Incubation for 3 h in the presence (fumarate-respiring condition) or absence (fermentative condition) of fumarate

Gene Ontology (GO) terms related to the experiment conditions:
1. Electron transport chain (GO: 0022900)
2. Fumarate reductase activity (GO: 0004631)
3. Response to fumarate (GO: 0010267)
4. Logarithmic growth (GO: 0016091)
5. Anaerobic respiration (GO: 0009061)
6. Cell growth (GO: 0016049)

These GO terms capture the biological processes and molecular functions relevant to the experiment conditions described."
'''
'''
for d in tqdm(gsm_df['description'], 'test'):
    pass
'''

for ans in gsm_df['OPENAI_ANS'] :
    pattern = r'GO:* *_*\d+'
    res = re.findall(pattern, ans) 
    res = set(res)
    #print(res)

    concepts.append(res)

gsm_df['CONCEPTS'] = pd.Series(concepts).apply(GOID_regu)
print(gsm_df['CONCEPTS'])

gsm_df.set_index('SAMPLES', inplace=True)
gsm_df.sort_index(inplace=True)
print(gsm_df)
gsm_df.to_csv('dataset/GSE_concepts.csv')

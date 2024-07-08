import pandas as pd
from tqdm import tqdm
import re

gsm_df = pd.read_csv('data_SOneidensis/GSE_concepts.csv')
concepts = []

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

for ans in gsm_df['openai_ans'] :
    pattern = r'GO: *\d+'
    res = re.findall(pattern, ans) 
    res = set(res)
    #print(res)

    concepts.append(res)

gsm_df['concepts'] = pd.Series(concepts)
print(gsm_df)
gsm_df.to_csv('data_SOneidensis/GSE_concepts.csv')

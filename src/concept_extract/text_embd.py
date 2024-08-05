import pandas as pd
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

gse_df = pd.read_csv('dataset/concepts/GSE_concepts.csv', index_col='SAMPLES')
model = SentenceTransformer("all-MiniLM-L6-v2")

for gsm, row in gse_df.iterrows():
    descrp = row['DESCRIP']
    embeddings = model.encode(descrp)
    print(embeddings.shape, embeddings)


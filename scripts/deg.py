from itertools import count
import pandas as pd
import GEOparse

from pydeseq2.dds import DeseqDataSet
from pydeseq2.default_inference import DefaultInference
from pydeseq2.ds import DeseqStats

accessions = pd.read_csv("dataset/accessions")

for accession in accessions['accession']:
    mat_path = 'dataset/matrix/'+accession+'_expr_mat.csv'

    counts = pd.read_csv(mat_path)
    counts = counts.groupby('GENE').mean()
    counts = counts.drop('Unnamed: 0', axis=1)
    counts = counts.transpose()
    #counts.columns = counts.iloc[0]
    #counts.drop(['GENE'], axis=0, inplace=True)
    counts.dropna(axis=1, inplace=True)
    #counts.set_index([0], inplace=True)
    counts.reset_index(inplace=True)
    counts.drop(['index'], axis=1, inplace=True)
    print(counts)

    if counts.mean(axis=1).mean() < 10:
        counts *= 10
    counts = counts.round().astype(int)
    print(counts)

    gse_path = "dataset/GSE/" + accession + "_family.soft.gz"
    gse = GEOparse.get_GEO(filepath=gse_path, silent=True)

    
    descriptions = []
    groups = []

    for gsm_name, gsm in gse.gsms.items():

        description = ''
        if('characteristics_ch1' in gsm.metadata):
            for s in gsm.metadata['characteristics_ch1']:
                description = description + s + '\n'
        if('treatment_protocol_ch1' in gsm.metadata):
            for s in gsm.metadata['treatment_protocol_ch1']:
                description = description + s + '\n'
        if('growth_protocol_ch1' in gsm.metadata):
            for s in gsm.metadata['growth_protocol_ch1']:
                description = description + s + '\n'
        descriptions.append(description)

    cur_idx = 0
    grp = 0
    for i in range(len(descriptions)):
        if descriptions[i] != descriptions[cur_idx]:
            cur_idx = i
            grp += 1
        groups.append(str(grp))

    metadata = pd.DataFrame({'group':groups})
    print(metadata)


    inference = DefaultInference(n_cpus=8)
    dds = DeseqDataSet(
        counts=counts,
        metadata=metadata,
        design_factors="group",
        refit_cooks=True,
        inference=inference,
    )
    
    dds.deseq2()
    
    for grp in range(1, len(set(groups))):
        stat_res = DeseqStats(dds, contrast=['group', '0', str(grp)], inference=inference)
        stat_res.summary()
        #with open(os.path.join(DEG_HET_KO_PTH, "shrunk_stat_results.pkl"), "wb") as f:
        #    pkl.dump(stat_res, f)
        deg_df = stat_res.results_df.sort_values('pvalue', ascending=False)
        deg_df.reset_index(inplace=True)

        print(deg_df)
        path = 'dataset/deg_result/'+accession+'_'+str(grp)+'.csv'
        deg_df.to_csv(path, index=False)


    #tmp
    break

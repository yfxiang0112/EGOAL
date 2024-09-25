# EGOAL: predict gene expression with Gene Ontology and Abductive Learning

EGOAL is a attempt of introducing the *Holy Grail*
of Artificial Intelligence
— **combination of Machine Learning and Symbolic Reasoning**, aka.
Neural-Symbolic AI — into the sight of Synthetic Biology.

We are trying to assist researches and drive innovations in SynBio, via
Abductive Learning, the novel paradigm of neural-symbolic AI
proposed by researchers from Nanjing University.

---

This project is a part of Drylab for iGEM team Nanjing-China 2024.

This is also a project of 2024 AI+ Contest, School of Artificial Intelligence,
Nanjing University.

## Description

We constructed a gene expression prediction model based on Abductive Learning, a prominent neural-symbolic AI paradigm. By leveraging the Gene Ontology, it generates accurate predictions with minimal reliance on historical data, demonstrating the effectiveness of neural-symbolic AI in the field of synthetic biology.

The knowledge base, i.e. Gene Ontology, contains the relations
of gene regulation in its graph structure, which can be learned by the model.
Thus we can predict expression of genes on the regulation pathway from the condition and result of the experiment.

## Usage

### Directly Use GO Concepts

```
python src/abl/predict -d True -i examples/NADK/input_terms.txt -o examples/NADK
```

### Use Natural Language Descriptions

```
python src/abl/predict -i examples/GAPDH/input_terms.txt -o examples/GAPDH
```

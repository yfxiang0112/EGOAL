# GOABL Development Log

## Introduction

---

## Part I: Construct Dataset from GEO Sample Data

A species-specified dataset of Shewanella Oneidensis.

A dataset of gene expression in Shewanella Oneidensis is constructed

### Collecting Data Sample from GEO

40 gene expression series and 426 samples of Shewanella Oneidensis are
collected from Gene Expression Onimbus (GEO) database.

### Obtaining Expression Matrix from GEO Sample

### Extracting Concept from Natural Language Description

Large Language Models (LLMs) are employed in the preliminary implement.
In detail, we used `OpenAI`\`s API of `GPT 3.5-Turbo` to understand natural
language-based description of `GEO` experiment datasets, and summerize
them to corresponding concept IDs in `GO`.

A fundamental risk underlies in the method above: great ambiguity and uninterpretability
of LLMs is introduced to the dataset. Therefore, we are exploring better solutions.

### Unifying Expression Level Data and Integrating Samples as Dataset

**TODO**: Ratio and Signal intensity?

### Unify Expression Data with Importance Metric

TODO: **non-supervised importance** and **top 20 relative expression with DEG**

---

## Part II: Embedding Method

In a traditional method, the concept name-descripted instances are mapped to
ectors to train a learner model.

### Ontology Embedding

The concepts of Gene Ontology is mapped to vectors with `owl2vec_star`, which
preserves information of knowledge graph structure, word vector and literal meaning
of concept names.

### Processing Multiple Concepts

For instances with multiple concepts as input, it is mapped to the mean value of
the concept embeddings.

### Obtaining Learner Model with Concept Embeddings

---

## Part III: Knowledge Graph Preprocessing: Remembering

### Subgraph Extraction

### Rule Mining

### Remember Algorithm

---

## Part IV: Abductive Learning

### Building Learner

### Building Reasoner

### Bridging Learner and Reasoner

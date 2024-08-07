# FSIL-Model

## t-ner Model

### Data Preprocessing.ipynb

Given an annotated JSON file, the script outputs the processed data in CoNLL format.

The continuation link is implemented, and the text it points to is directly appended to the original text with the same label. 

The 'O-' tag is also implemented, meaning that everything other than the labeled text is considered as 'O-'.

Place the JSON file and script in the same directory to generate the output.

### Finetuning.ipynb

The initial model does not perform very well

## Graph RAG

GraphRAGs are less prone to hallucinate because the knowledge graphs offer more relevant, varied, engaging, coherent, and reliable data to the LLM, ultimately leading to accurate and factual text generation.

The pipeline is structured as follows:

1. Split the input texts into manageable chunks for processing.
2. Identify and extract instances of graph nodes and edges from each chunk of source text.
3. Use a LLM to summarize the extracted instances in an abstractive manner.
4. Model the index created in the previous step as a homogeneous undirected weighted graph.
5. Generate report-like summaries for each community.
6. Given a user query, utilize the community summaries generated in the previous step to produce a final answer through a multi-stage process.

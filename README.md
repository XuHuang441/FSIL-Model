# FSIL-Model

## Data Preprocessing.ipynb

Given an annotated JSON file, the script outputs the processed data in CoNLL format. However, the coding regarding continuation link is not implemented.

Place the JSON file and script in the same directory to generate the output.

## Finetuning.ipynb

It appears that the label: "o-" is required for training, otherwise there would be an AssertionError.

## Context Extraction.ipynb

I have been working on the "o-" tag, which serves as the context for the labels. Initially, I used the p tag in the HTML document to split the paragraphs with Beautiful Soup, aiming to use these segments as context. Then, I attempted to leverage the information provided in the label, specifically:

1. The globalOffsets. I'm unsure how Label Studio calculates this, but it does not appear to be based on the total character count of the document.
2. The start and end attributes. I tried to locate the label using the provided directory, but this approach did not yield accurate results.

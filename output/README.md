## Outputs

After running the program, you can find the related outputs under this folder:

- Processed versions of the train and test data.
- Perplexity calculations for each sentence in the test data.
- Randomly generated sentences with 5 syllables.

Additionally, you will find:
- Unigram, bigram, and trigram tables. These tables represent frequency counts after applying Good-Turing smoothing.
- The n-gram tables are stored as dictionaries. Whenever the 'UNK' element is encountered in the test data, a zero-count probability is utilized.

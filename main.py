import math
import random
import numpy as np
import pandas as pd
import nltk
from preprocessing_util import split_to_sentences, tokenize_sentences, get_tokenized_data
from preprocessing import preprocess_data, preprocess_test
from ngram import count_n_grams, ngram_test, ngram_prob_test, estimate_probabilities, make_count_matrix, make_probability_matrix, count_matrix_test, prob_matrix_test
from evaluation import calculate_perplexity, ppl_test
from count import count_test
from autocomplete import autocomplete_test
nltk.data.path.append('.')
nltk.download("punkt")
nltk.download("punkt_tab")


### Preprocessing Twitter Dataset ###
# Read twitter data
with open("en_US.twitter.txt", "r", encoding='UTF8') as f:
    data = f.read()

print("Data type:", type(data))
print("Number of letters:", len(data))

print("\nFirst 300 letters of the data")
print("-------")
print(data[0:300])
print("-------")

print("\nLast 300 letters of the data")
print("-------")
print(data[-300:])
print("-------")


# Tokenizing a sentence
x = "Sky is blue.\nLeaves are green\nRoses are red."
print(f"\n## Original sentences :\n{x}")
print(f"## Tokenized sentences:\n{get_tokenized_data(x)}")


# Split into train and test sets (8:2)
print("\nTokenizing the data...")
tokenized_data = get_tokenized_data(data)
random.seed(87)
random.shuffle(tokenized_data)

train_size = int(len(tokenized_data) * 0.8)
train_data = tokenized_data[0:train_size]
test_data = tokenized_data[train_size:]

print("{} data are split into {} train and {} test set".format(
    len(tokenized_data), len(train_data), len(test_data)))

print("\nFirst training sample:")
print(train_data[0])

print("First test sample")
print(test_data[0])


## Preprocess the train and test data
minimum_freq = 2  # Words that appear less frequently than minimum_freq are treated as UNKNOWN.
preprocess_test(train_data[:100], test_data[:100], minimum_freq)  
train_data_processed, test_data_processed, vocabulary = preprocess_data(train_data, test_data, minimum_freq)

print("First preprocessed training sample:")
print(train_data_processed[0])

print("\nFirst preprocessed test sample:")
print(test_data_processed[0])

print("\nFirst 10 vocabulary:")
print(vocabulary[0:10])

print("\nSize of vocabulary:", len(vocabulary))

##################################### Preprocessing is finished

## n-gram test: Bigram
sentences = [['i', 'like', 'a', 'cat'],
             ['this', 'dog', 'is', 'like', 'a', 'cat']]

sentences_flatten = []
for sentence in sentences:
    sentences_flatten += sentence
unique_words = list(set(sentences_flatten))

# add <e> <unk> to the vocabulary
# <s> is omitted since it should not appear as the next word
unique_words += ["<e>", "<unk>"]

count_test(sentences)
ngram_test(sentences) 
ngram_prob_test(sentences, unique_words)  
count_matrix_test(sentences, unique_words)
prob_matrix_test(sentences, unique_words)
ppl_test(sentences, unique_words) 
autocomplete_test(sentences, unique_words, train_data_processed)

print("\nCongratulations! You have completed all tasks.")


## n-gram: Trigram examples using preprocessed Twitter dataset
sentences = train_data_processed
sentences_flatten = []
for sentence in sentences:
    sentences_flatten += sentence

# add <e> <unk> to the vocabulary
# <s> is omitted since it should not appear as the next word
unique_words = list(set(sentences_flatten + ["<e>", "<unk>"]))

unigram_counts = count_n_grams(sentences, 1)
bigram_counts = count_n_grams(sentences, 2)
trigram_counts = count_n_grams(sentences, 3)

prob_words = estimate_probabilities(["<s>", "<s>"], bigram_counts, trigram_counts, unique_words)

print()
# print(make_count_matrix(trigram_counts, unique_words))
# print(make_probability_matrix(trigram_counts, unique_words, k=1))

sentences = test_data_processed[:10]
for sentence in sentences:
    ppl = calculate_perplexity(sentence, bigram_counts, trigram_counts, len(unique_words))
    print(f"""ppl of "{sentence}": {round(ppl, 4)}""")

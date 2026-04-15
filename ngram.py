import numpy as np
import pandas as pd

  #Count n-gram 
def count_n_grams(data, n, start_token='<s>', end_token='<e>'):
    """
    Count all n-grams in the data

    Args:
        data: List of lists of words
        n: number of words in a sequence

    Returns:
        A dictionary that maps a tuple of n-words to its frequency
    """

    # Initialize dictionary of n-grams and their counts
    n_grams = {}

    # Go through each sentence in the data
    for sentence in data:  # complete this line

        # prepend start token n times, and  append <e> one time
        sentence = [start_token] * n + sentence + [end_token]

        # convert list to tuple
        # So that the sequence of words can be used as
        # a key in the dictionary
        sentence = tuple(sentence)

        # Use 'i' to indicate the start of the n-gram
        # from index 0
        # to the last index where the end of the n-gram
        # is within the sentence.
        m = len(sentence) if n == 1 else len(sentence) - 1
        for i in range(m):

            # Get the n-gram from i to i+n
            n_gram = sentence[i:i+n]

            # check if the n-gram is in the dictionary
            if n_gram in n_grams:  # complete this line

                # Increment the count for this n-gram
                n_grams[n_gram] += 1
            else:
                # Initialize this n-gram count to 1
                n_grams[n_gram] = 1

    return n_grams


# Get n-gram probability
def estimate_probability(word, previous_n_gram,
                         n_gram_counts, n_plus1_gram_counts, vocabulary_size):
    """
    Estimate the probabilities of a next word using the n-gram counts with laplace smoothing

    Args:
        word: next word
        previous_n_gram: A sequence of words of length n
        n_gram_counts: Dictionary of counts of n-grams
        n_plus1_gram_counts: Dictionary of counts of (n+1)-grams
        vocabulary_size: number of words in the vocabulary

    Returns:
        A probability
    """
    # convert list to tuple to use it as a dictionary key
    previous_n_gram = tuple(previous_n_gram)

    ### START CODE HERE (Replace instances of 'None' with your code) ###

    # Set the denominator
    # If the previous n-gram exists in the dictionary of n-gram counts,
    # Get its count. Otherwise, set the count to zero
    # Use the dictionary that has counts for n-grams
    previous_n_gram_count = n_gram_counts.get(previous_n_gram, 0)

    # Calculate the denominator using the count of the previous n gram
    # and apply laplace smoothing
    denominator = previous_n_gram_count + vocabulary_size

    # Define n plus 1 gram as the previous n-gram plus the current word as a tuple
    n_plus1_gram = previous_n_gram + (word,)

    # Set the count to the count in the dictionary,
    # otherwise 0 if not in the dictionary
    # use the dictionary that has counts for the n-gram plus current word
    n_plus1_gram_count = n_plus1_gram_counts.get(n_plus1_gram, 0)

    # Define the numerator use the count of the n-gram plus current word,
    # and apply smoothing
    numerator = n_plus1_gram_count + 1

    # Calculate the probability as the numerator divided by denominator
    probability = numerator / denominator

    return probability


def estimate_probabilities(previous_n_gram, n_gram_counts, n_plus1_gram_counts, vocabulary):
    """
    Estimate the probabilities of next words using the n-gram counts with laplace smoothing

    Args:
        previous_n_gram: A sequence of words of length n
        n_gram_counts: Dictionary of counts of (n+1)-grams
        n_plus1_gram_counts: Dictionary of counts of (n+1)-grams
        vocabulary: List of words

    Returns:
        A dictionary mapping from next words to the probability.
    """

    # convert list to tuple to use it as a dictionary key
    previous_n_gram = tuple(previous_n_gram)

    vocabulary_size = len(vocabulary)

    probabilities = {}
    for word in vocabulary:
        probability = estimate_probability(word, previous_n_gram,
                                           n_gram_counts, n_plus1_gram_counts,
                                           vocabulary_size)
        probabilities[word] = probability

    return probabilities

def make_count_matrix(n_plus1_gram_counts, vocabulary):
    # obtain unique n-grams
    n_grams = []
    for n_plus1_gram in n_plus1_gram_counts.keys():
        n_gram = n_plus1_gram[0:-1]
        n_grams.append(n_gram)
    n_grams = list(set(n_grams))

    # mapping from n-gram to row
    row_index = {n_gram: i for i, n_gram in enumerate(n_grams)}
    # mapping from next word to column
    col_index = {word: j for j, word in enumerate(vocabulary)}

    nrow = len(n_grams)
    ncol = len(vocabulary)
    count_matrix = np.zeros((nrow, ncol))
    for n_plus1_gram, count in n_plus1_gram_counts.items():
        n_gram = n_plus1_gram[0:-1]
        word = n_plus1_gram[-1]
        if word not in vocabulary:
            continue
        i = row_index[n_gram]
        j = col_index[word]
        count_matrix[i, j] = count

    count_matrix = pd.DataFrame(count_matrix, index=n_grams, columns=vocabulary)
    return count_matrix

def make_probability_matrix(n_plus1_gram_counts, vocabulary):
    count_matrix = make_count_matrix(n_plus1_gram_counts, vocabulary)
    count_matrix += 1 # Laplace smoothing
    prob_matrix = count_matrix.div(count_matrix.sum(axis=1), axis=0)
    return prob_matrix


def ngram_test(sentences):
    print("\n n-gram (Unigram, Bigram)")
    unigram = count_n_grams(sentences, 1)
    bigram = count_n_grams(sentences, 2)
    print("Unigram:")
    print(unigram)
    print("Bigram:")
    print(bigram)

    if unigram == {('<s>',): 2, ('i',): 1, ('like',): 2, ('a',): 2, ('cat',): 2, ('<e>',): 2, ('this',): 1, ('dog',): 1, ('is',): 1}:
        print('SUCCESS')
    else:
        print('FAIL')
        exit(1)

    if bigram == {('<s>', '<s>'): 2, ('<s>', 'i'): 1, ('i', 'like'): 1, ('like', 'a'): 2, ('a', 'cat'): 2, ('cat', '<e>'): 2, ('<s>', 'this'): 1, ('this', 'dog'): 1, ('dog', 'is'): 1, ('is', 'like'): 1}:
        print('SUCCESS')
    else:
        print('FAIL')
        exit(1)
    print('')

def ngram_prob_test(sentences, unique_words):
    print("\n Bigram probability)")
    unigram_counts = count_n_grams(sentences, 1)
    bigram_counts = count_n_grams(sentences, 2)

    prob_cat_after_a = estimate_probability("cat", "a", unigram_counts, bigram_counts, len(unique_words))
    print(f"The estimated probability of word 'cat' given the previous n-gram 'a' is: {prob_cat_after_a:.4f}")

    prob_words_after_a = estimate_probabilities("a", unigram_counts, bigram_counts, unique_words)
    print(f"The estimated probability of each word given the previous n-gram 'a' is: ")
    print(prob_words_after_a)

    if abs(prob_cat_after_a - 0.2727) < 0.0001:
        print('SUCCESS')
    else:
        print('FAIL')
        exit(1)

    if abs(prob_words_after_a['like'] - 0.0909) < 0.0001 and \
        abs(prob_words_after_a['this'] - 0.0909) < 0.0001 and \
        abs(prob_words_after_a['cat'] - 0.2727) < 0.0001 and \
        abs(prob_words_after_a['<unk>'] - 0.0909) < 0.001:
        print('SUCCESS')
    else:
        print('FAIL')
        exit(1)


def count_matrix_test(sentences, unique_words):
    bigram_counts = count_n_grams(sentences, 2)

    print('\nbigram counts')
    print(make_count_matrix(bigram_counts, unique_words))


def prob_matrix_test(sentences, unique_words):
    bigram_counts = count_n_grams(sentences, 2)
    print("\nbigram probabilities")
    print(make_probability_matrix(bigram_counts, unique_words))

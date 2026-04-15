from ngram import count_n_grams, estimate_probability

# Q5: Perplexity (25 pts)
def calculate_perplexity(sentence, n_gram_counts, n_plus1_gram_counts, vocabulary_size):
    """
    Calculate perplexity for a list of sentences

    Args:
        sentence: List of strings
        n_gram_counts: Dictionary of counts of (n+1)-grams
        n_plus1_gram_counts: Dictionary of counts of (n+1)-grams
        vocabulary_size: number of unique words in the vocabulary
        k: Positive smoothing constant

    Returns:
        Perplexity score
    """
    # length of previous words
    n = len(list(n_gram_counts.keys())[0])

    # prepend <s> and append <e>
    sentence = ["<s>"] * n + sentence + ["<e>"]

    # Cast the sentence from a list to a tuple
    sentence = tuple(sentence)

    # length of sentence (after adding <s> and <e> tokens)
    N = len(sentence)

    # The variable p will hold the product
    # that is calculated inside the n-root
    # Update this in the code below
    product_pi = 1.0

    ### START CODE HERE (Replace instances of 'None' with your code) ###

    # Index t ranges from n to N - 1, inclusive on both ends
    for t in range(n, N):  # complete this line

        # get the n-gram preceding the word at position t
        n_gram = sentence[t-n:t]

        # get the word at position t
        word = sentence[t]

        # Estimate the probability of the word given the n-gram
        # using the n-gram counts, n-plus1-gram counts,
        # vocabulary size, and smoothing constant
        probability = estimate_probability(word, n_gram, n_gram_counts, n_plus1_gram_counts, vocabulary_size)
    
        # Update the product of the probabilities
        # This 'product_pi' is a cumulative product
        # of the probabilities that are calculated in the loop
        product_pi *= probability

    # Take the -1/N power of the product
    perplexity = pow(product_pi, -1/N)

    ### END CODE HERE ###
    return perplexity


########################################################################################################################

def ppl_test(sentences, unique_words):
    print("\n## Q5: Perplexity (25 pts)")
    unigram_counts = count_n_grams(sentences, 1)
    bigram_counts = count_n_grams(sentences, 2)

    perplexity_train1 = calculate_perplexity(sentences[0],
                                             unigram_counts, bigram_counts,
                                             len(unique_words))
    print(f"Perplexity for first train sample: {perplexity_train1:.4f}")

    test_sentence = ['i', 'like', 'a', 'dog']
    perplexity_test = calculate_perplexity(test_sentence,
                                           unigram_counts, bigram_counts,
                                           len(unique_words))
    print(f"Perplexity for test sample: {perplexity_test:.4f}")

    if abs(perplexity_train1 - 3.3268) < 0.0001:
        print('SUCCESS')
    else:
        print('FAIL')
        exit(1)

    if abs(perplexity_test - 4.7224) < 0.0001:
        print('SUCCESS')
    else:
        print('FAIL')
        exit(1)
    print('')
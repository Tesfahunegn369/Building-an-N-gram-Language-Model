from ngram import count_n_grams, estimate_probabilities

def suggest_a_word(previous_tokens, n_gram_counts, n_plus1_gram_counts, vocabulary, start_with=None):
    """
    Get suggestion for the next word

    Args:
        previous_tokens: The sentence you input where each token is a word. Must have length > n
        n_gram_counts: Dictionary of counts of (n+1)-grams
        n_plus1_gram_counts: Dictionary of counts of (n+1)-grams
        vocabulary: List of words
        start_with: If not None, specifies the first few letters of the next word

    Returns:
        A tuple of
          - string of the most likely next word
          - corresponding probability
    """

    # length of previous words
    n = len(list(n_gram_counts.keys())[0])

    # From the words that the user already typed
    # get the most recent 'n' words as the previous n-gram
    previous_n_gram = previous_tokens[-n:]

    # Estimate the probabilities that each word in the vocabulary
    # is the next word,
    # given the previous n-gram, the dictionary of n-gram counts,
    # the dictionary of n plus 1 gram counts, and the smoothing constant
    probabilities = estimate_probabilities(previous_n_gram,
                                           n_gram_counts, n_plus1_gram_counts,
                                           vocabulary)

    # Initialize suggested word to None
    # This will be set to the word with the highest probability
    suggestion = None

    # Initialize the highest word probability to 0
    # this will be set to the highest probability
    # of all words to be suggested
    max_prob = 0

    # For each word and its probability in the probabilities dictionary:
    for word, prob in probabilities.items():  # complete this line

        # If the optional start_with string is set
        if start_with:  # complete this line

            # Check if the beginning of word does not match with the letters in 'start_with'
            if not word.startswith(start_with):  # complete this line

                # if they don't match, skip this word (move onto the next word)
                continue  # complete this line

        # Check if this word's probability
        # is greater than the current maximum probability
        if prob > max_prob:  # complete this line

            # If so, save this word as the best suggestion (so far)
            suggestion = word

            # Save the new maximum probability
            max_prob = prob

    return suggestion, max_prob


def get_suggestions(previous_tokens, n_gram_counts_list, vocabulary, start_with=None):
    model_counts = len(n_gram_counts_list)
    suggestions = []
    for i in range(model_counts - 1):
        n_gram_counts = n_gram_counts_list[i]
        n_plus1_gram_counts = n_gram_counts_list[i + 1]

        suggestion = suggest_a_word(previous_tokens, n_gram_counts,
                                    n_plus1_gram_counts, vocabulary,
                                    start_with=start_with)
        suggestions.append(suggestion)
    return suggestions


########################################################################################################################

def autocomplete_test(sentences, unique_words, data):
    unigram_counts = count_n_grams(sentences, 1)
    bigram_counts = count_n_grams(sentences, 2)

    previous_tokens = ["i", "like"]
    tmp_suggest1 = suggest_a_word(previous_tokens, unigram_counts, bigram_counts, unique_words)
    print(f"The previous words are 'i like',\n\tand the suggested word is `{tmp_suggest1[0]}` with a probability of {tmp_suggest1[1]:.4f}\n")

    # test your code when setting the starts_with
    tmp_starts_with = 'c'
    tmp_suggest2 = suggest_a_word(previous_tokens, unigram_counts, bigram_counts, unique_words, start_with=tmp_starts_with)
    print(f"The previous words are 'i like', the suggestion must start with `{tmp_starts_with}`\n\tand the suggested word is `{tmp_suggest2[0]}` with a probability of {tmp_suggest2[1]:.4f}\n")

    unigram_counts = count_n_grams(sentences, 1)
    bigram_counts = count_n_grams(sentences, 2)
    trigram_counts = count_n_grams(sentences, 3)
    quadgram_counts = count_n_grams(sentences, 4)
    qintgram_counts = count_n_grams(sentences, 5)

    n_gram_counts_list = [unigram_counts, bigram_counts, trigram_counts, quadgram_counts, qintgram_counts]
    previous_tokens = ["i", "like"]
    tmp_suggest3 = get_suggestions(previous_tokens, n_gram_counts_list, unique_words)

    print(f"The previous words are 'i like', the suggestions are:")
    print(tmp_suggest3)

    previous_tokens = ["i", "am", "to"]
    tmp_suggest4 = get_suggestions(previous_tokens, n_gram_counts_list, unique_words)

    ## Get n-gram
    n_gram_counts_list = []
    for n in range(1, 6):
        print("Computing n-gram counts with n =", n, "...")
        n_model_counts = count_n_grams(data, n)
        n_gram_counts_list.append(n_model_counts)

    print(f"The previous words are {previous_tokens}, the suggestions are:")
    print(tmp_suggest4)

    previous_tokens = ["i", "want", "to", "go"]
    tmp_suggest5 = get_suggestions(previous_tokens, n_gram_counts_list, unique_words)

    print(f"The previous words are {previous_tokens}, the suggestions are:")
    print(tmp_suggest5)

    previous_tokens = ["hey", "how", "are"]
    tmp_suggest6 = get_suggestions(previous_tokens, n_gram_counts_list, unique_words)

    print(f"The previous words are {previous_tokens}, the suggestions are:")
    print(tmp_suggest6)

    previous_tokens = ["hey", "how", "are", "you"]
    tmp_suggest7 = get_suggestions(previous_tokens, n_gram_counts_list, unique_words)

    print(f"The previous words are {previous_tokens}, the suggestions are:")
    print(tmp_suggest7)

    previous_tokens = ["hey", "how", "are", "you"]
    tmp_suggest8 = get_suggestions(previous_tokens, n_gram_counts_list, unique_words, start_with="d")

    print(f"The previous words are {previous_tokens}, the suggestions are:")
    print(tmp_suggest8)
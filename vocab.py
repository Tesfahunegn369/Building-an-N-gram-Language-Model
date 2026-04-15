from count import count_words

def get_words_with_nplus_frequency(tokenized_sentences, count_threshold):
    """
    Find the words that appear N times or more

    Args:
        tokenized_sentences: List of lists of sentences
        count_threshold: minimum number of occurrences for a word to be in the closed vocabulary.

    Returns:
        List of words that appear N times or more
    """
    # Initialize an empty list to contain the words that
    # appear at least 'minimum_freq' times.
    closed_vocab = []

    # Get the word couts of the tokenized sentences
    # Use the function that you defined earlier to count the words
    word_counts = count_words(tokenized_sentences)

    # for each word and its count
    for word, cnt in word_counts.items():  # complete this line

        # check that the word's count
        # is at least as great as the minimum count
        if cnt >= count_threshold:
            # append the word to the list
            closed_vocab.append(word)

    return closed_vocab


def replace_oov_words_by_unk(tokenized_sentences, vocabulary, unknown_token="<unk>"):
    """
    Replace words not in the given vocabulary with '<unk>' token.

    Args:
        tokenized_sentences: List of lists of strings
        vocabulary: List of strings that we will use
        unknown_token: A string representing unknown (out-of-vocabulary) words

    Returns:
        List of lists of strings, with words not in the vocabulary replaced
    """

    # Place vocabulary into a set for faster search
    vocabulary = set(vocabulary)

    # Initialize a list that will hold the sentences
    # after less frequent words are replaced by the unknown token
    replaced_tokenized_sentences = []

    # Go through each sentence
    for sentence in tokenized_sentences:

        # Initialize the list that will contain
        # a single sentence with "unknown_token" replacements
        replaced_sentence = []

        # for each token in the sentence
        for token in sentence:  # complete this line

            # Check if the token is in the closed vocabulary
            if token in vocabulary:  # complete this line
                # If so, append the word to the replaced_sentence
                replaced_sentence.append(token)
            else:
                # otherwise, append the unknown token instead
                replaced_sentence.append(unknown_token)

        # Append the list of tokens to the list of lists
        replaced_tokenized_sentences.append(replaced_sentence)

    return replaced_tokenized_sentences


########################################################################################################################

def vocab_test():
    tokenized_sentences = [['sky', 'is', 'blue', '.'],
                           ['leaves', 'are', 'green', '.'],
                           ['roses', 'are', 'red', '.']]
    tmp_closed_vocab = get_words_with_nplus_frequency(tokenized_sentences, count_threshold=2)
    print(f"Closed vocabulary:")
    print(tmp_closed_vocab)

def oov_test():
    tokenized_sentences = [["dogs", "run"], ["cats", "sleep"]]
    vocabulary = ["dogs", "sleep"]
    tmp_replaced_tokenized_sentences = replace_oov_words_by_unk(tokenized_sentences, vocabulary)
    print(f"Original sentence:")
    print(tokenized_sentences)
    print(f"tokenized_sentences with less frequent words converted to '<unk>':")
    print(tmp_replaced_tokenized_sentences)
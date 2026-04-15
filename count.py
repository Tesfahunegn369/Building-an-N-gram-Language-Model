
# Q2: Implement word count function (15 pts)
def count_words(tokenized_sentences):
    """
    Count the number of word appearence in the tokenized sentences

    Args:
        tokenized_sentences: List of lists of strings

    Returns:
        dict that maps word (str) to the frequency (int)
    """

    word_counts = {}
    ### START CODE HERE (Replace instances of 'None' with your code) ###

    # Loop through each sentence
    for sentence in tokenized_sentences:  # complete this line

        # Go through each token in the sentence
        for token in sentence:  # complete this line

            # If the token is not in the dictionary yet, set the count to 1
            if token not in word_counts:  # complete this line
                word_counts[token] = 1

            # If the token is already in the dictionary, increment the count by 1
            else:
                word_counts[token] += 1

    ### END CODE HERE ###

    return word_counts


########################################################################################################################

def count_test(sentences):
    print("\n## Q2: Count words (15 pts)")
    count_result = count_words(sentences)
    print("Counting words" + str(count_result))
    if count_result == {'i': 1, 'like': 2, 'a': 2, 'cat': 2, 'this': 1, 'dog': 1, 'is': 1}:
        print('SUCCESS')
    else:
        print('FAIL')
        exit(1)
    print('')



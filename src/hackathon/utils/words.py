from nltk.corpus import words, wordnet
import nltk
import random

#%% Downloads
nltk.download('wordnet', quiet=True)
nltk.download('words', quiet=True)

#%% Functions
def get_word(word_length):
    """
    Generate a random {word_length} letter word from the English language corpus.

    Returns
    -------
    str:
        Random {word_length} letter word.

    """
    english_words = words.words()
    answer = [word for word in english_words if len(word) == word_length]
    return random.choice(answer).upper()

def get_definition(word):
    """
    Returns the definition of a word using wordnet.

    Parameters
    ----------
    word : str
        The randomly generated word.

    Returns
    -------
    str
        The definition of the word.

    """
    word_syonym_set = wordnet.synsets(word)
    if word_syonym_set:
        word_name = word_syonym_set[0]
        return word_name.definition()
    else:
        return

def word_def_pair(word_length=5):
    """
    Get word-definition as a tuple

    Args:
        word_length (int, optional): length of word. Defaults to 5.

    Returns:
        tuple: word-definition pair.

    """

    # Give the word only if a definition for it
    # has been found
    definition = None
    while not definition:
        word = get_word(word_length)
        definition = get_definition(word)

    return (word, definition)


#%% Example and testing
if __name__== '__main__':
    word = get_word()
    print(f"Hocus pocus randomus wordus: {word} \n Definition: {get_definition(word)}")

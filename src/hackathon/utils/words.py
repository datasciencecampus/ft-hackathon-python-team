import random

import nltk
from nltk.corpus import wordnet, words

# %% Downloads
nltk.download('wordnet', quiet=True)
nltk.download('words', quiet=True)
#%% Functions

def get_word(word_length: int=5)-> str:
    """
    Generate a random {word_length} letter word from the English language corpus.

    Returns
    -------
    str:
        Random {word_length} letter word.

    """
    if word_length == 5:
        path = r'./docs/word_list.txt'
        with open(path, 'r') as file:
            target = random.choice(file.read().split('\n')).upper()

    else:
        wordlist = [word for word in words.words() if len(word) == word_length]
        if wordlist:
            target = random.choice(wordlist).upper()
        else:
            raise IndexError(f'No words have length {word_length}')

    return target

def get_definition(word: str)->str:
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
    if len(word) == 5:
        path = r'./docs/guess_list.txt'
        with open(path, 'r') as f:
            content = f.read()
            if word.upper() not in content:
                return

    word_syonym_set = wordnet.synsets(word)
    if word_syonym_set:
        word_name = word_syonym_set[0]
        return word_name.definition()
    else:
        return

def word_def_pair(word_length: int=5)-> tuple:
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

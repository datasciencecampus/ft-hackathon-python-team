from nltk.corpus import words, wordnet
import nltk
import random

#%% Downloads
nltk.download('wordnet')
nltk.download('words')

#%% Functions
def random_word():
    """
    Generate a random five letter word from the English language corpus.

    Returns
    -------
    str:
        Random five letter word.

    """
    english_words = words.words()
    answer = [word for word in english_words if len(word) == 5]
    return random.choice(answer)

def return_word_definition(word):
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
        return (f"No definition available for {word}")

#%% Example and testing
if __name__== '__main__':
    word = random_word()
    print(f"Hocus pocus randomus wordus: {word} \n Definition: {return_word_definition(word)}")

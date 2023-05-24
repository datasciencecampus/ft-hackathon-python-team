from nltk.corpus import words, wordnet
import nltk
nltk.download('wordnet')
nltk.download('words')
import random

def random_word():
    english_words = words.words()
    answer = [word for word in english_words if len(word) == 5]
    return random.choice(answer)

def return_word_definition(word):
    word_syonym_set = wordnet.synsets(word)
    if word_syonym_set:
        word_name = word_syonym_set[0]
        return word_name.definition()
    else:
        return (f"No definition available for {word}")

word = random_word()
print(f"Hocus pocus randomus wordus: {word} \n Definition: {return_word_definition(word)}")

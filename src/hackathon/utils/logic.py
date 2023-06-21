# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 17:51:30 2023

@author: willin6
"""

# TODO: make constants file
RED = '#BB0A1E'
YELLOW = '#B59F3B'
GREEN = '#538D4E'
GREY = '#3A3A3C'
BLACK = '#000000'
WHITE = '#FFFFFF'

def check_placement(letter, idx, target):
    if letter == target[idx]:
        print(f'{letter} is in the correct position')
        color = GREEN
    elif letter in target and letter != target[idx]:
        print(f'{letter} is in the word but in the wrong position')
        color = YELLOW
    elif letter not in target:
        print(f'{letter} not in word')
        color = GREY
    return color

def n_letter(word, letter):
    n = word.count(letter)
    return n

def check_placement_letter(word, target):

    status = []
    for idx, letter in enumerate(word):
        if letter == target[idx]:
            print(f'{letter} is in the correct position')
            color = GREEN
        elif letter in target:
            if word.count(letter) > 1 and word.count(letter) == target.count(letter):
                print(f'{letter} is in the word but in the wrong position')
                color = YELLOW
            else:
                print(f'{letter} not in word')
                color = GREY
        else:
            print(f'{letter} not in word')
            color = GREY

        status.append((idx, letter, color))

    return status

if __name__ == '__main__':
    word = 'HELLO'
    target = 'WORLD'

    output = check_placement_letter(word, target)


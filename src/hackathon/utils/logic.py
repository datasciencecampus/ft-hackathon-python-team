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

def check_placement_letter(word, idx, target):
    print(word[idx])
    if n_letter(word, word[idx]) == 1 or n_letter(target,word[idx]) == n_letter(word,word[idx]) or word[idx] not in word[0:idx]:
        if word[idx] == target[idx]:
            print(f'{word[idx]} is in the correct position')
            color = GREEN
        elif word[idx] in target and word[idx] != target[idx]:
            print(f'{word[idx]} is in the word but in the wrong position')
            color = YELLOW
        elif word[idx] not in target:
            print(f'{word[idx]} not in word')
            color = GREY
    elif n_letter(word, word[idx]) > 1 and n_letter(target, word[idx]) <= 1:
        if word[idx] == target[idx]:
            print(f'{word[idx]} is in the correct position')
            color = GREEN
        else:
            print(f'{word[idx]} not in word')
            color = GREY
    
    return color

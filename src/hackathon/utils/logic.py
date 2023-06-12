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
        color = RED
    return color

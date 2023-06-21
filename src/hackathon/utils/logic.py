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


def get_result(word, target):
    w1 = [i for i in word]
    t1 = [i for i in target]

    output = []

    for idx, i in enumerate(w1):
        if w1[idx] == t1[idx]:
            w1[idx] = '*'
            t1[idx] = '*'
            output.append((idx, GREEN,  i))

    # Restart the loop with greens removed
    for idx, i in enumerate(w1):
        if i not in ['*',*[letter[2] for letter in output]]:
            if i in t1:
                w1[idx] = '-'
                t1[idx] = '-'
                output.append((idx, YELLOW, i))

    for idx, i in enumerate(w1):
        if i not in ['*','-']:
            output.append((idx, GREY, i))

    return sorted(output)


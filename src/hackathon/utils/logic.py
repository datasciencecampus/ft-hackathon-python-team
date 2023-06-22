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

def get_colours(word: str, target: str)-> list:
    """
    Compare user-submitted word
    against target and give colour
    based on placement

    Args:
        word (str): User's guess.
        target (str): Target word.

    Returns:
        lst_clue (list): Colours of each letter.

    """

    # Easiest if word is converted to a list
    lst_target = list(target)

    # Blank list ready to be populated with colours
    colours = ['' for i in target]

    for i, letter in enumerate(word):
        # First check for exact matches
        if letter == target[i]:
            colours[i] = GREEN
            # Remove exact matches from word so not double-counted
            lst_target[i] = None

    for i, letter in enumerate(word):

        if colours[i] == '':
            if letter in lst_target:
                colours[i] = YELLOW
                # Remove partial match so not double-counted
                lst_target.remove(letter)
            else:
                # Everything else must be grey by default
                colours[i] = GREY
    return colours

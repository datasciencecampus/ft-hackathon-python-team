# -*- coding: utf-8 -*-
"""
Created on Wed Jul  5 17:15:18 2023

@author: willin6
"""

ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

LETTER_COUNT = 0
# Initialise guess
GUESS_NUM = 1
WORD = ''

WORD_LENGTH = 5
NUM_GUESSES = 6

GREEN = '#538D4E'
YELLOW = '#B59F3B'
GREY = '#3A3A3C'

BLACK = '#121213'
WHITE = '#FFFFFF'

# Tuple needed for dark/light mode
THEME = (BLACK, WHITE)

# Use for all text
FONT = ('Helvetica', 24, 'bold')

# Number of rows the main window will have
SPAN = tuple([i for i in range(NUM_GUESSES+1)])

# Relative path to icons (should? work on any machine)
ICON_PATH = r'./src/hackathon/icons'

# max height for the letter boxes
BUTTON_MAX_HEIGHT = 80
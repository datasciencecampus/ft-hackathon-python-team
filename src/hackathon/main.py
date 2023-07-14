# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 15:48:59 2023

@author: willin6
"""

# %% Imports
from src.hackathon.utils.wordle import Wordle

# %% Main
if __name__ == "__main__":
    wordle = Wordle()
    wordle.focus_set()
    wordle.start_game()

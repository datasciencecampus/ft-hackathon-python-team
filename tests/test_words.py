# -*- coding: utf-8 -*-
"""
Created on Fri Jun 23 12:22:17 2023

Testing word-related functions

@author: willin6
"""
import src.hackathon.utils.words as words

def test_get_word():

    path = r'./docs/word_list.txt'
    with open(path, 'r') as file:
        contents = file.read()

        # 5 letter word must come from approve list
        assert words.get_word(5) in contents

        # != 5 letter word must come from NLTK
        assert words.get_word(6) not in contents

def test_get_defintion():
    # Cheese
    target_def = 'a solid food prepared from the pressed curd of milk'
    assert words.get_definition('Cheese') == target_def
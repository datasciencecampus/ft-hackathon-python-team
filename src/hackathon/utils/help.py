# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 15:37:04 2023

@author: willin6
"""
# %% Imports

from textwrap import dedent

import customtkinter as ctk

import src.hackathon.utils.constants as c
from src.hackathon.utils.letterbox import LetterBox

# %% Main

class Help(ctk.CTkToplevel):
    """Display instructions for how the game works"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.configure(fg_color=c.THEME[::-1])
        self.geometry("+0+0")
        self.title("Rules")

        self.add_intro_text()
        self.add_examples()

    def add_intro_text(self) -> None:
        """
        Add all the text bits to the help window.

        The end result should be:

        How To Play

        Guess the Wordle in 6 tries.

        - Each guess must be a valid 5-letter word
        - The colour of the tiles will change to show how close your
        guess was to the word.

        Examples

        Returns
        -------
        None.

        """

        # To add to the text just drop a line and continue.
        # NOTE: for now you'll have to updated the grid
        # rows in _example grid manually. Just increment them
        # all by the number of additions you've made.

        # TODO: find out how CTk tracks gridsize
        # and use that to only populate the next empty
        # row/column.

        text = dedent(
            f"""\
            How To Play
            Guess the Wordle in {c.NUM_GUESSES} tries.
            • Each guess must be a valid {c.WORD_LENGTH}-letter word
            • The colour of the tiles will change to show how close your guess was to the word.
            Examples
            """
        ).strip()

        for row, line in enumerate(text.split("\n")):
            # First or last row
            if row in [0, len(text.split("\n")) - 1]:
                font = ("Helvetica", 24, "bold", "underline")
                pady = 10
            else:
                font = ("Helvetica", 20)

            label = ctk.CTkLabel(self, text=line, font=font)
            label.grid(row=row, column=0, padx=10, pady=pady, sticky="nw")

    def add_examples(self) -> None:
        """
        Add three examples of the logic:
            - Right letter right place (green)
            - Right letter wrong place (yellow)
            - Wrong letter (grey)

        Returns
        -------
        None.

        TODO: Convert to for loop

        """

        words = ["WORDS", "FIGHT", "CLAMP"]

        font = ("Helvetica", 20)
        self._example_grid(6, c.GREEN, words[0])
        self._example_grid(8, c.YELLOW, words[1])
        self._example_grid(10, c.GREY, words[2])

        green_example = ctk.CTkLabel(
            self, text="W is in the word and in the correct spot.", font=font
        )

        yellow_example = ctk.CTkLabel(
            self, text="T is in the word but in the wrong spot.", font=font
        )
        grey_example = ctk.CTkLabel(
            self, text="C, A and P are not in the word in any spot.", font=font
        )
        green_example.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        yellow_example.grid(row=7, column=0, padx=10, pady=5, sticky="w")
        grey_example.grid(row=9, column=0, padx=10, pady=5, sticky="w")

    def _example_grid(self, row: int, colour: str, word: str) -> None:
        """
        Create a frame with 5 boxes in to display how colours change
        according to letter placement.

        Parameters
        ----------
        row : int
            Grid row.
        colour : str
            Colour the example box should be.

        Returns
        -------
        None.

        """

        # Box 1 green for green example
        # Box 5 yellow for yellow example
        # Box 1, 3 and give grey for grey example.

        # Using lists for box placement
        # so we can use IN to check box idx
        if colour == c.GREEN:
            colour_box = [0]

        elif colour == c.YELLOW:
            colour_box = [4]

        else:
            colour_box = [0, 2, 4]

        self.example_frame = ctk.CTkFrame(self, width=600, fg_color="transparent")
        self.example_frame.grid(row=row, column=0, padx=10, pady=10, sticky="w")

        for idx, letter in enumerate(word):
            if idx in colour_box:
                fg_color = colour
                hover_color = colour
            else:
                fg_color = "transparent"
                hover_color = c.THEME[::-1]

            box = LetterBox(
                self.example_frame,
                text=letter,
                fg_color=fg_color,
                hover_color=hover_color,
            )
            box.grid(row=0, column=idx, padx=5)
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 15:41:41 2023

@author: willin6
"""

from itertools import product

# %% Imports
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

import src.hackathon.utils.constants as c
from src.hackathon.utils.letterbox import LetterBox

# %% Main

class Main(ctk.CTkFrame):
    """Main frame of game. This holds the grid of LetterBoxes"""

    def __init__(self, parent: any):
        super().__init__(parent)

        self.configure(
            corner_radius=0,
            fg_color=c.THEME[::-1],
            width=parent.winfo_screenwidth() * 0.9,
        )

        self.grid(row=0, rowspan=c.NUM_GUESSES, column=1)

        self.grid_coords = {}
        self.create_grid(parent)

    def create_grid(self, parent: any) -> None:
        """
        Generate a grid of buttons.
        This will contain each letter.

        Parameters
        ----------
        parent : any
            Parent class.

        Returns
        -------
        None.

        """

        for row, col in product(
            range(parent.number_guesses), range(parent.word_length)
        ):
            btn = LetterBox(self)
            btn.grid(row=row, column=col, padx=2, pady=2)

            btn.grid_propagate(False)
            self.grid_coords[row, col] = btn

    def get_colours(self, parent: any) -> list:
        """
        Compares guessed word to target word and
        returns a list of colours corresponding to
        each letter.

        Parameters
        ----------
        parent : any
            Parent class.

        Returns
        -------
        colours : list
            List of colours, one per letter.

        """

        guess = parent.guess_word
        # Easiest if word is converted to a list
        target = list(parent.target_word)

        colours = ["" for i in target]

        for i, letter in enumerate(guess):
            # First check for exact matches
            if letter == target[i]:
                colours[i] = c.GREEN
                # Remove exact matches from word so not double-counted
                target[i] = None

        for i, letter in enumerate(guess):
            if colours[i] == "":
                if letter in target:
                    colours[i] = c.YELLOW
                    # Remove partial match from word so not double-counted
                    target.remove(letter)
                else:
                    # Everything else must be grey by default
                    colours[i] = c.GREY

        return colours

    def _shrink_box(self, button: LetterBox, max_height: int) -> None:
        """
        Simulate first part of box-flipping
        by decrementing the box height to a minimum

        Parameters
        ----------
        button : LetterBox
            Button to be animated.
        max_height : int
            Original height of button.

        Returns
        -------
        None.

        """

        # May be a bit off due to window-drawing quirks
        current_height = button.winfo_height()
        if current_height > max_height:
            current_height = max_height

        while current_height > 1:
            current_height -= 1
            button.configure(height=current_height)
            button.update()

        # Workaround for button flexing
        button.configure(height=1, border_color=c.THEME)

    def _expand_box(self, button, colour, max_height):
        button.configure(fg_color=colour, hover_color=colour)

        current_height = button.winfo_height()
        if current_height != 1:
            current_height = 1

        while button.winfo_height() <= max_height:
            current_height += 1
            button.configure(height=current_height)
            button.update()

        # Workaround for button flexing
        button.configure(height=max_height, border_color=c.THEME)

    def flip_box(
        self, button: LetterBox, colour: str, max_height: int = c.BUTTON_MAX_HEIGHT
    ) -> None:
        """
        Handler for total animation. Shrink box to minimum
        then expand back to original height.

        Parameters
        ----------
        button : LetterBox
            Button to be animated.
        colour : str
            Colour the button should be upon expanding.
        max_height : int, optional
            Original height. The default is c.BUTTON_MAX_HEIGHT.

        Returns
        -------
        None.

        """

        # Shrink animation
        self._shrink_box(button, max_height)
        # Expand animation
        self._expand_box(button, colour, max_height)

    def lose(self, parent: any) -> None:
        """
        Displays a messagebox with the correct
        word and option to quit or restart.

        Parameters
        ----------
        parent : any
            Parent class.

        Returns
        -------
        None.

        """

        box = CTkMessagebox(
            title="Try again?",
            cancel_button=None,
            message=f"The word was {parent.target_word}",
            icon=None,
            option_1="Retry",
            option_2="Quit",
            fade_in_duration=2,
        )
        box.focus_set()

        response = box.get()
        if response == "Retry":
            parent.restart_game()
        elif response == "Quit":
            parent.quit_game()

    def win(self, parent: any) -> None:
        """
        Display winning box and option to quit or restart.

        Parameters
        ----------
        parent : any
            Parent class.

        Returns
        -------
        None.

        """
        box = CTkMessagebox(
            parent,
            title="Correct!",
            cancel_button=None,
            message=f"The word was {parent.target_word}",
            icon=None,
            option_1="Retry",
            option_2="Quit",
            fade_in_duration=2,
        )
        box.focus_set()

        response = box.get()
        if response == "Retry":
            parent.restart_game()
        elif response == "Quit":
            parent.quit_game()

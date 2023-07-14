# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 15:44:51 2023

@author: willin6
"""

# %% Imports
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

import src.hackathon.utils.constants as c
from src.hackathon.utils.words import get_definition

# %% Main


class Keyboard(ctk.CTkFrame):
    """On-screen keyboard"""

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(
            corner_radius=0,
            fg_color=c.THEME[::-1],
            height=parent.winfo_screenheight() * 0.2,
            width=parent.winfo_screenwidth() * 0.9,
        )

        self.grid(rows=c.NUM_GUESSES + 1, column=1, pady=10)

        self.key_coords = {}
        self.add_keyboard_keys(parent)

        # Allows users to type
        parent.bind("<Key>", lambda event: self.key_pressed(event, parent))

    def _increment_letter_position(self, parent: any) -> None:
        parent.current_position += 1

    def _decrement_letter_position(self, parent: any) -> None:
        parent.current_position -= 1

    def _reset_letter_position(self, parent: any) -> None:
        parent.current_position = 0

    def _increment_guess_number(self, parent: any) -> None:
        parent.guess_number += 1

    def _decrement_guess_number(self, parent: any) -> None:
        parent.guess_number -= 1

    def _add_letter_to_word(self, parent: any, letter: str) -> None:
        parent.guess_word += letter

    def _remove_letter_from_word(self, parent: any) -> None:
        parent.guess_word = parent.guess_word[:-1]

    def _reset_word(self, parent: any) -> None:
        parent.guess_word = ""

    def add_keyboard_keys(self, parent: any) -> None:
        """
        Add on-screen keyboard.

        Returns
        -------
        None.

        """
        for idx, row in enumerate(c.KEYS):
            row_frame = ctk.CTkFrame(self, fg_color="transparent")
            row_frame.grid(row=idx + 1)
            for idy, key in enumerate(row):
                # These keys don't exist in Helvetica
                if key in ["⌫", "↵"]:
                    width = 80
                    _font = ("", 24)
                    width = 80
                    padx = 0
                    if key == "↵":
                        key = "ENTER"
                        _font = ("", 18)
                        padx = (0, 5)
                else:
                    _font = c.FONT
                    width = 50
                    padx = (0, 5)

                letter = ctk.CTkButton(
                    row_frame,
                    text=key,
                    width=width,
                    height=40,
                    font=_font,
                    fg_color=r"#787c7f",
                    hover_color=c.GREY,
                    command=lambda event=key: self.key_pressed(event, parent),
                )
                letter.grid_propagate(False)
                letter.grid(row=idx, column=idy, padx=padx, pady=(0, 5))

                self.key_coords[idx, idy] = letter

    def key_pressed(self, event: any, parent: any) -> None:
        """
        Handler for key press event. Adds
        whatever the user has typed or pressed
        to the LetterBoxes (unless delete/return).

        Parameters
        ----------
        event : any
            Key press event.
        parent : any
            Parent class.

        Returns
        -------
        None.

        """

        # Handle on-screen keyboard or physical key presses
        if isinstance(event, str):
            if event == "⌫":
                key = "BACKSPACE"
            elif event == "↵":
                key = "RETURN"
            else:
                key = event
        else:
            key = event.keysym.upper()

        if key in c.ALPHABET:
            self._add_letter(parent, key)

        elif key == "BACKSPACE":
            self._delete_letter(parent)

        elif key in ["RETURN", "ENTER"]:
            self.submit_guess(parent)

    def _add_letter(self, parent: any, key: str) -> None:
        """
        Add letter to next available space in grid.

        Parameters
        ----------
        parent : any
            Parent class.
        key : str
            Letter submitted.

        Returns
        -------
        None.

        """
        if parent.current_position < c.WORD_LENGTH:
            button = parent.main.grid_coords[
                parent.guess_number, parent.current_position
            ]
            button.configure(text=key)

            self._increment_letter_position(parent)
            self._add_letter_to_word(parent, key)

    def _delete_letter(self, parent: any) -> None:
        """
        Delete last latter from grid

        Parameters
        ----------
        parent : any
            Parent class.

        Returns
        -------
        None.

        """
        grid = parent.main.grid_coords
        if parent.current_position > 0:
            self._decrement_letter_position(parent)
            self._remove_letter_from_word(parent)
            button = grid[parent.guess_number, parent.current_position]
            button.configure(text="")

    def submit_guess(self, parent: any) -> None:
        """
        Handler for guess submission

        Parameters
        ----------
        parent : any
            Parent class.

        Returns
        -------
        None.

        """

        button_grid = parent.main.grid_coords

        if not get_definition(parent.guess_word):
            invalid = CTkMessagebox(
                parent,
                title="",
                fg_color="transparent",
                button_color="transparent",
                cancel_button=None,
                message=f"{parent.guess_word} is not a valid guess!",
                icon=None,
                option_1=None,
                option_2=None,
                fade_in_duration=1,
            )

            # Wait two seconds
            invalid.after(2000)
            invalid.destroy()

        elif parent.current_position == c.WORD_LENGTH:
            for idx, colour in enumerate(parent.main.get_colours(parent)):
                button = button_grid[parent.guess_number, idx]
                parent.main.flip_box(button, colour, c.BUTTON_MAX_HEIGHT)

            if parent.guess_word == parent.target_word:
                parent.main.win(parent)

            self._increment_guess_number(parent)
            self._reset_letter_position(parent)
            self._reset_word(parent)

        if parent.guess_number == c.NUM_GUESSES:
            parent.main.lose(parent)

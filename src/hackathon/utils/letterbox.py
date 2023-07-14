# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 15:39:53 2023

@author: willin6
"""

# %% Imports
import customtkinter as ctk

import src.hackathon.utils.constants as c


# %% Main
class LetterBox(ctk.CTkButton):
    """
    The default box that stores user guesses.
    There are no methods applied as this
    class exists solely to create a template
    box.
    """

    def __init__(
        self,
        parent: any,
        fg_color: str = "transparent",
        height: int = c.BUTTON_MAX_HEIGHT,
        width: int = c.BUTTON_MAX_HEIGHT,
        border_color: tuple = c.THEME,
        border_width: int = 1,
        corner_radius: int = 0,
        font: tuple = c.FONT,
        text: str = "",
        text_color: tuple = c.THEME,
        hover_color: tuple = c.THEME[::-1],
    ):
        super().__init__(
            parent,
            fg_color=fg_color,
            height=height,
            width=width,
            border_color=border_color,
            border_width=border_width,
            corner_radius=corner_radius,
            font=font,
            text=text,
            text_color=text_color,
            hover_color=hover_color,
        )

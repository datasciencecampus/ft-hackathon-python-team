# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 15:43:28 2023

@author: willin6
"""
# %% Imports
import customtkinter as ctk

import src.hackathon.utils.constants as c

from src.hackathon.utils.appearance import change_appearance
from src.hackathon.utils.in_work_mode import boss_is_watching


# %% Main
class Options(ctk.CTkFrame):
    """Side panel containing in-game options"""

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(
            corner_radius=0,
            fg_color=c.THEME[::-1],
            width=parent.winfo_screenwidth() * 0.1,
            height=parent.winfo_screenheight() * 0.5,
        )

        self.grid(
            row=0,
            column=0,
            rowspan=c.NUM_GUESSES + 1,
            sticky="nw",
        )
        self.grid_propagate(False)

        self.add_option_label()
        self.add_dark_mode()
        self.add_in_work_mode(parent)
        self.add_help_button(parent)
        self.add_retry_button(parent)
        self.add_quit_button(parent)

    def add_option_label(self) -> None:
        """
        Add option label to top
        of option frame.

        Returns
        -------
        None.

        """
        option_label = ctk.CTkLabel(self, text="Options", width=50)
        option_label.grid(row=0, column=0, sticky="n", padx=10)

        option_label.grid_propagate(False)

    def add_dark_mode(self) -> None:
        """
        Adds a switch to enable/disable
        dark mode. Enabled by default.

        Returns
        -------
        None.

        """
        # Initial value
        theme_toggle = ctk.StringVar(value="on")
        theme = ctk.CTkSwitch(
            self,
            width=110,
            text="Dark mode",
            onvalue="Dark",
            offvalue="light",
            border_color="transparent",
            variable=theme_toggle,
            progress_color=c.GREEN,
            command=lambda: change_appearance(theme_toggle),
        )
        theme.grid(row=1, column=0, sticky="ew", padx=10, pady=10)
        # Start with dark mode on
        theme.select()

    def add_in_work_mode(self, parent: any) -> None:
        """
        Adds a mode that switches
        the app to calculator
        and changes icons/titles. Off by default.

        TODO: Make it switch to a calculator

        Parameters
        ----------
        parent : any
            Parent class.

        Returns
        -------
        None.

        """
        # Initial value
        work_toggle = ctk.StringVar(value="no")
        in_work = ctk.CTkSwitch(
            self,
            width=110,
            text="Boss is in?",
            onvalue="yes",
            offvalue="no",
            border_color="transparent",
            variable=work_toggle,
            progress_color=c.GREEN,
            command=lambda: boss_is_watching(work_toggle, parent, c.ICON_PATH),
        )

        in_work.grid(row=2, column=0, padx=10)

        in_work.grid_propagate(False)

    def add_help_button(self, parent) -> None:
        """
        Opens up a help window containing instructions.

        Parameters
        ----------
        parent : any
            Parent class.

        Returns
        -------
        None.

        """

        help_button = ctk.CTkButton(
            self, text="Help", fg_color=c.GREEN, width=80, command=parent.help_window
        )
        help_button.grid(row=3, column=0, padx=10, pady=10)

        help_button.grid_propagate(False)

    def add_retry_button(self, parent: any) -> None:
        """
        Adds a retry button to the options
        pane that restarts the app when clicked.

        Parameters
        ----------
        parent : any
            Parent class.

        Returns
        -------
        None.

        """

        quit_button = ctk.CTkButton(
            self, text="Retry", fg_color=c.GREEN, width=80, command=parent.restart_game
        )
        quit_button.grid(row=4, column=0, padx=10, pady=10)

        quit_button.grid_propagate(False)

    def add_quit_button(self, parent: any) -> None:
        """
        Adds a quit button to the options
        pane that closes the app when clicked.

        Parameters
        ----------
        parent : any
            Parent class.

        Returns
        -------
        None.

        """

        quit_button = ctk.CTkButton(
            self, text="Quit", fg_color=c.GREEN, width=80, command=parent.quit_game
        )
        quit_button.grid(row=5, column=0, padx=10, pady=10)

        quit_button.grid_propagate(False)

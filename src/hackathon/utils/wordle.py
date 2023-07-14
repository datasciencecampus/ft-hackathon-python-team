# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 15:46:33 2023

@author: willin6
"""

# %% Imports
import customtkinter as ctk

import src.hackathon.utils.constants as c
from src.hackathon.utils.help import Help
from src.hackathon.utils.keyboard import Keyboard
from src.hackathon.utils.mainframe import Main
from src.hackathon.utils.options import Options
from src.hackathon.utils.words import word_def_pair

# %% Main
class Wordle(ctk.CTk):
    """Game window"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # General setup
        self.title("Team FinTrans Wordle")
        self.iconbitmap(rf"{c.ICON_PATH}/app_logo.ico")

        self.configure(fg_color=c.THEME[::-1])

        # Size
        self.geometry("+0+0")
        self.minsize(750, 680)

        # What to do when X is clicked
        self.protocol("WM_DELETE_WINDOW", self.quit_game)

        self.grid_columnconfigure((1), weight=1, uniform="a")
        self.grid_rowconfigure(c.SPAN, weight=1, uniform="a")

        # Stop main window shrinking to fit
        # widgets
        self.grid_propagate(False)

        # Initial values
        self.word_length = c.WORD_LENGTH
        self.number_guesses = c.NUM_GUESSES

        self.target_word = word_def_pair(self.word_length)[0]

        self.guess_number = 0
        self.current_position = 0

        self.guess_word = ""

        # Frames setup
        # Options menu
        self.options = Options(self)
        self.help_window = None

        # Main frame
        self.main = Main(self)

        # Keyboard
        self.keyboard = Keyboard(self)

    def start_game(self) -> None:
        """
        Starts the app.

        Returns
        -------
        None.

        """
        self.mainloop()

    def restart_game(self) -> None:
        """
        Restart the app.

        Returns
        -------
        None.

        """
        self.quit_game()
        self.__init__()
        self.start_game()

    def quit_game(self) -> None:
        """
        Closes the app.

        Returns
        -------
        None.

        """
        print("Quitting...\n")
        self.update_idletasks()
        self.quit()
        self.destroy()

    def help_window(self) -> None:
        """
        Bring up help window and focus.

        Returns
        -------
        None.

        """
        # Ensures only one help window opens
        if self.help_window is None or not self.help_window.winfo_exists():
            self.help_window = Help(self)
        self.help_window.grab_set()

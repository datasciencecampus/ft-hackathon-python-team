# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 14:10:12 2023

@author: willin6
"""

# %% Functions
from itertools import product
from textwrap import dedent
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import src.hackathon.utils.constants as c
from src.hackathon.utils.appearance import change_appearance
from src.hackathon.utils.in_work_mode import boss_is_watching
from src.hackathon.utils.words import get_definition, word_def_pair
# from typing import Union, Tuple, Callable, Optional, Dict

# %% Main
# Dark by default
ctk.set_appearance_mode("dark")
# Default theme
ctk.set_default_color_theme("green")


class Help(ctk.CTkToplevel):
    """Display instructions for how the game works"""

    def __init__(self, parent, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.configure(fg_color = c.THEME[::-1])
        self.geometry("+0+0")
        self.title('Rules')
        
        self.add_intro_text()
        self.add_examples()
    
    def add_intro_text(self):
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
        
        text = dedent(f"""\
            How To Play
            Guess the Wordle in {c.NUM_GUESSES} tries.
            • Each guess must be a valid {c.WORD_LENGTH}-letter word
            • The colour of the tiles will change to show how close your guess was to the word.
            Examples
            """).strip()
            
        for row, line in enumerate(text.split('\n')):
            
            # First or last row
            if row in [0, len(text.split('\n'))-1]:
                font = ('Helvetica', 24, 'bold', 'underline')
                pady = 10
            else:
                font = ('Helvetica', 20)
                
            
            label = ctk.CTkLabel(self,
                                 text = line,
                                 font = font)
            
            label.grid(row = row,
                       column = 0,
                       padx = 10,
                       pady = pady,
                       sticky = 'nw')
                
    def add_examples(self):
    
        # These are just used
        # for the example page
        words = [
            'WORDS',
            'FIGHT',
            'CLAMP',
            ]
        
        font = ('Helvetica', 20)
        self._example_grid(6, c.GREEN, words[0])
        self._example_grid(8, c.YELLOW, words[1])
        self._example_grid(10, c.GREY, words[2])

        green_example = ctk.CTkLabel(self, 
                                     text = 'W is in the word and in the correct spot.',
                                     font = font,
                                     )

        
        yellow_example = ctk.CTkLabel(self, 
                                      text = 'T is in the word but in the wrong spot.',
                                      font = font,
                                      )
        grey_example = ctk.CTkLabel(self, 
                                    text = 'C, A and P are not in the word in any spot.',
                                    font = font,
                                    )
        green_example.grid(row = 5, 
                           column = 0,
                           padx = 10, 
                           pady = 5,
                           sticky = 'w')
        yellow_example.grid(row = 7, 
                            column = 0, 
                            padx = 10, 
                            pady = 5, 
                            sticky = 'w')
        grey_example.grid(row = 9, 
                          column = 0, 
                          padx = 10, 
                          pady = 5, 
                          sticky = 'w')
        
    def _example_grid(self, row, colour, word='WORDS', **kwargs):
        """
        Create a frame with 5 boxes in
        to display how colours change
        according to letter placement.

        Parameters
        ----------
        row : TYPE
            DESCRIPTION.
        colour : TYPE
            DESCRIPTION.

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

        self.example_frame = ctk.CTkFrame(self,
                                          width = 600,
                                          fg_color = 'transparent',
                                          )
        self.example_frame.grid(row = row,
                                column = 0,
                                padx = 10,
                                pady = 10, 
                                sticky = 'w',
                                **kwargs,
                                )


        for idx, letter in enumerate(word):

            if idx in colour_box:
                fg_color = colour
                hover_color = colour
            else:
                fg_color = 'transparent'
                hover_color = c.THEME[::-1]
            box = LetterBox(self.example_frame,
                            text = letter,
                            fg_color = fg_color,
                            hover_color = hover_color)
            box.grid(row = 0,
                     column = idx,
                     padx = 5)


class LetterBox(ctk.CTkButton):
    """Default box for the letters to go in"""

    def __init__(
            self,
            parent,
            fg_color: str = 'transparent',
            height: int = c.BUTTON_MAX_HEIGHT,
            width: int = c.BUTTON_MAX_HEIGHT,
            border_color: tuple = c.THEME,
            border_width: int = 1,
            corner_radius: int = 0,
            font: tuple = c.FONT,
            text: str = "",
            text_color: tuple = c.THEME,
            hover_color: tuple = c.THEME[::-1]
            ):

        super().__init__(
            parent,
            fg_color = fg_color,
            height = height,
            width = width,
            border_color = border_color,
            border_width = border_width,
            corner_radius = corner_radius,
            font = font,
            text = text,
            text_color = text_color,
            hover_color = hover_color,
            )



# Main Frame
class Main(ctk.CTkFrame):
    """Main frame of game"""

    def __init__(self, parent):
        super().__init__(parent)

        self.configure(
            corner_radius=0,
            fg_color=c.THEME[::-1],
            width=parent.winfo_screenwidth() * 0.9,
        )

        self.grid(row=0, rowspan=c.NUM_GUESSES, column=1)

        self.grid_coords = {}
        self.create_grid(parent)

    def create_grid(self, parent):
        """
        Generate a grid of buttons.
        This will contain each letter.

        Parameters
        ----------
        parent : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        for row, col in product(
            range(parent.number_guesses), range(parent.word_length)
        ):
            btn = LetterBox(self)
            btn.grid(
                row=row,
                column=col,
                padx=2,
                pady=2,
            )

            btn.grid_propagate(False)
            self.grid_coords[row, col] = btn

    def get_colours(self, parent):
        """
        Compare user-submitted word
        against target and give colour
        based on placement

        Parameters
        ----------
        parent : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

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

    def _shrink_box(self, button, max_height):
        """
        Simulate first part of box-flipping
        by decrementing the box height to a minimum

        Args:
            button (ctk.CTkButton): The button to be shrunk.
        """

        # Should be 100 but may be a bit off
        # due to window-drawing quirks
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

    def flip_box(self, button, colour, max_height=c.BUTTON_MAX_HEIGHT):
        """
        Handler for total animation.

        Args:
            button (ctk.CTkButton): The button that was clicked.
            colour (str): The color to be applied to the button.
        """

        # Shrink animation
        self._shrink_box(button, max_height)
        # Expand animation
        self._expand_box(button, colour, max_height)

    def lose(self, parent):
        """
        Simulate second part of box-flipping
        by incrementing the box height to the original height
        Args:
            button (ctk.CTkButton): The button to be expanded.
            colour (str): The color to be applied to the button.
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

    def win(self, parent):
        """
        Display winning box with option
        to retry or quit

        Parameters
        ----------
        parent : TYPE
            DESCRIPTION.

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


# %%
# Options Frame
class Options(ctk.CTkFrame):
    """Panel containing in-game options"""

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

    def add_option_label(self):
        """
        Add option label to top
        of option frame

        Returns
        -------
        None.

        """
        option_label = ctk.CTkLabel(
            self,
            text="Options",
            width=50,
        )
        option_label.grid(
            row=0,
            column=0,
            sticky="n",
            padx=10,
        )

        option_label.grid_propagate(False)

    def add_dark_mode(self):
        """
        Adds a switch to enable/disable
        dark mode. Enabled by default

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
        theme.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=10,
            pady=10,
        )
        # Start with dark mode on
        theme.select()

    def add_in_work_mode(self, parent):
        """
        Adds a mode that switches
        the app to calculator
        and changes icons/titles. Off by default.

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

        in_work.grid(
            row=2,
            column=0,
            padx=10,
        )

        in_work.grid_propagate(False)

    def add_help_button(self, parent):
        """
        Opens up a help window.

        Parameters
        ----------
        parent : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        help_button = ctk.CTkButton(
            self,
            text="Help",
            fg_color=c.GREEN,
            width=80,
            command=parent.help_window,
        )
        help_button.grid(
            row=3,
            column=0,
            padx=10,
            pady=10,
        )

        help_button.grid_propagate(False)

    def add_retry_button(self, parent):
        """
        Adds a retry button to the options
        pane that restarts the app when clicked.

        Parameters
        ----------
        parent : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        quit_button = ctk.CTkButton(
            self,
            text="Retry",
            fg_color=c.GREEN,
            width=80,
            command=parent.restart_game,
        )
        quit_button.grid(
            row=4,
            column=0,
            padx=10,
            pady=10,
        )

        quit_button.grid_propagate(False)

    def add_quit_button(self, parent):
        """
        Adds a quit button to the options
        pane that closes the app when clicked.

        Parameters
        ----------
        parent : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        quit_button = ctk.CTkButton(
            self,
            text="Quit",
            fg_color=c.GREEN,
            width=80,
            command=parent.quit_game,
        )
        quit_button.grid(
            row=5,
            column=0,
            padx=10,
            pady=10,
        )

        quit_button.grid_propagate(False)


# Keyboard Frame
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

        self.grid(
            rows=c.NUM_GUESSES + 1,
            column=1,
            pady=10,
        )

        self.key_coords = {}
        self.add_keyboard_keys(parent)

        # Allows users to type
        parent.bind("<Key>", lambda event: self.key_pressed(event, parent))

    def _increment_letter_position(self, parent):
        parent.current_position += 1

    def _decrement_letter_position(self, parent):
        parent.current_position -= 1

    def _reset_letter_position(self, parent):
        parent.current_position = 0

    def _increment_guess_number(self, parent):
        parent.guess_number += 1

    def _decrement_guess_number(self, parent):
        parent.guess_number -= 1

    def _add_letter_to_word(self, parent, letter):
        parent.guess_word += letter

    def _remove_letter_from_word(self, parent):
        parent.guess_word = parent.guess_word[:-1]

    def _reset_word(self, parent):
        parent.guess_word = ""

    def add_keyboard_keys(self, parent):
        """
        Add keyboard layout

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
                letter.grid(
                    row=idx,
                    column=idy,
                    padx=padx,
                    pady=(0, 5),
                )

                self.key_coords[idx, idy] = letter

    def key_pressed(self, event, parent):
        """
        Handler for key press event

        Parameters
        ----------
        event : TYPE
            DESCRIPTION.
        parent : TYPE
            DESCRIPTION.

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

    def _add_letter(self, parent, key):
        """
        Add letter to next available space in grid

        Parameters
        ----------
        parent : TYPE
            DESCRIPTION.

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

    def _delete_letter(self, parent):
        """
        Delete last latter from grid

        Parameters
        ----------
        parent : TYPE
            DESCRIPTION.

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

    def submit_guess(self, parent):
        """
        Handler for guess submission

        Parameters
        ----------
        key : TYPE
            DESCRIPTION.
        parent : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """

        button_grid = parent.main.grid_coords

        if not get_definition(parent.guess_word):
            
            invalid = CTkMessagebox(
                parent,
                title="",
                fg_color='transparent',
                button_color='transparent',
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


# %%
# App
class App(ctk.CTk):
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

        print(self.target_word)

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

    def start_game(self):
        self.mainloop()
        # self.focus_set()

    def restart_game(self):
        self.quit_game()
        self.__init__()
        self.start_game()

    def quit_game(self):
        print("Quitting...\n")
        self.update()
        self.quit()
        self.destroy()

    def help_window(self):
        if self.help_window is None or not self.help_window.winfo_exists():
            self.help_window = Help(self)
        self.help_window.grab_set()


# %%
if __name__ == "__main__":
    app = App()
    app.start_game()

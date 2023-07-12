# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 14:10:12 2023

@author: willin6
"""

# %% Functions
import customtkinter as ctk
from typing import Union, Tuple, Callable, Optional, Dict

from src.hackathon.utils.words import word_def_pair, get_definition
from src.hackathon.utils.in_work_mode import boss_is_watching
from src.hackathon.utils.appearance import change_appearance
from src.hackathon.utils.logic import get_colours
import src.hackathon.utils.constants as c

from itertools import product

# %% Main
# Dark by default
ctk.set_appearance_mode('dark')
# Default theme
ctk.set_default_color_theme("green")   

# Main Frame
class Main(ctk.CTkFrame):
    """Main frame of game"""
    def __init__(self, parent):
        super().__init__(parent)
        
        self.configure(corner_radius = 0,
                       fg_color = c.THEME[::-1],
                       width = parent.winfo_screenwidth()*0.9,
                       )

        self.grid(row = 0,
                  rowspan = max(c.SPAN),
                  column = 1)
        
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
        
        for row, col in product(range(parent.number_guesses), 
                                range(parent.word_length)
                                ):
            btn = ctk.CTkButton(self,
                                fg_color = 'transparent',
                                height = c.BUTTON_MAX_HEIGHT,
                                width = c.BUTTON_MAX_HEIGHT,
                                border_color = c.THEME,
                                border_width = 1,
                                corner_radius=0,
                                font = c.FONT,
                                text = '',
                                text_color = c.THEME,
                                hover_color = c.THEME[::-1],
                                )
            btn.grid(row = row,
                     column = col,
                     padx = 2,
                     pady = 2,
                     sticky = 'ew')
            btn.grid_propagate(False)
            self.grid_coords[row, col] = btn


# Options Frame
class Options(ctk.CTkFrame):
    """Panel containing in-game options"""
    def __init__(self, parent):
        super().__init__(parent)
        
        self.configure(corner_radius = 0, 
                       fg_color = c.THEME[::-1],
                       width = parent.winfo_screenwidth()*0.1,
                       )
        


        self.grid(row = 0,
                  column = 0,
                  rowspan = c.NUM_GUESSES+1,
                  sticky = 'nw',
                  )
        self.grid_propagate(False)
        # self.grid_columnconfigure((0, 1), weight=2, uniform='tag')

        
        self.add_option_label()
        self.add_dark_mode()
        self.add_in_work_mode(parent)
        self.add_quit_button(parent)


    def add_option_label(self):
        """
        Add option label to top
        of option frame

        Returns
        -------
        None.

        """
        option_label = ctk.CTkLabel(self, 
                                    text = 'Options', 
                                    width = 50,
                                    )
        option_label.grid(row = 0, 
                          column = 0, 
                          sticky = 'n',
                          padx = 10,
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
        theme_toggle = ctk.StringVar(value='on')
        theme = ctk.CTkSwitch(self,
                              width = 110,
                              text = 'Dark mode',
                              onvalue = 'Dark',
                              offvalue = 'light',
                              border_color = 'transparent',
                              variable = theme_toggle,
                              progress_color = c.GREEN,
                              command=lambda: change_appearance(theme_toggle),
                              )       
        theme.grid(row=1, 
                   column=0, 
                   sticky='ew', 
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
        work_toggle = ctk.StringVar(value = 'no')
        in_work = ctk.CTkSwitch(self,
                                width = 110,
                                text = 'Boss is in?',
                                onvalue = 'yes',
                                offvalue = 'no',
                                border_color = 'transparent',
                                variable = work_toggle,
                                progress_color = c.GREEN,
                                command=lambda: boss_is_watching(work_toggle,
                                                                 parent,
                                                                 c.ICON_PATH),
                                )

        in_work.grid(row = 2, 
                     column = 0, 
                     padx = 10,
                     )
        
        in_work.grid_propagate(False)
    
    

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
        
        quit_button = ctk.CTkButton(self,
                                    text = 'Quit',
                                    fg_color = c.GREEN,
                                    width = 80,
                                    command = parent.quit_game,
                                    )
        quit_button.grid(row = 4, 
                         column = 0, 
                         padx = 10, 
                         pady = 10,
                         )
        
        quit_button.grid_propagate(False)


# Keyboard Frame
class Keyboard(ctk.CTkFrame):
    """On-screen keyboard"""
    def __init__(self, parent):
        super().__init__(parent)
        
        self.configure(corner_radius = 0,
                       fg_color = c.THEME[::-1],
                       height = parent.winfo_screenheight()*0.2,
                       width = parent.winfo_screenwidth()*0.9
                       )

        self.grid(rows = c.NUM_GUESSES+1,
                  column = 1,
                  )
        
        self.key_coords = {}
        
        self.add_keyboard_keys(parent)
        
        # Allows users to type
        parent.bind('<Key>', lambda event: self.key_pressed(event, parent))
    
    def _increment_letter_position(self, parent):
        parent.current_position += 1
        
    def _decrement_letter_position(self, parent):
        parent.current_position -= 1

    def _increment_guess_number(self, parent):
        parent.guess_number += 1
        
    def _decrement_guess_number(self, parent):
        parent.guess_number -= 1
    
    def _add_letter_to_word(self, parent, letter):
        parent.guess_word += letter
        
    def _remove_letter_from_word(self, parent):
        parent.guess_word = parent.guess_word[:-1]
        
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
            if event == '⌫':
                key = 'BACKSPACE'
            elif event == '↵':
                key = 'RETURN'
            else:
                key = event
        else:
            key = event.keysym.upper()
        
        # Avoids attempts to write to non-existent buttons
        if key in c.ALPHABET and parent.current_position < c.WORD_LENGTH:
            button = (parent
                      .main
                      .grid_coords[parent.guess_number, parent.current_position]
                      )
            button.configure(text=key)
            
            self._increment_letter_position(parent)
            self._add_letter_to_word(parent, key)
            
        elif key == 'BACKSPACE':
            if parent.current_position > 0:
                self._decrement_letter_position(parent)
                self._remove_letter_from_word(parent)
                button = (parent
                          .main
                          .grid_coords[parent.guess_number, parent.current_position]
                          )
                button.configure(text='')
            
            
    def add_keyboard_keys(self, parent):
        """
        Add keyboard layout

        Returns
        -------
        None.

        """
        for idx, row in enumerate(c.KEYS):
            row_frame = ctk.CTkFrame(self, 
                                     fg_color = 'transparent')
            row_frame.grid(row = idx+1)
            for idy, key in enumerate(row):
                 # These keys don't exist in Helvetica
                 if key in ['⌫','↵']:
                     width = 80
                     _font = ('', 24)
                     width = 80
                     padx=0
                     if key == '↵':
                         key = 'ENTER'
                         _font = ('', 18)
                         padx = (0, 5)
                 else:
                     _font = c.FONT
                     width=50
                     padx=(0,5)
        
                 letter = ctk.CTkButton(row_frame,
                                        text = key,
                                        width = width,
                                        height = 40,
                                        font = _font,
                                        fg_color = r'#787c7f',
                                        hover_color=c.GREY,
                                        command = lambda event=key: self.key_pressed(event, 
                                                                                     parent),
                                        )
                 letter.grid_propagate(False)
                 letter.grid(row = idx, 
                             column = idy, 
                             padx = padx, 
                             pady = (0,5),
                             )
        
                 self.key_coords[idx, idy] = letter               

def get_colours(word: str, target: str)-> list:
    """
    Compare user-submitted word
    against target and give colour
    based on placement

    Args:
        word (str): User's guess.
        target (str): Target word.

    Returns:
        lst_clue (list): Colours of each letter.

    """

    # Easiest if word is converted to a list
    lst_target = list(target)

    # Blank list ready to be populated with colours
    colours = ['' for i in target]

    for i, letter in enumerate(word):
        # First check for exact matches
        if letter == target[i]:
            colours[i] = GREEN
            # Remove exact matches from word so not double-counted
            lst_target[i] = None

    for i, letter in enumerate(word):

        if colours[i] == '':
            if letter in lst_target:
                colours[i] = YELLOW
                # Remove partial match so not double-counted
                lst_target.remove(letter)
            else:
                # Everything else must be grey by default
                colours[i] = GREY
    return colours

# Will display letters if typed or
# on-screen keyboard used
# root.bind('<Key>', key_pressed)
# %% 
# App
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # General setup
        self.title('Team FinTrans Wordle')
        self.iconbitmap(rf'{c.ICON_PATH}/app_logo.ico')
        
        self.configure(fg_color = c.THEME[::-1])
        
        # Size
        self.geometry('700x700+0+0')
        self.minsize(600,600)
        
        # What to do when X is clicked
        self.protocol('WM_DELETE_WINDOW', self.quit_game)
        
        self.grid_columnconfigure((1), weight=1, uniform='a')
        self.grid_rowconfigure(c.SPAN, weight=1, uniform='a')
        
        # Stop main window shrinking to fit
        # widgets
        self.grid_propagate(False)
        
        # Initial values
        self.word_length = c.WORD_LENGTH
        self.number_guesses = c.NUM_GUESSES
        self.guess_number = 0
        self.current_position = 0
        self.guess_word = ''
        
        
        # Frames setup
        
        # Options menu
        self.options = Options(self)
        
        # Main frame
        self.main = Main(self)
        
        # Keyboard
        self.keyboard = Keyboard(self)
        
    def start_game(self):
        self.mainloop()
        
            
    def quit_game(self):
        print('Qutting...')
        self.update()
        self.quit()
        self.destroy()
        
        

        
# %%
if __name__=='__main__':
    app = App()
    app.start_game()

# -*- coding: utf-8 -*-
"""
Convert to OOP test
@author: willin6
"""

# %% Functions
import customtkinter as ctk
from typing import Union, Tuple, Callable, Optional, Dict

from src.hackathon.utils.words import word_def_pair, get_definition
from src.hackathon.utils.quit import quit_game
from src.hackathon.utils.in_work_mode import boss_is_watching
from src.hackathon.utils.appearance import change_appearance
from src.hackathon.utils.logic import get_colours
from src.hackathon.utils.constants import *

from itertools import product

# %% Main

# Dark by default
ctk.set_appearance_mode('dark')
# Default theme
ctk.set_default_color_theme("green")   
class LetterButton(ctk.CTkButton):
    """Buttons to place letters in."""
    
    def __init__(self, 
                 master: any,
                 height: int = 80,
                 width: int = 80,
                 text: str = ' ',
                 font: Union[Tuple[str, int, str]] = FONT,
                 text_color: Union[str, Tuple[str, str]] = THEME,
                 fg_color: str = 'transparent',
                 border_color: Union[str, Tuple[str, str]] = THEME[::-1],
                 border_width: int = 1,
                 corner_radius: int = 0,
                 sticky: str = 'ew'):
        
        super().__init__(master)
        
        
        self.height = height
        self.width = width
        
        self.text = text
        self.font = font
        self.text_color = text_color
        
        self.fg_color = fg_color
        self.border_color = border_color
        self.sticky = sticky
        
        
class MainFrame(ctk.CTkFrame):
    """
    Frame containing the grid where
    user inputs guess
    """
    def __init__(self, 
                 master: any,
                 height: int = 530,
                 width: int = 450,
                 fg_color: str = 'transparent',
                 border_color: Union[str, Tuple[str, str]] = THEME[::-1],
                 buttons: Dict[Tuple[int, int], LetterButton] = {}
                 # **kwargs
                 ):
        super().__init__(master)
        
        self.width = width
        self.height = height
        
        self.fg_color = fg_color
        self.border_color = border_color

        self.buttons = buttons
        
        self._generate_button_grid(self.buttons, )
    def _generate_button_grid(self,
                              buttons: Dict[Tuple[int, int], LetterButton],
                              word_length: int = WORD_LENGTH, 
                              number_of_guesses: int = NUM_GUESSES)-> None:
        """

        Generate a (default) 5x6 grid of buttons to store user guesses.

        Parameters
        ----------
        word_length : int, optional
            Length of the word. The default is 5.
        number_of_guesses : int, optional
            Number of guesses. The default is 6.

        Returns
        -------
        None.

        """
        
        for row, column in product(range(word_length), range(number_of_guesses)):
            
            pos = (row, column)
            buttons[pos] = LetterButton(self)
            buttons[pos].grid(row=row, column=column)
            
                    
            

        

class OptionsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        config_options = {
            'width': 170, 
            'height': 490,
            'fg_color':'transparent',
            'border_color':THEME,
            }
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Window title
        self.title('Team FinTrans Wordle')
        # Size
        self.geometry('200x200+0+0')
        
        self.main_frame = MainFrame(self)
        
if __name__ == '__main__':
    app = App()
    app.mainloop()
        
        
        









































# %% Run
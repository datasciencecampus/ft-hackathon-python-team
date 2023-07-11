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
## Buttons

# Options Frame
class Options(ctk.CTkFrame):
    """Panel containing in-game options"""
    def __init__(self, parent):
        super().__init__(parent)
        
        self.configure(fg_color='transparent')

        self.place(x=0,
                   y=0,
                   relwidth=0.25, # % of window
                   relheight=1)

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
                                    width = 20,
                                    )
        option_label.grid(row = 0, 
                          column = 0, 
                          sticky = 'ew',
                          padx = 30,
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
                   padx=5,
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
                     padx = 5,
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
                         padx = 20, 
                         pady = 10,
                         )
        
        quit_button.grid_propagate(False)


# Keyboard Frame

# %% 
# App
class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Main setup
        # Window title
        self.title('Team FinTrans Wordle')
        self.iconbitmap(rf'{c.ICON_PATH}/app_logo.ico')
        
        # Size
        self.geometry('+0+0')
        self.minsize(600,600)
        
        # What to do when X is clicked
        self.protocol('WM_DELETE_WINDOW', self.quit_game)
        
        # Options menu
        self.options = Options(self)

        self.grid_columnconfigure((0, 1, 2), weight=1, uniform='a')
        self.grid_rowconfigure(c.SPAN, weight=1, uniform='a')
        
        # Stop main window shrinking to fit
        # widgets
        self.grid_propagate(False)
        
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

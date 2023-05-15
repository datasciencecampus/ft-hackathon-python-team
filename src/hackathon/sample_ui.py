# -*- coding: utf-8 -*-
"""
Created on Mon May 15 14:43:10 2023

@author: willin6
"""

import customtkinter as ctk

WORD_LENGTH = 5
NUM_GUESSES = 6

BLACK = '#000000'
WHITE = '#FFFFFF'

# Inherit system default (light/dark mode)
ctk.set_appearance_mode("System")

# Default options are blue, green or dark-blue
ctk.set_default_color_theme("blue")

# Begin with blank window
root = ctk.CTk()

# Window name
root.title("Team FinTrans Wordle")

# Generate 5x6 grid
for row in range(NUM_GUESSES):
    for column in range(WORD_LENGTH):

        # Frame needed to then place text boxes in
        # Corner radius defines the roundness
        # of the box corners
        text_frame = ctk.CTkFrame(root,
                                  height=80,
                                  width=80,
                                  fg_color='transparent',
                                  border_color=(BLACK, WHITE),
                                  border_width=1,
                                  corner_radius=5,
                                  )
        text_frame.grid(row=row,
                        column=column,
                        rowspan=1,
                        sticky='nsew',
                        padx=1,
                        pady=3)

        # Text box
        text = ctk.CTkEntry(text_frame,
                            text_color=(BLACK, WHITE),
                            font=('Arial',24))


submit_box = ctk.CTkEntry(root,
                          placeholder_text='Guess word',
                          fg_color='transparent',
                          text_color=(BLACK, WHITE))
submit_box.grid(row=NUM_GUESSES,
                column=1,
                columnspan=6)
# If left blank, will autofit
# existing elements
root.geometry()

# Static initial size
# root.geometry(f"{1100}x{580}")

# Display window
root.mainloop()
# -*- coding: utf-8 -*-

# %% Imports
import customtkinter as ctk
from src.hackathon.utils.words import word_def_pair, get_definition
from src.hackathon.utils.quit import quit_game
from src.hackathon.utils.in_work_mode import boss_is_watching
# %% Functions

# TODO: tidy this up
target = word_def_pair(5)
target_word = target[0].upper()
target_def = target[1]

count = 0
print(target_word)
def guess():
    global count
    word = submit_box.get().upper()

    # PLACEHOLDER - close if word right
    if word == target_word:
        print('yay')
        root.destroy()

    if not get_definition(word):
        print(f'{word} Not an English word')

    else:
        if len(word) == 5:
            for i in range(len(word)):
                displayBox = ctk.CTkTextbox(root,
                                            height=40,
                                            width=40,
                                            fg_color='transparent',
                                            border_color=(BLACK, WHITE)
                                            )
                displayBox.grid(row = count,
                                column = i,
                                columnspan = 1,
                                padx = 20,
                                pady = 20,
                                # sticky = "nsew"
                                )
                #   displayBox.delete("0.0","200.0")
                displayBox.insert("0.0",word[i])
            count = count + 1
            if count > 5:
                root.destroy()
    submit_box.delete(0,5)


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

# What to do when the X is clicked
root.protocol('WM_DELETE_WINDOW', lambda: quit_game(root))

# Window name
root.title("Team FinTrans Wordle")


root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure((0, 1, 2), weight=1)

# =============================================================================
# PANE 1
# =============================================================================
# This frame holds config options
sidebar = ctk.CTkFrame(root, width=50)

# It needs a weight in order to do stuff in
sidebar.grid_rowconfigure(0, weight=1)
sidebar.grid_columnconfigure(0, weight=1)

sidebar.grid(row=0,
             column=0,
             rowspan=10,
             sticky='nsew')

# Initial value
boss_switch = ctk.StringVar(value='no')
boss_watch = ctk.CTkSwitch(sidebar,
                           text="Boss is in?",
                           command=lambda: boss_is_watching(boss_switch),
                           variable=boss_switch,
                           onvalue="yes",
                           offvalue="no",
                           border_color=(WHITE, BLACK),
                           bg_color='transparent')

boss_watch.grid(row=NUM_GUESSES+2, column=0, padx=20, pady=0)
# Text above option menu
ui_scale = ctk.CTkLabel(sidebar, text='Scaling:', anchor='w')
ui_scale.grid(row=NUM_GUESSES-1, column=0, padx=20, pady=10)
# Clickable options
ui_scale_options = ctk.CTkOptionMenu(sidebar,
                                     values=[f'{i}%' for i in range(80, 130, 10)],
                                     command = change_scaling)
ui_scale_options.grid(row=NUM_GUESSES, column=0, padx=20, pady=0)
ui_scale_options.set('100%')


switch_var = ctk.StringVar(value="on")
theme = ctk.CTkSwitch(sidebar,
                      text="Dark mode",
                      command=lambda: change_appearance(switch_var),
                      variable=switch_var,
                      onvalue="Dark",
                      offvalue="Light",
                      border_color=(WHITE, BLACK),
                      bg_color='transparent')
theme.select()

theme.grid(row=NUM_GUESSES+1, column=0, padx=20, pady=(10, 10), sticky='s')


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
                column=0,
                columnspan=4)

guess_button = ctk.CTkButton(master = root,
                             text = "Guess",
                             command = guess)

guess_button.grid(row = NUM_GUESSES,
                  column = 3,
                  columnspan = 6)

# Make pressing enter do the same thing
# as clicking the Submit guess button
root.bind('<Return>', lambda event: guess())

# If left blank, will autofit
# existing elements
root.geometry()

# Static initial size
# root.geometry(f"{1100}x{580}")

# Display window
root.mainloop()
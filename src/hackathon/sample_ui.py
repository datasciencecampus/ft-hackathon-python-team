# -*- coding: utf-8 -*-

# %% Imports
import customtkinter as ctk
from src.hackathon.utils.words import word_def_pair, get_definition
from src.hackathon.utils.quit import quit_game
from src.hackathon.utils.in_work_mode import boss_is_watching
from src.hackathon.utils.appearance import change_appearance
from src.hackathon.utils.scaling import change_scaling
from src.hackathon.utils.logic import check_placement
from src.hackathon.utils.slide_panel import SlidePanel
from PIL import Image
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
            for idx, letter in enumerate(word):

                box_colour = check_placement(letter, idx, target_word)
                text_boxes[(count, idx)].insert("0.0", letter)
                text_boxes[(count, idx)].configure(bg_color=box_colour)
                text_frames[(count, idx)].configure(fg_color=box_colour)

            count = count + 1
            if count > 5:
                root.destroy()
    submit_box.delete(0, ctk.END)


WORD_LENGTH = 5
NUM_GUESSES = 6

RED = '#BB0A1E'
YELLOW = '#B59F3B'
GREEN = '#538D4E'
GREY = '#3A3A3C'
BLACK = '#000000'
WHITE = '#FFFFFF'

# Relative path to icons (should? work on any machine)
ICON_PATH = r'./src/hackathon/icons'

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
# This frame holds main game
main_frame = ctk.CTkFrame(root,
                          fg_color='transparent',
                          border_color=(BLACK, WHITE))
main_frame.grid(row=0,
                column=1,
                columnspan=WORD_LENGTH,
                rowspan=NUM_GUESSES)


# Need location of text frames
# to update bg colours later
text_frames = {}
text_boxes = {}

# Generate 5x6 grid
for row in range(NUM_GUESSES):
    for column in range(WORD_LENGTH):

        # Frame needed to then place text boxes in
        # Corner radius defines the roundness
        # of the box corners
        text_frame = ctk.CTkFrame(main_frame,
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

        # Prevent frame shrinking to fit
        # contents
        text_frame.grid_propagate(False)

        text_frames[(row, column)] = text_frame
        # Text box
        text = ctk.CTkTextbox(text_frame,
                              height=40,
                              width=40,
                              fg_color='transparent',
                              border_color=(BLACK, WHITE),
                              corner_radius=0,
                              font=('Droid', 28),
                              )

        text.grid(row=row,
                  column=column,
                  padx=22,
                  pady=20)

        text_boxes[(row, column)] = text

submit_box = ctk.CTkEntry(main_frame,
                          placeholder_text='Guess word',
                          fg_color='transparent',
                          text_color=(BLACK, WHITE))
submit_box.grid(row=NUM_GUESSES,
                column=0,
                columnspan=4)

guess_button = ctk.CTkButton(master = main_frame,
                             text = "Guess",
                             command = guess)

guess_button.grid(row = NUM_GUESSES,
                  column = 3,
                  columnspan = 2)

# =============================================================================
# PANE 4
# =============================================================================
# This frame holds options

animated_panel = SlidePanel(main_frame, 1.0, 0.5)
# Initial value
boss_switch = ctk.StringVar(value='no')
boss_watch = ctk.CTkSwitch(animated_panel,
                           text="Boss is in?",
                           variable=boss_switch,
                           onvalue="yes",
                           offvalue="no",
                           border_color=(WHITE, BLACK),
                           bg_color='transparent',
                           command=lambda: boss_is_watching(boss_switch,
                                                            root,
                                                            ICON_PATH),
                           )

boss_watch.grid(row=NUM_GUESSES+2, column=0, padx=20, pady=0)
# Text above option menu
ui_scale = ctk.CTkLabel(animated_panel, text='Scaling:', anchor='w')
ui_scale.grid(row=NUM_GUESSES-1, column=0, padx=20, pady=10)
# Clickable options
ui_scale_options = ctk.CTkOptionMenu(animated_panel,
                                     values=[f'{i}%' for i in range(80, 130, 10)],
                                     command = change_scaling)
ui_scale_options.grid(row=NUM_GUESSES, column=0, padx=20, pady=0)
ui_scale_options.set('100%')


switch_var = ctk.StringVar(value="on")
theme = ctk.CTkSwitch(animated_panel,
                      text="Dark mode",
                      command=lambda: change_appearance(switch_var),
                      variable=switch_var,
                      onvalue="Dark",
                      offvalue="Light",
                      border_color=(WHITE, BLACK),
                      bg_color='transparent')
theme.select()

theme.grid(row=NUM_GUESSES+1,
           column=0,
           padx=20,
           pady=(10, 10),
           sticky='s')

hamburger = ctk.CTkImage(light_image=Image.open(rf'{ICON_PATH}/hamburger_menu_light.ico'))
open_close = ctk.CTkButton(main_frame,
                           image=hamburger,
                           text="",
                           command=animated_panel.animate,
                           font=('Droid', 12),
                           corner_radius=8,
                           width=25,
                           height=25)

open_close.grid(row=NUM_GUESSES, column=5, padx=10)
open_close.grid_propagate(False)
# open_close.configure(r'D:/FinTrans/github_repos/hackathon/src/hackathon/icons/hamburger_menu_light.ico')
# Make pressing enter do the same thing
# as clicking the Submit guess button
root.bind('<Return>', lambda event: guess())

# If left blank, will autofit
# existing elements
root.geometry()

# Static initial size
# root.geometry(f"{1100}x{580}")
# Minimum size
root.minsize(500, 200)
# Display window
root.mainloop()
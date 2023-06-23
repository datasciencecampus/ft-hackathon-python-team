# -*- coding: utf-8 -*-

# %% Imports
import customtkinter as ctk
from src.hackathon.utils.words import word_def_pair, get_definition
from src.hackathon.utils.quit import quit_game
from src.hackathon.utils.focus import focus_start
from src.hackathon.utils.in_work_mode import boss_is_watching
from src.hackathon.utils.appearance import change_appearance
from src.hackathon.utils.logic import get_colours
from src.hackathon.utils.slide_panel import SlidePanel
from PIL import Image
# %% Functions
target_word, target_definition = word_def_pair(5)
print(target_word)

# Initialise guess
guess_number = 1


def guess():
    global guess_number
  #  global target_word
    word = submit_box.get().upper()

    # PLACEHOLDER - close if word right
    if word == target_word:
        print('yay')
        root.destroy()

    if not get_definition(word):
        print(f'{word} not a valid guess')

    else:
        if len(word) == WORD_LENGTH:

            status = get_colours(word, target_word)

            for idx, result in enumerate(status):

                pos = idx
                colour = status[idx]
                letter = word[idx]

                text_box = text_boxes[(guess_number-1, pos)]
                text_frame = text_frames[(guess_number-1, pos)]

                text_box.insert("0.0", letter)
                root.after(150, text_frame.configure(fg_color=colour))
                text_box.configure(bg_color=colour)

            guess_number += 1
            if guess_number > NUM_GUESSES:
                quit_game(root)
            else:
                # Remove text from box
                submit_box.delete(0, 'end')

WORD_LENGTH = 5
NUM_GUESSES = 6

RED = '#BB0A1E'
YELLOW = '#B59F3B'
GREEN = '#538D4E'
GREY = '#3A3A3C'
BLACK = '#000000'
WHITE = '#FFFFFF'
SPAN = tuple([i for i in range(NUM_GUESSES+2)])
# Relative path to icons (should? work on any machine)
ICON_PATH = r'./src/hackathon/icons'

# Needs to be dark by default
ctk.set_appearance_mode("Dark")

# Default options are blue, green or dark-blue
ctk.set_default_color_theme("blue")

# Begin with blank window
root = ctk.CTk()

# What to do when the X is clicked
root.protocol('WM_DELETE_WINDOW', lambda: quit_game(root))

# Window name
root.title("Team FinTrans Wordle")

# Weight grid so widgets move nicely
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(SPAN, weight=1)

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
                              text_color=WHITE,
                              )

        text.grid(row=row,
                  column=column,
                  padx=22,
                  pady=20)

        text_boxes[(row, column)] = text

# Where the user inputs word
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
# PANE 2
# =============================================================================
# This frame holds options
animated = False
# Panel slides in from the right
animated_panel = SlidePanel(main_frame, 1.0, 0.5)
static_panel = ctk.CTkFrame(root, height=550, width=150, fg_color='transparent')

if animated:
    panel = animated_panel
else:
    panel = static_panel
    panel.grid_propagate(False)
    panel.grid(row=0)
    panel.grid_columnconfigure(0, weight=1)

option_label = ctk.CTkLabel(panel,
                            text='Options',
                            # anchor='s',
                            width=50,
                            )
option_label.grid(row=0,
                  padx=20,
                  )
# Initial value
boss_switch = ctk.StringVar(value='no')
boss_watch = ctk.CTkSwitch(
    panel,
    width=110,
    text="Boss is in?",
    variable=boss_switch,
    onvalue="yes",
    offvalue="no",
    border_color=(WHITE, BLACK),
    # bg_color='transparent',
    command=lambda: boss_is_watching(boss_switch,
                                     root,
                                     ICON_PATH),
    )


# Default value
switch_var = ctk.StringVar(value="on")
# Dark/light mode
theme = ctk.CTkSwitch(panel,
                      width=110,
                      text="Dark mode",
                      command=lambda: change_appearance(switch_var),
                      variable=switch_var,
                      onvalue="Dark",
                      offvalue="Light",
                      border_color=(WHITE, BLACK),
                      # bg_color='transparent',
                      )
theme.select()

theme.grid(row=1, column=0, padx=20, pady=10)
boss_watch.grid(row=2, column=0, padx=20)

theme.grid_propagate(False)
option_label.grid_propagate(False)
boss_watch.grid_propagate(False)

# settings_cogs
if animated:
    cogs = ctk.CTkImage(light_image=Image.open(rf'{ICON_PATH}/settings_light_theme.ico'),
                        dark_image=Image.open(rf'{ICON_PATH}/settings_dark_theme.ico'))
    open_close = ctk.CTkButton(main_frame,
                               image=cogs,
                               text="",
                               command=panel.animate,
                               font=('Droid', 12),
                               corner_radius=8,
                               width=40,
                               height=25)

    open_close.grid(row=NUM_GUESSES, column=5, padx=10)
    open_close.grid_propagate(False)

# Make pressing enter do the same thing
# as clicking the Submit guess button
root.bind('<Return>', lambda event: guess())

root.bind('<FocusIn>', lambda event: focus_start(event=event, app=root, element=submit_box))
# If left blank, will autofit
# existing elements
root.geometry()

# Static initial size
# root.geometry(f"{1100}x{580}")
# Minimum size
root.minsize(500, 550)
# root.maxsize(500, 550)
# Display window
root.mainloop()


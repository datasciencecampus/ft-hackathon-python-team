# -*- coding: utf-8 -*-

# %% Imports
import customtkinter as ctk
from src.hackathon.utils.words import word_def_pair, get_definition

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
                column=0,
                columnspan=4)

guess_button = ctk.CTkButton(master = root,
                             text = "Guess",
                             command = lambda event: guess())

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
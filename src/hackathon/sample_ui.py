# -*- coding: utf-8 -*-

# %% Imports
import customtkinter as ctk
from src.hackathon.utils.words import word_def_pair, get_definition
from src.hackathon.utils.quit import quit_game
from src.hackathon.utils.in_work_mode import boss_is_watching
from src.hackathon.utils.appearance import change_appearance
from src.hackathon.utils.logic import get_colours
# %% Functions
def key_pressed(event):
    global LETTER_COUNT, word, GUESS_NUM, ks, target_word

    # This block handles both
    # typed keys and those
    # taken from on-screen keyboard
    # presses
    if isinstance(event, str):
        if event == '⌫':
            key = 'BACKSPACE'
        elif event == '↵':
            key = 'RETURN'
        else:
            key = event
    else:
        key = event.keysym.upper()

    # If we just used isalpha() then BACKSPACE and
    # RETURN would return True
    if key in ALPHABET and LETTER_COUNT < WORD_LENGTH:
        button = buttons[(GUESS_NUM-1, LETTER_COUNT)]
        button.configure(text=key)

        LETTER_COUNT += 1
        word += key


    elif len(word) == WORD_LENGTH and key in ['RETURN','ENTER']:
        if not get_definition(word):
            print(f'{word} not a valid guess')
        else:
            check_word(word, target_word)
            word = ''
            LETTER_COUNT = 0
            GUESS_NUM += 1

    elif key == 'BACKSPACE':
        if LETTER_COUNT > 0:
            LETTER_COUNT -= 1
            word = word[:-1]
            buttons[(GUESS_NUM-1, LETTER_COUNT)].configure(text='')


def check_word(word, target_word):
    # PLACEHOLDER - close if word right
    if word == target_word:
        print('yay')
        quit_game(root)

    if not get_definition(word):
        print(f'{word} not a valid guess')

    else:
        if len(word) == WORD_LENGTH:

            status = get_colours(word, target_word)

            for idx, result in enumerate(status):

                pos = idx
                colour = status[idx]
                letter = word[idx]

                button = buttons[(GUESS_NUM-1, pos)]

                button.configure(text=letter)
                button.configure(fg_color=colour)

            if GUESS_NUM > NUM_GUESSES:
                quit_game(root)
# %% Defaults
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Initialise guess
GUESS_NUM = 1

LETTER_COUNT = 0
word = ''


WORD_LENGTH = 5
NUM_GUESSES = 6

GREEN = '#538D4E'
YELLOW = '#B59F3B'
GREY = '#3A3A3C'

BLACK = '#121213'
WHITE = '#FFFFFF'

# WHITE = '#792DC3'

# Tuple needed for dark/light mode
THEME = (BLACK, WHITE)

# Use for all text
FONT = ('Helvetica', 24, 'bold')
# Number of rows the window will have
SPAN = tuple([i for i in range(NUM_GUESSES+1)])

# Relative path to icons (should? work on any machine)
ICON_PATH = r'icons/'

target_word, target_definition = word_def_pair(WORD_LENGTH)
print(target_word)

# Needs to be dark by default
ctk.set_appearance_mode("Dark")

# Default options are blue, green or dark-blue
ctk.set_default_color_theme("blue")

# Begin with blank window
root = ctk.CTk()
root.configure(fg_color=(WHITE, BLACK))

# What to do when the X is clicked
root.protocol('WM_DELETE_WINDOW', lambda: quit_game(root))

# Window name
root.title("Team FinTrans Wordle")

# Weight grid so widgets move nicely
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(SPAN, weight=1)

# %% Frames

# Main frame
frame_1 = ctk.CTkFrame(root, fg_color='transparent', border_color=THEME)
frame_1.grid(row=0, column=1, columnspan=WORD_LENGTH, rowspan=NUM_GUESSES)
frame_1.grid_columnconfigure(1, weight=1)
frame_1.grid_rowconfigure(SPAN, weight=1)

# Options frame
size_2 = {'width': 170, 'height': 490}
frame_2 = ctk.CTkFrame(root, fg_color='transparent', border_color=THEME, **size_2)
frame_2.grid(row=0, column=0)

# Stop window shrinking to fit contents
frame_2.grid_propagate(False)
frame_2.grid_columnconfigure(0, weight=1)

# Keyboard frame
frame_3 = ctk.CTkFrame(root, fg_color='transparent', border_color=THEME)
frame_3.grid(row=NUM_GUESSES+2, column=1)

# %% Buttons

# This will hold the coordinates of each button placed
buttons = {}
button_config = {
    'height' : 80,
    'width' : 80,
    'text': ' ', # should be blank to begin with,
    'text_color':THEME,
    'fg_color' : 'transparent',
    'border_color' : THEME,
    'border_width' : 1,
    'corner_radius' : 0,
    'font':FONT
    }
for row in range(NUM_GUESSES):
    for column in range(WORD_LENGTH):

        # Need to access buttons by position
        # to determine which letters go where
        coords = (row, column)
        button = ctk.CTkButton(frame_1, **button_config)
        button.grid(row=row, column=column, padx=1, pady=1, sticky='n')

        buttons[coords] = button


# %% Keyboard

# Will need key coords for
# button animation
key_coords = {}

keys = ['QWERTYUIOP',
        'ASDFGHJKL',
        '↵ZXCVBNM⌫']

for idx, row in enumerate(keys):
    row_frame = ctk.CTkFrame(frame_3, fg_color='transparent')
    row_frame.grid(row=idx+1)
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
            _font = FONT
            width=50
            padx=(0,5)

        letter = ctk.CTkButton(row_frame,
                               text=key,
                               width=width,
                               height=70,
                               font=_font,
                               fg_color=r'#787c7f',
                               command = lambda a=key: key_pressed(a))
        letter.grid_propagate(False)
        letter.grid(row=idx, column=idy, padx=padx, pady = (0,5))

        key_coords[(idx, idy)] = letter

# Will display letters if typed or
# on-screen keyboard used
root.bind('<Key>', key_pressed)
# %% Option menu

# Initial values
boss_switch = ctk.StringVar(value='no')
theme_switch = ctk.StringVar(value="on")

# This sits above the options
option_label = ctk.CTkLabel(frame_2, text='Options', width=50)

# Light/Dark mode
theme_config = {
    'width':110,
    'text':"Dark mode",
    'onvalue':"Dark",
    'offvalue':"Light",
    'border_color':'transparent',
    'variable':theme_switch,
    'progress_color':'#538D4E',
    }

# Dark/light mode
theme = ctk.CTkSwitch(frame_2, **theme_config, command=lambda: change_appearance(theme_switch))
# Start with dark mode on
theme.select()

# Boss is watching switch
boss_config = {
    'width':110,
    'text':"Boss is in?",
    'onvalue':"yes",
    'offvalue':"no",
    'border_color':'transparent',
    'variable':boss_switch,
    'progress_color':'#538D4E',

    }
boss_watch = ctk.CTkSwitch(
    frame_2,
    **boss_config,
    command=lambda: boss_is_watching(boss_switch,
                                     root,
                                     ICON_PATH),
    )


option_label.grid(row=0,padx=20)
theme.grid(row=1, column=0, padx=20, pady=10)
boss_watch.grid(row=2, column=0, padx=20)

theme.grid_propagate(False)
option_label.grid_propagate(False)
boss_watch.grid_propagate(False)


# %% Start game

# If left blank, will autofit
# existing elements
root.geometry()

# Disable resizing
root.resizable(False,False)

# Display window
root.mainloop()
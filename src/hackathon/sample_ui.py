# -*- coding: utf-8 -*-

# %% Imports
import customtkinter as ctk
from src.hackathon.utils.words import word_def_pair, get_definition
from src.hackathon.utils.quit import quit_game
from src.hackathon.utils.in_work_mode import boss_is_watching
from src.hackathon.utils.appearance import change_appearance
from src.hackathon.utils.logic import get_colours
# %% Functions
def button_clicked(button, colour, BUTTON_MAX_HEIGHT):
    """
    Handler for total animation.

    Args:
        button (ctk.CTkButton): The button that was clicked.
        colour (str): The color to be applied to the button.
    """
    # Shrink animation
    shrink_button(button, BUTTON_MAX_HEIGHT)
    # Expand animation
    expand_button(button, colour, BUTTON_MAX_HEIGHT)


def shrink_button(button, BUTTON_MAX_HEIGHT):
    """
    Simulate first part of box-flipping
    by decrementing the box height to a minimum

    Args:
        button (ctk.CTkButton): The button to be shrunk.
    """

    # Should be 100 but may be a bit off
    # due to window-drawing quirks
    current_height = button.winfo_height()
    if current_height > BUTTON_MAX_HEIGHT:
        current_height = BUTTON_MAX_HEIGHT

    while current_height > 1:
        current_height -= 1
        button.configure(height=current_height)
        button.update()

    # Workaround for button flexing
    button.configure(height=1, border_color=THEME)

def expand_button(button, colour, BUTTON_MAX_HEIGHT):
    button.configure(fg_color=colour, hover_color=colour)

    current_height = button.winfo_height()
    if current_height != 1:
        current_height = 1

    while button.winfo_height() <= BUTTON_MAX_HEIGHT:
        current_height += 1
        button.configure(height=current_height)
        button.update()

    # Workaround for button flexing
    button.configure(height=BUTTON_MAX_HEIGHT, border_color=THEME)


def check_win(root, WORD, target_word):
    """
    Simulate second part of box-flipping
    by incrementing the box height to the original height
    Args:
        button (ctk.CTkButton): The button to be expanded.
        colour (str): The color to be applied to the button.
    """
    if WORD == target_word:
        print('SPLENDID')
        quit_game(root)

# %% Functions
def key_pressed(event):
    global LETTER_COUNT, WORD, GUESS_NUM, ks, target_word

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
        WORD += key


    elif len(WORD) == WORD_LENGTH and key in ['RETURN','ENTER']:
        if not get_definition(WORD):
            print(f'{WORD} not a valid guess')
        else:
            colours = get_colours(WORD, target_word)
            for column in range(WORD_LENGTH):
                button = buttons[(GUESS_NUM - 1, column)]
                if button.cget('text') != '':
                    button_clicked(button, colours[column], BUTTON_MAX_HEIGHT)

                root.update_idletasks()
                root.after(2500, check_win, root, WORD, target_word)

            WORD = ''
            LETTER_COUNT = 0
            GUESS_NUM += 1

    elif key == 'BACKSPACE':
        if LETTER_COUNT > 0:
            LETTER_COUNT -= 1
            WORD = WORD[:-1]
            buttons[(GUESS_NUM-1, LETTER_COUNT)].configure(text='')
# %% Defaults
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

# Initialise guess
GUESS_NUM = 1

LETTER_COUNT = 0
WORD = ''

WORD_LENGTH = 5
NUM_GUESSES = 6

GREEN = '#538D4E'
YELLOW = '#B59F3B'
GREY = '#3A3A3C'

BLACK = '#121213'
WHITE = '#FFFFFF'

# Tuple needed for dark/light mode
THEME = (BLACK, WHITE)

# Use for all text
FONT = ('Helvetica', 24, 'bold')
# Number of rows the window will have
SPAN = tuple([i for i in range(NUM_GUESSES+1)])

# Relative path to icons (should? work on any machine)
ICON_PATH = r'./src/hackathon/icons'

BUTTON_MAX_HEIGHT = 80
target_word, target_definition = word_def_pair(WORD_LENGTH)
print(target_word)

# Needs to be dark by default
ctk.set_appearance_mode("Dark")

# Default options are blue, green or dark-blue
ctk.set_default_color_theme("blue")

# Begin with blank window
root = ctk.CTk()
root.configure(fg_color=(WHITE, BLACK))
# Add logo
root.iconbitmap(rf'{ICON_PATH}/app_logo.ico')

# What to do when the X is clicked
root.protocol('WM_DELETE_WINDOW', lambda: quit_game(root))

# Window name
root.title("Team FinTrans Wordle")

# Weight grid so widgets move nicely
root.grid_columnconfigure(1, weight=1)
root.grid_rowconfigure(SPAN, weight=1)

# %% Frames

# Main frame
config_1 = {
    'width':450,
    'height':530,
    'fg_color':'transparent',
    'border_color':THEME[::-1],
    }

if NUM_GUESSES == 6:
    frame_1 = ctk.CTkFrame(root, **config_1)
    frame_1.grid(row=0, column=1, columnspan=WORD_LENGTH, rowspan=NUM_GUESSES)
    frame_1.grid_rowconfigure(SPAN, weight=1)
    # frame_1.grid_propagate(False)
else:
    frame_1 = ctk.CTkScrollableFrame(root, **config_1)
    frame_1.grid(row=0, column=1, columnspan=WORD_LENGTH, rowspan=NUM_GUESSES)
    frame_1.grid_rowconfigure(SPAN, weight=1)
    frame_1.grid_propagate()

# Options frame
config_2 = {'width': 170, 'height': 490}
frame_2 = ctk.CTkFrame(root, fg_color='transparent', border_color=THEME, **config_2)
frame_2.grid(row=0, column=0)

# Stop window shrinking to fit contents
frame_2.grid_propagate(False)
frame_2.grid_columnconfigure(0, weight=1)

# Keyboard frame
frame_3 = ctk.CTkFrame(root, fg_color='transparent', border_color=THEME)
frame_3.grid(row=NUM_GUESSES+1, column=1)

# %% Buttons

# This will hold the coordinates of each button placed
buttons = {}
button_config = {
    'height' : BUTTON_MAX_HEIGHT,
    'width' : BUTTON_MAX_HEIGHT,
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
        button.grid(row=row, column=column, padx=2, pady=2, sticky='ew')
        button.grid_propagate(False)
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
                               height=40,
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
root.geometry('+0+0')

# Disable resizing
# root.resizable(False,False)

# Display window
root.mainloop()
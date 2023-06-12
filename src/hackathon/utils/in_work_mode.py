# -*- coding: utf-8 -*-

def boss_is_watching(boss_switch: str,
                     root,
                     ICON_PATH):

    # TODO: Turn into calculator app?

    new_answer = boss_switch.get()
    if new_answer == 'yes':
        root.title('Super serious work stuff')

        # Minimize when pressing left/right CTRL button
        root.bind('<Control_L>', lambda event: on_unmap())
        root.bind('<Control_R>', lambda event: on_unmap())

        root.iconbitmap(rf'{ICON_PATH}/placeholder_calculator.ico')
    else:
        # Window name
        root.title("Team FinTrans Wordle")
        root.iconbitmap(rf'{ICON_PATH}/placeholder_cat.ico')

def on_unmap(root):
    # Minimize
    root.wm_state('iconic')
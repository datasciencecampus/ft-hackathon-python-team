# -*- coding: utf-8 -*-

import customtkinter as ctk
def change_appearance(switch_var):
    new_mode = switch_var.get()
    ctk.set_appearance_mode(new_mode)


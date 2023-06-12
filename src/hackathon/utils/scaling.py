# -*- coding: utf-8 -*-

import customtkinter as ctk
def change_scaling(new_scale: str):
    new_scale = int(new_scale.replace('%','')) / 100
    ctk.set_widget_scaling(new_scale)

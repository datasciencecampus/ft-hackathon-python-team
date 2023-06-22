# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 16:46:52 2023

@author: willin6
"""

def focus_start(event, app, element):
    if event.widget == app:
        app.focus_set()
        element.focus_set()
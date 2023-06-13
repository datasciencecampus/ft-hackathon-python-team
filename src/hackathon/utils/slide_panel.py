# -*- coding: utf-8 -*-
"""
Created on Tue Jun 13 11:12:44 2023

@author: willin6
"""
import customtkinter as ctk

class SlidePanel(ctk.CTkFrame):
	def __init__(self, parent, start_pos, end_pos):
		super().__init__(master = parent)

		# general attributes
		self.start_pos = start_pos + 0.04
		self.end_pos = end_pos - 0.002
		self.width = abs(start_pos - end_pos)

		# animation logic
		self.pos = self.start_pos
		self.in_start_pos = True

		# layout
		self.place(relx = self.start_pos, rely = 0.05, relwidth = self.width, relheight = 1)

	def animate(self):
		if self.in_start_pos:
			self.animate_forward()
		else:
			self.animate_backwards()

	def animate_forward(self):
		if self.pos > self.end_pos:
			self.pos -= 0.008
			self.place(relx = self.pos, rely = 0.05, relwidth = self.width, relheight = 1)
			self.after(2, self.animate_forward)
		else:
			self.in_start_pos = False

	def animate_backwards(self):
		if self.pos < self.start_pos:
			self.pos += 0.008
			self.place(relx = self.pos, rely = 0.05, relwidth = self.width, relheight = 1)
			self.after(1, self.animate_backwards)
		else:
			self.in_start_pos = True
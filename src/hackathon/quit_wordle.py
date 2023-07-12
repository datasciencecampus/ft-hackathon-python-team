import tkinter as tk

import customtkinter as ctk

from src.hackathon.utils.quit import quit_game

#Structure:
#- If word guessed
    #- Dialogue box to say so
    #- Option to quit
#-If word not guessed after 5 goes
    #- Dialogue box to say so
    #- Option to try again
    #- Option to quit


# Word guessed, congrats and quit
#If/else for correct guess [TO DO]
root = ctk.CTk()
root.title('Message box test')
#Dialogue box for 'congrats' and quit
#Create a Tkinter frame
frame_w = ctk.CTkFrame(root, height = 80,
                      width = 80,
                      fg_color = 'black')
frame_w.grid()

#Define stuff
# answer = tk.messagebox.askokcancel("","Congratulations, you guessed correctly!")

# #Create a Label
# tk.Label(frame_w, text=answer, font= ('Arial',24)) #.pack() - idk what this does
# # frame.mainloop()

# # Add Button for making selection
button1_w = ctk.CTkButton(frame_w, text="Quit", command = lambda a=root: quit_game(a), fg_color="grey")
button1_w.grid(row=0, column=1)


# # Word not guessed, try again or quit
# #If/else for word not guessed after 6 goes [TO DO]


# #If/else for dialogue box choice (try again/quit)
# # def choice(option):
# #     if option == "Yes"
# #     #code here to loop back to start
    
# #     if option == "No"
# #     quit()
    
# #     else:
# #     quit() #Could do with just this bit and delete lines 45/6?

# #Create a Tkinter frame
# frame_l = ctk.CTkFrame(root, height = 80,
#                      width = 80,
#                      fg_color = 'black')
# #Define stuff
# answer = tk.messagebox.askyesno("Question","Word not guessed, would you like to try again?")
# #Create a Label
# tk.Label(frame_l, text=answer, font= ('Arial',24)) #.pack() - idk what this does
# # frame.mainloop()

# # Add Button for making selection
# button1_l = tk.Button(frame_l, text="Yes",
# command = lambda: choice("Yes"), bg="grey")
# button1_l.grid(row=0, column=1)
# button2_l = tk.Button(frame_l, text="No",
# command = lambda: choice("No"), bg="grey")
# button2_l.grid(row=0, column=2)

#To do:
root.mainloop()
#Some sort of 'if' and/or 'when' thingy that brings up dialogue box
#when NUM_GUESSES reaches 6

#Pop up if word is correct
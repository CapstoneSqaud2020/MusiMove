#UI front end code
import tkinter as tk
import UserInfo 
from tkinter import messagebox
import os
#min size for window
HEIGHT = 500 
WIDTH = 700

#window object w/ window header
root = tk.Tk()
root.minsize(height = HEIGHT, width = WIDTH)
root.title("MusiMove - The music that moves you")


#gonna try to get people to log onto spotify or use playlist from their computer somehow but like 
def musicManager(user_id):
    frame = tk.Frame(root, bg="#C1DDE7", bd=5)
    frame.place(relwidth = .8, relheight = 1, relx = 0, rely = 0)
    tk.Label(frame, text = "music", bg = "#E7CBC1", fg = "#FFFFFF", font=("Helvetica", 20)).place(relwidth = 0.2, relheight = 0.2, relx = .1, rely = .1)


#page user sees once they login/signup
def mainpage(user_id):
    canvas = tk.Canvas(root, bg = "#C1DDE7").place(relwidth = 1, relheight = 1)
 #buttons to different pages to manipulate the settings
    frame = tk.Frame(root, bg="#80c1ff", bd=5)
    frame.place(relwidth = .2, relheight = 1, relx = .8, rely = 0)

    music = tk.Button(frame, text = "music", font = ("Helvetica", 12), command = musicManager(user_id))
    music.place(relwidth=1, relheight = .3, rely = .1 )  

    settings = tk.Button(frame, text = "music", font = ("Helvetica", 12), command = None)
    settings.place(relwidth=1, relheight = .3, rely = .4 )

    logout = tk.Button(frame, text="logout", font=("Helvetica", 12), command=welcome)
    logout.place(relwidth=1, relheight = .3, rely = .7 )   

#logs user in if they are in the system
def comfirmUser(username, password):
    user_id = UserInfo.login(username,password)
    if(username == '' or password == '' or user_id == 0):
        messagebox.showerror("Error", "Invalid Username/Password")
    
    else:
        mainpage(user_id)

#adds new user to system
def newUser(username, password, password1):

    if(username == '' or password == '' or password1 == ''):
        messagebox.showerror("Error", "Invalid Username/Password")

    elif(password != password1):
        messagebox.showerror("Error", "Passwords do not match")
    
    elif(UserInfo.userExists(username)):
         messagebox.showerror("Error", "Username already exists")

    else:
        user_id = UserInfo.addNewUser(username,password)
        mainpage(user_id)

#allows user to enter their username/password to be logged in
def Login():
    canvas = tk.Canvas(root, bg = "#C1DDE7").place(relwidth = 1, relheight = 1)
    
    frame = tk.Frame(root, bg="#80c1ff", bd=5, height = HEIGHT/1.5, width = WIDTH)
    frame.place(relx=0.5, rely=0.2, anchor='n')
    
    tk.Label(frame, text = "Login", bg = "#80c1ff", fg = "#FFFFFF", font=("Helvetica", 35)).place(relwidth = 0.6, relheight = 0.18, relx = .2, rely = .1)
#username entry label & text box
    u_label = tk.Label(frame, text = "username: ", font = ("Helvetica", 12)).place(relwidth=0.2, relheight=.1, relx = .1, rely= .3)
    u_entry = tk.Entry(frame, font=("Helvetica", 12))
    u_entry.place(relwidth=0.6, relheight=.1, relx = .31, rely = .3)
    
#pw entry label & text box
    p_label = tk.Label(frame, text = "password: ", font = ("Helvetica", 12)).place(relwidth=0.2, relheight=.1, relx = .1, rely= .41)
    p_entry = tk.Entry(frame, font=("Helvetica", 12))
    p_entry.config(show="*")
    p_entry.place(relwidth=0.6, relheight=.1, relx = .31, rely = .41)
#button that takes you to function comfirm user to be logged in    
    login = tk.Button(frame, text="continue →", font=("Helvetica", 12), command=lambda: comfirmUser(u_entry.get(), p_entry.get()))
    login.place(relwidth=0.15, relheight = .1, relx =.76, rely = .53 )   

    bck = tk.Button(canvas, text = "back" , font = ("Helvetica", 12, "underline"), command = welcome).place( in_ = frame, relwidth = .1, relheight = .1, relx = 0.1, rely = .9)

#allows user to enter their username/password to be registered
def Register():
    canvas = tk.Canvas(root, bg = "#C1DDE7").place(relwidth = 1, relheight = 1)
    
    frame = tk.Frame(root, bg="#80c1ff", bd=5, height = HEIGHT/1.5, width = WIDTH)
    frame.place(relx=0.5, rely=0.2, anchor='n')

    tk.Label(frame, text = "Register", bg = "#80c1ff", fg = "#FFFFFF", font=("Helvetica", 35)).place(relwidth = 0.6, relheight = 0.18, relx = .2, rely = .1)
#username entry label & text box
    u_label = tk.Label(frame, text = "username: ", font = ("Helvetica", 12)).place(relwidth=0.2, relheight=.1, relx = .1, rely= .3)
    u_entry = tk.Entry(frame, font=("Helvetica", 12))
    u_entry.place(relwidth=0.6, relheight=.1, relx = .31, rely = .3)
#pw entry label & text box
    p_label = tk.Label(frame, text = "password: ", font = ("Helvetica", 12)).place(relwidth=0.2, relheight=.1, relx = .1, rely= .41)
    p_entry = tk.Entry(frame, font=("Helvetica", 12))
#hides pw text as '*'s
    p_entry.config(show="*")
    p_entry.place(relwidth=0.6, relheight=.1, relx = .31, rely = .41)
#comfirm pw entry label & text box
    p_label1 = tk.Label(frame, text = "comfirm password: ", font = ("Helvetica", 12)).place(relwidth=0.2, relheight=.1, relx = .1, rely= .52)
    p_entry1 = tk.Entry(frame, font=("Helvetica", 12))
    p_entry1.config(show="*")
    p_entry1.place(relwidth=0.6, relheight=.1, relx = .31, rely = .52)

    reg = tk.Button(frame, text="continue →", font=("Helvetica", 12), command=lambda: newUser(u_entry.get(), p_entry.get(), p_entry1.get())).place(relwidth=0.15, relheight = .1, relx =.76, rely = .64 )   
   
    bck = tk.Button(canvas, text = "back" , font = ("Helvetica", 12, "underline"), command = welcome).place( in_ = frame, relwidth = .1, relheight = .1, relx = 0.1, rely = .9)
    
#welcome page that starts up when program is first initiated
def welcome(): 

    canvas = tk.Canvas(root, bg = "#C1DDE7").place(relwidth = 1, relheight = 1)
    
    tk.Label(canvas, text = "Welcome", bg = "#E7CBC1", fg = "#FFFFFF", font=("Helvetica", 35)).place(relwidth = 0.6, relheight = 0.2, relx = .2, rely = .3)
#login/register buttons command is the function that they call
    lg = tk.Button(canvas, text = "Login", command = Login).place(relwidth = 0.3, relheight = 0.15, relx = 0.35, rely = .525)
    reg = tk.Button(canvas, text = "Register", command = Register).place(relwidth = 0.3, relheight = 0.15, relx = 0.35, rely = .685)
    root.mainloop()
    
welcome()


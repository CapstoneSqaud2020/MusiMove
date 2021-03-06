#UI front end code
import tkinter as tk
import UserInfo 
import Webcam
import testRadio
import MotionDetection
from tkinter import messagebox
from tkinter import filedialog

import threading
import time
import os
import shutil

import numpy as np


class passiveThread():
    def __init__(self):
        self.__running = True

    def passive(self):
    
        while True:
            if self.__running and testRadio.is_paused:
                id = MotionDetection.motion()
                print(id)
                if testRadio.is_paused and id != -1:
                    if UserInfo.getMusicOpt(id) == "Radio":
                        urls = ["http://stream.revma.ihrhls.com/zc545", "https://stream.revma.ihrhls.com/zc2341"]
                        index = UserInfo.getRadioStation(id)
                        testRadio.setRadio(urls[index])
                        testRadio.play()
                    else:
                        testRadio.playPlaylist()

    def pause_passive(self):
        self.__running = False

    def continue_passive(self):
        self.__running = True


class Applcation:
    #gonna try to get people to log onto spotify or use playlist from their
    #computer somehow but like
    def musicManager(self):
        frame = tk.Frame(self.root, bg="#C1DDE7", bd=5)
        frame.place(relwidth = .8, relheight = 1, relx = 0, rely = 0)
        
        if UserInfo.getMusicOpt(self.user_id) == "Radio":
            tk.Label(frame, text = "Pick a Radio Station:", bg="#C1DDE7", font=("Helvetica", 12)).place(relwidth = .333, relheight = 0.1, relx = .333, rely = .2)
            
            stations = ["ed sheeran iheartradio station","lumineers iheartradio station"]
            urls = ["http://stream.revma.ihrhls.com/zc545", "https://stream.revma.ihrhls.com/zc2341"]

            index = UserInfo.getRadioStation(self.user_id)

            testRadio.setRadio(urls[index])

            dropVar = tk.StringVar()
            dropVar.set(stations[index])
            opts = tk.OptionMenu(frame, dropVar, *stations, command= self.changeRadStation)
            opts.place(relwidth=.333, relheight = .1, rely = .3, relx = .333)

            play = tk.Button(frame, text = "play", command = testRadio.play).place(relwidth = .333, relheight = 0.1, rely = .8, relx = .1665)
            pause =  tk.Button(frame, text = "pause", command = testRadio.stop ).place(relwidth = .333, relheight = 0.1, rely = .8, relx = .5)
            
        else:
            tk.Label(frame, text = "Playlist:", bg="#C1DDE7", font=("Helvetica", 12)).place(relwidth = .333, relheight = 0.1, relx = .333, rely = .2)            
            path = "Music"

            scrollBar_y = tk.Scrollbar(frame)
            scrollBar_x = tk.Scrollbar(frame)
            
            self.musicList = tk.Listbox(frame)
            self.musicList.place(relwidth=.666, relheight = .3, rely = .3, relx = .167)
            self.musicList.insert(tk.END, *[s[:-4] for s in os.listdir(path) if os.path.isfile(os.path.join(path,s))])
            self.musicList.config(yscrollcommand = scrollBar_y.set, xscrollcommand = scrollBar_x.set)

            scrollBar_y.config(command=self.musicList.yview)
            scrollBar_x.config(command=self.musicList.xview)


            addMusic = tk.Button(frame, text = "add", command = self.addSong).place(relwidth = .333, relheight = 0.1, rely = .65, relx = .1665)
            removeMusic = tk.Button(frame, text = "delete", command = self.removeFile).place(relwidth = .333, relheight = 0.1, rely = .65, relx = .5)

            play = tk.Button(frame, text = "play", command = self.playSingleSong).place(relwidth = .333, relheight = 0.1, rely = .8, relx = .1665)
            pause =  tk.Button(frame, text = "pause", command = testRadio.stop ).place(relwidth = .333, relheight = 0.1, rely = .8, relx = .5)
            
            
        tk.Label(frame, text = "music", bg = "#E7CBC1", fg = "#FFFFFF", font=("Helvetica", 20)).place(relwidth = .333, relheight = 0.1)

        #musicMenu = tk.Menu()

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    def changeRadStation(self, value):
        station = {"ed sheeran iheartradio station": {0:0, 1:"http://stream.revma.ihrhls.com/zc545"},"lumineers iheartradio station":{0:1, 1:"https://stream.revma.ihrhls.com/zc2341"}}
        index = station.get(value)[0]
        UserInfo.updateRadioStation(self.user_id, index)
        
        was_paused = testRadio.is_paused
        if not testRadio.is_paused:
            testRadio.stop()

        testRadio.setRadio(station.get(value)[1])
        
        if not was_paused:
            testRadio.play()
    

    def playSingleSong(self):
        i = self.musicList.curselection()
        if i:
            testRadio.stop()
            song = self.musicList.get(i)
            songPath = os.path.join("Music",song+".mp3")
            testRadio.setRadio(songPath)
            testRadio.play()
        else:
            messagebox.showerror("Error", "Please click on song")


    def addSong(self):
        file = filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("MP3 files","*.mp3"),))
        if file:
            shutil.copy(file,"Music")
            self.musicList.insert(tk.END,os.path.basename(file[:-4]))
    
    def removeFile(self):
        i = self.musicList.curselection()
        if i:
            song = self.musicList.get(i)
            os.remove(os.path.join("Music",song+".mp3"))
            self.musicList.delete(i)
        else:
            messagebox.showerror("Error", "Please click on song")


#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

    def settings(self):
        frame = tk.Frame(self.root, bg="#C1DDE7", bd=5)
        frame.place(relwidth = .8, relheight = 1, relx = 0, rely = 0)
        tk.Label(frame, text = "setting", bg = "#E7CBC1", fg = "#FFFFFF", font=("Helvetica", 20)).place(relwidth = .333, relheight = 0.1)

        tk.Label(frame, text = "Stop playing music after:", bg="#C1DDE7", font=("Helvetica", 12)).place(relwidth = .333, relheight = 0.1, rely = .2, relx = .333)
        
        Times = [" 5 mins","10 mins","30 mins","1 hr", "2 hrs", "5 hrs", "10 hrs", "Stay On"]
        dropVar1 = tk.StringVar()
        dropVar1.set(UserInfo.getStopTime(self.user_id))
        opts1 = tk.OptionMenu(frame, dropVar1, *Times, command= self.changeStopTime)
        opts1.place(relwidth=.333, relheight = .1, rely = .325, relx = .333)
        
        tk.Label(frame, text = "Radio or MP3s:", bg="#C1DDE7", font=("Helvetica", 12)).place(relwidth = .333, relheight = 0.1, rely = .45, relx = .333)
        
        musOpts = ["Radio","MP3s"]
        dropVar2 = tk.StringVar()
        dropVar2.set(UserInfo.getMusicOpt(self.user_id))
        opts2 = tk.OptionMenu(frame, dropVar2, *musOpts, command = self.changeMusicOpt)
        opts2.place(relwidth=.333, relheight = .1, rely = .575, relx = .333)

        delete = tk.Button(frame, text="Delete Account", font=("Helvetica", 12), command=self.deleteAccount)
        delete.place(relwidth=.333, relheight = .1, rely = .8, relx = .333)
    
    def changeMusicOpt(self, value):
        UserInfo.updateMusicOpt(self.user_id, value)
        testRadio.pause()

    def changeStopTime(self, value):
        UserInfo.updateStopTime(self.user_id, value)
        
    def deleteAccount(self):
        MsgBox = tk.messagebox.askquestion ('Delete Account','Are you sure you want to delete your account?',icon = 'warning')
        if MsgBox == 'yes':
            UserInfo.deleteUser(self.user_id)
            self.welcome()

    #page user sees once they login/signup
    def mainpage(self):
        tk.Canvas(self.root, bg = "#C1DDE7").place(relwidth = 1, relheight = 1)
        #buttons to different pages to manipulate the settings
        frame = tk.Frame(self.root, bg="#80c1ff", bd=5)
        frame.place(relwidth = .2, relheight = 1, relx = .8, rely = 0)

        music = tk.Button(frame, text = "music", font = ("Helvetica", 12), command = lambda :self.musicManager())
        music.place(relwidth=1, relheight = .33, rely = .003)  

        settings = tk.Button(frame, text = "settings", font = ("Helvetica", 12), command = lambda: self.settings())
        settings.place(relwidth=1, relheight = .33, rely = .336)

        logout = tk.Button(frame, text="logout", font=("Helvetica", 12), command=self.welcome)
        logout.place(relwidth=1, relheight = .33, rely = .669)   

        self.musicManager()

    #logs user in if they are in the system
    def comfirmUser(self,username, password):
        self.user_id = UserInfo.login(username,password)
        if(username == '' or password == '' or self.user_id == 0):
            messagebox.showerror("Error", "Invalid Username/Password")
    
        else:
            self.mainpage()

    #adds new user to system
    def newUser(self,username, password, password1):

        if(username == '' or password == '' or password1 == ''):
            messagebox.showerror("Error", "Invalid Username/Password")

        elif(password != password1):
            messagebox.showerror("Error", "Passwords do not match")
    
        elif(UserInfo.userExists(username)):
            messagebox.showerror("Error", "Username already exists")

        else:
            self.user_id = UserInfo.addNewUser(username,password)
            self.recordVideo()

    #allows user to enter their username/password to be logged in
    def Login(self):
        self.p.pause_passive()
        time.sleep(.5)

        canvas = tk.Canvas(self.root, bg = "#C1DDE7").place(relwidth = 1, relheight = 1)
    
        frame = tk.Frame(self.root, bg="#80c1ff", bd=5, height = self.HEIGHT / 1.5, width = self.WIDTH)
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
        login = tk.Button(frame, text="continue →", font=("Helvetica", 12), command=lambda: self.comfirmUser(u_entry.get(), p_entry.get()))
        login.place(relwidth=0.15, relheight = .1, relx =.76, rely = .53)   

        bck = tk.Button(canvas, text = "back" , font = ("Helvetica", 12, "underline"), command = self.welcome).place(in_ = frame, relwidth = .1, relheight = .1, relx = 0.1, rely = .9)

    #allows user to enter their username/password to be registered
    def Register(self):
        self.p.pause_passive()
        time.sleep(.5)

        canvas = tk.Canvas(self.root, bg = "#C1DDE7").place(relwidth = 1, relheight = 1)
    
        frame = tk.Frame(self.root, bg="#80c1ff", bd=5, height = self.HEIGHT / 1.5, width = self.WIDTH)
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

        reg = tk.Button(frame, text="continue →", font=("Helvetica", 12), command=lambda: self.newUser(u_entry.get(), p_entry.get(), p_entry1.get())).place(relwidth=0.15, relheight = .1, relx =.76, rely = .64)   
   
        bck = tk.Button(canvas, text = "back" , font = ("Helvetica", 12, "underline"), command = self.welcome).place(in_ = frame, relwidth = .1, relheight = .1, relx = 0.1, rely = .9)
    
    #welcome page that starts up when program is first initiated
    def welcome(self): 

        canvas = tk.Canvas(self.root, bg = "#C1DDE7").place(relwidth = 1, relheight = 1)
    
        tk.Label(canvas, text = "Welcome", bg = "#E7CBC1", fg = "#FFFFFF", font=("Helvetica", 35)).place(relwidth = 0.6, relheight = 0.2, relx = .2, rely = .3)
        #login/register buttons command is the function that they call
        lg = tk.Button(canvas, text = "Login", command = self.Login).place(relwidth = 0.3, relheight = 0.15, relx = 0.35, rely = .525)
        reg = tk.Button(canvas, text = "Register", command = self.Register).place(relwidth = 0.3, relheight = 0.15, relx = 0.35, rely = .685)  
        
        self.p.continue_passive()

    def recordVideo(self):
        canvas = tk.Canvas(self.root, bg = "#C1DDE7")
        canvas.place(relwidth = 1, relheight = 1)
    
        self.stopEvent = None
        self.thread = None
        self.frame = None
        self.cap = None
        self.out = None
        self.rec = None

        self.rec = tk.Button(canvas, text = "Record", command = lambda: self.saveVideoProc())
        self.rec.place(relwidth = 0.15, relheight = 0.1, relx = 0.425, rely = .85)

        self.panel = tk.Label(canvas, bg="#80c1ff")
        self.panel.place(relwidth = .6, relheight = .6,relx = .2, rely = .2)
        time.sleep(1)
        Webcam.startVideoProc(self)  

    def saveVideoProc(self):
        self.rec.configure(text= "Continue ->")
        self.rec.config(command = lambda: self.next())
        Webcam.saveVideo(self)

    def next(self):
        self.mainpage()
        Webcam.stopVideoProc(self)


    def __init__(self):
        #min size for window
        self.HEIGHT = 600 
        self.WIDTH = 1000

        #window object w/ window header
        self.user_id = None
        #self.user_id = 10000009
        self.root = tk.Tk()
        self.root.minsize(height = self.HEIGHT, width = self.WIDTH)
        self.root.title("MusiMove - The music that moves you")
        
        
        self.p = passiveThread()
        self.passiveThread = threading.Thread(target = self.p.passive)
        self.passiveThread.start()
        
        self.welcome()
        #self.mainpage()
        #self.root.after(0,self.)
        self.root.mainloop()




ap = Applcation()

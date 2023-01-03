import wave
import sys
import matplotlib.pyplot as plt
import pydub
import tkinter as tk
import simpleaudio as sa
from tkinter import *
import numpy as npp
import tkinter as tk

# declare the window
window = tk.Tk()
# set window title
n=-75
n2 = 50
window.title("Audio Processing Singnals")
# set window width and height
window.configure(width=480, height=380)
# set window background image
img =PhotoImage(file='wa.png')
laa = Label(window,image= img)
laa.place(x=-5,y=-5)
window.resizable(0,0)
#====================
o = 120
entryshift = tk.Entry(window)
entryshift.place(x=150+o , y = 165+n)
w =Label(window,text= "Shifting",fg= "white",bg="#4b86c2",padx=43)
w.configure(font=("",15,""))
w.place(x = 50 , y = 160+n)
#=====================
h=50
g = 50
li3 = Label(window,text= "Reverse",fg= "white",bg="#4b86c2",padx=40)
li3.configure(font=("",15,""))
li3.place(x =n2,y = 160+n+h+53+g)
#Radio buttons
ee = StringVar()
rad1 = tk.Radiobutton(window,text="ON",font=("",15,""),variable= ee,value='on',bg="green",padx=4)
rad1.place(x=150+o,y=160+n+h+g+50)
rad2 = tk.Radiobutton(window,text="OFF",font=("",15,""),variable= ee ,value='off',bg = "red",padx=4)
rad1.place(x=130+o,y=160+n+h+g+50)
rad2.place(x=195+o+30,y=160+n+g+h+50)
#==========================
entrysc = tk.Entry(window)
entrysc.place(x=150+o , y = 165+n+h+25)
scl =Label(window,text= "Time Scaling",fg= "white",bg="#4b86c2",padx=20)
scl.configure(font=("",15,""))
scl.place(x = 50 , y = 160+n+h+25)
#orignal wave function
def orignal():
   #open the wave
    global wav
    wav = wave.open("ftest.wav","rb")
    global sampleRate
    sampleRate= wav.getframerate()
    #check if mono or not
    if wav.getnchannels()==2:
        print("Stereo Files are not supported. Please Use Mono Files")
        sys.exit(0)
    #amplitued
    global raw
    raw = wav.readframes(-1)
    raw = npp.frombuffer(raw,dtype="int16")
    #shifting
    Time= npp.linspace(0,len(raw)/sampleRate,num=len(raw))
    #ploting
    plt.title("Waveform")
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.plot(Time,raw,color="purple")
    plt.show()
    #playing sound
    filename = 'ftest.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj  = wave_obj.play()
    play_obj.wait_done()
#orignal wave button
r = Button(window,text = "Orginal Wave",font=("",18,""),command=orignal,bg= "white",fg= "black" )
r.place(x = 50 , y =  160+n+h+50+g+75)
#modified wave function
def mode():
    #Entering the value of shifting and speed
    if entryshift.get() == '' :
        sh=0
    else:
        sh=float(entryshift.get())
    if entrysc.get() == '' :
        spd=1
    else:
        spd=float(entrysc.get())
    #speed
    nwav = pydub.AudioSegment.from_file(file="ftest.wav",format="wav")
    nwav = nwav._spawn(nwav.raw_data, overrides={"frame_rate" : float(nwav.frame_rate*spd)})
    nwav.export(out_f='Aftertest.wav', format='wav')
    global wav
    #shifting
    wav = pydub.AudioSegment.from_file(file="Aftertest.wav",format="wav")
    pydub.AudioSegment.converter = "ffmpeg.exe"
    pydub.AudioSegment.ffmpeg = "ffmpeg.exe"
    pydub.AudioSegment.ffprobe = "ffprobe.exe"
    if sh>0:
        sSec = sh
        eSec = 2.5
        sTime = sSec * 1000
        eTime = eSec * 1000
        wav = wav[sTime : eTime]
    else:
        shift=pydub.AudioSegment.silent(duration=-sh*1000)
        wav=shift+wav
    wav.export('Aftertest.wav', format='wav')

    wav = wave.open("Aftertest.wav","rb")
    global sampleRate
    sampleRate= wav.getframerate()
    global raw
    raw = wav.readframes(-1)
    raw = npp.frombuffer(raw,dtype="int16")
    Time= npp.linspace(0,len(raw)/sampleRate,num=len(raw))
    #reverse
    if ee.get() == 'on' :
        raw = raw[:: -1]
        wav = pydub.AudioSegment.from_file(file="aftertest.wav",format="wav")
        wav=wav.reverse()
        wav.export(out_f='aftertest.wav', format='wav')
    #ploting the wave after reverse
    plt.title("Waveform")
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.plot(Time,raw,color="purple")
    plt.show()
    #playing sound
    filename = 'aftertest.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj  = wave_obj.play()
    play_obj.wait_done()
#modified wave button
r = Button(window,text = "Modified Wave",font=("",18,""),command=mode,bg= "white",fg= "black" )
r.place(x = 250 , y =  160+n+h+50+g+75)
window.mainloop()
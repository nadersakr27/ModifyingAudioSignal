import wave
import numpy as np
import sys
import matplotlib.pyplot as plt
import pydub
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from hashlib import blake2b
from asyncio.windows_events import NULL
from cgitb import text
import simpleaudio as sa

#plot wave
def plot(t,r):
    plt.title("Waveform")
    plt.ylabel("Amplitude")
    plt.xlabel("Time")
    plt.plot(t,r,color="purple")
    plt.show()

#input audio wave
def B_open():
    wav = wave.open("ftest.wav","rb")
    #check if mono or not
    if wav.getnchannels()==2:
        print("Stereo Files are not supported. Please Use Mono Files")
        sys.exit(0)
    #convert wave audio to bytes
    amp = wav.readframes(-1)
    amp = np.frombuffer(amp,dtype="int16")
    sampleRate= wav.getframerate()
    Time= np.linspace(0,len(amp)/sampleRate,num=len(amp))
    plot(Time,amp)

#output audio wave
def A_open():
    wav = wave.open("aftertest.wav","rb")
    #check if mono or not
    if wav.getnchannels()==2:
        print("Stereo Files are not supported. Please Use Mono Files")
        sys.exit(0)
    #convert wave audio to bytes
    amp = wav.readframes(-1)
    amp = np.frombuffer(amp,dtype="int16")
    sampleRate= wav.getframerate()
    ti = len(amp)/sampleRate
    Time= np.linspace(0,ti,num=len(amp))
    plot(Time,amp)
#reverse
def reverse():
    wav = pydub.AudioSegment.from_file(file="ftest.wav",format="wav")
    wav=wav.reverse()
    wav.export(out_f='aftertest.wav', format='wav')
    A_open()

#shifting
def shift():
    sh=float (input())
    wav = pydub.AudioSegment.from_file(file="ftest.wav",format="wav")
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
    A_open()

#Speed
def speed():
    spd=float (input())
    nwav = pydub.AudioSegment.from_file(file="ftest.wav",format="wav")
    nwav = nwav._spawn(nwav.raw_data,
                       overrides={"frame_rate" : float(nwav.frame_rate*spd)})
    nwav.export(out_f='Aftertest.wav', format='wav')

#play sound
def bplay():
    filename = 'ftest.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj  = wave_obj.play()
    play_obj.wait_done()
def Aplay():
    filename = 'aftertest.wav'
    wave_obj = sa.WaveObject.from_wave_file(filename)
    play_obj  = wave_obj.play()
    play_obj.wait_done()
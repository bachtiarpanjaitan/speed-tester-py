#!/usr/bin/python
import RPi.GPIO as GPIO
from picamera import PiCamera
import tkinter
import time
from PIL import ImageTk, Image
from threading import Thread
import io
import sys
import threading
import os
import datetime

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
camera = PiCamera()

try:
    import tkinter as tk  # for python 3
    from tkinter import messagebox
except:
    import Tkinter as tk  # for python 2
    from tkinter import messagebox
import pygubu
class Application (pygubu.TkApplication,Thread):
    def __init__(self, master):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()
        self.button_state = 0
        self.sensora = 16
        self.sensorb = 18
        self.jarak = 5 #dalam satuan meter
        self.sensor_state = 0
        self.count_start = 0
        self.timer = 0 
        self.kecepatan =0
        self.limit = 40 #ini untuk limit kecepetan
        self.path = '/home/pi/share/SpeedTesterPy/Images/'
        
        
        #2: Load an ui file
        builder.add_from_file('main-ui.ui')

        #3: Create the widget using a master as parent
        self.mainwindow = builder.get_object('mainwindow', master)
        
        builder.connect_callbacks(self)
        
        callbacks = {
            'start_sensor': self.start_sensor
            }
        button_state = 1
        builder.connect_callbacks(callbacks)
         #self.threadsensor.start()
        self.textvalue = self.builder.get_object("speed_value")
        self.imagebox = self.builder.get_object("picture_box")
    
    def start_sensor(self):
        
        if self.button_state == 0:
            self.button_state = 1
            btn = self.builder.get_object("btn_start")
            btn.config(text="START")
        elif self.button_state == 1:
            #self.threadsensor.join()
            btn = self.builder.get_object("btn_start")
            btn.config(text="STOP")
            self.threadsensor = threading.Thread(name='backgroundsensor', target=get_sersor_value,args=(self.button_state,self,)).start()
            self.button_state = 0
def get_sersor_value(btn,self):
    #print(self.button_state)
    hasused = False
    try:
        while True:
            #print(self.button_state)
            valuea = rc_time(self.sensora)
            valueb = rc_time(self.sensorb)
            print("A : %s B: %s T: %i" %(valuea, valueb,self.count_start))
            textvalue = self.builder.get_object("speed_value")
            #.config(text="TEST")
            if hasused is True:
                if valuea == 0 and valueb == 1 and self.sensor_state == 0:
                    self.count_start = self.timer
                    self.sensor_state = 1
                elif valuea == 1 and valueb == 0 and self.sensor_state == 1:
                    textvalue.config(text=count_speed(self))
                    self.timer = 0
                    self.count_start = 0
                    self.sensor_state = 0
                    hasused = False
            else :
                if valuea == 1 and valueb == 0 and self.sensor_state == 0:
                    self.count_start = self.timer
                    self.sensor_state = 1
                elif valuea == 0 and valueb == 1 and self.sensor_state == 1:
                    textvalue.config(text=count_speed(self))
                    self.timer = 0
                    self.count_start = 0
                    self.sensor_state = 0
                    hasused = True
                
                
            self.timer += 1          
    except KeyboardInterupt:
        pass
    finally:
        #if self.button_state == 0:
        GPIO.cleanup()

def clearcv(self):
     self.imagebox.destroy()

def startcamera(self):
    camera.start_preview()
    #time.sleep(1)
    tmstamp = datetime.datetime.now().timestamp()
    img = self.path + str(tmstamp) + '.jpg'
    camera.capture(img)
    camera.stop_preview()
    #time.sleep(1)
    gambar = ImageTk.PhotoImage(Image.open(img))
    #item = self.imagebox.create_image(2,2, image=gambar)
    self.imagebox = self.builder.get_object("picture_box")
    self.imagebox.photo = gambar
    imgArea = self.imagebox.create_image(3,3,image = gambar)
    self.imagebox.itemconfig(imgArea, image = gambar)
    #self.imagebox.lower(item)
        
def count_speed(self):
    km_range = self.jarak / 1000
    jam = (self.timer - self.count_start) / 3600000
    kecepatan = km_range / jam
    if kecepatan > self.limit:
        startcamera(self)
    return ("%.2f" % kecepatan)

def rc_time(a):
        GPIO.setup(a, GPIO.IN)
        for i in range(0,1):   
            return GPIO.input(a)
      
if __name__ == '__main__':
    root = tk.Tk(className="speed tester")
    app = Application(root)
    root.mainloop()
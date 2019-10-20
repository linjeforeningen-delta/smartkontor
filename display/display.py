from tkinter import Tk, Label, W, Canvas
from datetime import datetime
from six.moves import urllib
import math

from bussapi import getBuses
from cantinahours import getCantinaHours
import serial


GLOSHAUGEN_STOP = 'NSR:StopPlace:44085'
PROF_BROCHS_STOP = 'NSR:StopPlace:41620'
NUMBER_OF_CALLS = 10

FONTSIZE_CONSTANT = 42

BACKGROUND_COLOR = 'white'

try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0, writeTimeout=0)
except:
    print("No serial port connected")

class DeltaWall:
    def __init__(self, master):
        
        master.configure(background=BACKGROUND_COLOR)
        master.columnconfigure(0, weight=10)
        master.columnconfigure(1, weight=2)
        master.columnconfigure(2, weight=8)
        master.columnconfigure(3, weight=2)
        master.columnconfigure(4, weight=2)
        self.master = master
        
        screen_width = master.winfo_screenwidth()
        #screen_height = master.winfo_screenheight()
        
        busfontSize = math.floor(screen_width/FONTSIZE_CONSTANT)
        
        busfont = ("Lucidia Console", busfontSize)
        clockfont = ("DejaVuSansMono", 40)
        
        self.delta_logo = Canvas(master, width=260, height=150, bg=BACKGROUND_COLOR, highlightthickness=0)
        self.delta_logo.grid(row=0, column=0, rowspan=2, sticky=W)
        self.delta_logo.create_polygon(10,140, 250,140, 130,10, 65,75, 105,75,
                                       130,50, 190,115, 35,115, fill='green')
        
        
        self.clock = Label(master, text="00:00", font=clockfont, bg=BACKGROUND_COLOR)
        self.clock.grid(row=0, column=4)
        
        self.cantina_hours = Label(master, text="cantina_hours", font=busfont, bg=BACKGROUND_COLOR)
        self.cantina_hours.grid(row=2, column=0, rowspan=4)

        self.coffe_button = Label(master, text="Coffee made:\n No coffee made", font=busfont, bg=BACKGROUND_COLOR)
        self.coffe_button.grid(row=7, column=0, rowspan=3)
        
        self.glos_label = Label(master, text="Gløshaugen:", font=busfont, bg=BACKGROUND_COLOR)
        self.glos_label.grid(row=1, column=2)
        
        self.glos_estimated_calls = []
        for i in range(NUMBER_OF_CALLS):
            individual_call_line = Label(master, text="000", font=busfont, bg=BACKGROUND_COLOR)
            individual_call_dest = Label(master, text="dest_placeholder", font=busfont, bg=BACKGROUND_COLOR, anchor=W)
            individual_call_time = Label(master, text="00:00", font=busfont, bg=BACKGROUND_COLOR)
            individual_call_line.grid(row=2+i, column=1)
            individual_call_dest.grid(row=2+i, column=2, sticky=W)
            individual_call_time.grid(row=2+i, column=3, columnspan=2)
            self.glos_estimated_calls.append(individual_call_line)
            self.glos_estimated_calls.append(individual_call_dest)
            self.glos_estimated_calls.append(individual_call_time)

        
    def showTime(self):
        current_time = datetime.now()
        text = current_time.isoformat()[11:16]
        if (current_time.second % 2) == 0:
            text = text[:2] + " " + text[3:]
        
        if (self.clock['text'] != text):
            self.clock['text'] = text
        
    def updateBuses(self):
        g_lines, g_destinations, g_times = getBuses(GLOSHAUGEN_STOP, NUMBER_OF_CALLS)
        b_lines, b_destinations, b_times = getBuses(PROF_BROCHS_STOP, NUMBER_OF_CALLS)
        
        
        for i in range(NUMBER_OF_CALLS):
            self.glos_estimated_calls[i*3]['text'] = g_lines[i]
            self.glos_estimated_calls[i*3 + 1]['text'] = g_destinations[i]
            display_time = self.busTimesToString(g_times[i])
            self.glos_estimated_calls[i*3 + 2]['text'] = display_time

    def busTimesToString(self,bus_time): #misleading name, as bus times are already a string
        return_str = bus_time
        bus_hour = int(bus_time[:2])
        bus_minute = int(bus_time[3:])
        now = datetime.now()
        now_hour = now.hour
        now_minute = now.minute
        if now_hour > bus_hour: 
            bus_hour = bus_hour + 24 #Set bus hour to properly be tomorrow
        time_left = (bus_hour - now_hour)*60 + (bus_minute - now_minute)
        if time_left == 0:
            return_str = "Nå"
        elif time_left <= 9:
            return_str = str(time_left) + " min"
        return return_str

    def readArduino(self):
        while(True):
            c = ser.read().decode('ASCII')
            c.encode('utf-8')
            if len(c) == 0:
                break

            if c == '\r':
                c == ''

            if c == 'C':

                self.coffe_button['text'] = "Coffee made:\n" + datetime.now().isoformat()[11:16]
        root.after(10, self.readArduino)
    
        
    def periodicUpdateClock(self):
        try:
            self.showTime()
        finally:
            self.clock.after(200, self.periodicUpdateClock) #After 200ms, this function calls itself
        
            
    def updateCantinaHours(self):
        realfag_hours, hangaren_hours = getCantinaHours()
        self.cantina_hours['text'] = "Kantinetider: \n Realfag: " + realfag_hours + " \n Hangaren: " + hangaren_hours
        
    def periodicUpdateHourly(self): #Include everything that should be updated hourly in this function
        try:
            self.updateCantinaHours()
        finally:
            self.cantina_hours.after(3600000, self.periodicUpdateHourly)
        
    def periodicUpdate20s(self):
        try:
            self.updateBuses()
        finally:
            self.glos_estimated_calls[0].after(20000, self.periodicUpdate20s)

root = Tk()
root.attributes("-fullscreen", True)
deltaWall = DeltaWall(root)
try:
    deltaWall.periodicUpdateHourly()
except urllib.error.URLError as networkerror:
    print(networkerror)
except:
    print("Unknown error")
try:
    deltaWall.periodicUpdateClock()
    deltaWall.periodicUpdate20s()
except urllib.error.URLError as networkerror:
    print(networkerror)
except:
    print("Unknown error")

try:
    root.after(100, deltaWall.readArduino)
except:
    print("Couldn't read Arduino")

root.mainloop()
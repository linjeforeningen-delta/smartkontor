from tkinter import Tk, Label, Button
import time

from bussapi import getBuses
from cantinahours import getCantinaHours


GLOSHAUGEN_STOP = 'NSR:StopPlace:44085'
PROF_BROCHS_STOP = 'NSR:StopPlace:41620'
NUMBER_OF_CALLS = 10

BACKGROUND_COLOR = 'white'

class DeltaWall:
    def __init__(self, master):
        
        master.configure(background=BACKGROUND_COLOR)
        master.columnconfigure(0, weight=5)
        master.columnconfigure(1, weight=1)
        master.columnconfigure(2, weight=3)
        master.columnconfigure(3, weight=1)
        self.master = master
        
        busfont = ("Lucidia Console", 40)
        
        
        self.clock = Label(master, text="00:00", font=busfont, bg=BACKGROUND_COLOR)
        self.clock.grid(row=0, column=4)
        
        self.cantina_hours = Label(master, text="cantina_hours_string", font=busfont, bg=BACKGROUND_COLOR)
        self.cantina_hours.grid(row=2, column=0, rowspan=4, sticky='w')
        
        self.glos_label = Label(master, text="Gløshaugen:", font=busfont, bg=BACKGROUND_COLOR)
        self.glos_label.grid(row=1, column=1)
        
        self.glos_estimated_calls = []
        for i in range(NUMBER_OF_CALLS):
            individual_call_line = Label(master, text="Bus placeholder", font=busfont, bg=BACKGROUND_COLOR)
            individual_call_dest = Label(master, text="Bus placeholder", font=busfont, bg=BACKGROUND_COLOR)
            individual_call_time = Label(master, text="Bus placeholder", font=busfont, bg=BACKGROUND_COLOR)
            individual_call_line.grid(row=2+i, column=1)
            individual_call_dest.grid(row=2+i, column=2)
            individual_call_time.grid(row=2+i, column=3)
            self.glos_estimated_calls.append(individual_call_line)
            self.glos_estimated_calls.append(individual_call_dest)
            self.glos_estimated_calls.append(individual_call_time)

#        self.close_button = Button(master, text="Close", command=master.quit)
#        self.close_button.pack()
        
    def showTime(self):
        time = ""#QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + " " + text[3:]
        
        self.clock.setText(text)
        
    def updateBuses(self):
        g_lines, g_destinations, g_times = getBuses(GLOSHAUGEN_STOP, NUMBER_OF_CALLS)
        b_lines, b_destinations, b_times = getBuses(PROF_BROCHS_STOP, NUMBER_OF_CALLS)
        
        
        for i in range(NUMBER_OF_CALLS):
            self.glos_estimated_calls[i*3]['text'] = g_lines[i]
            self.glos_estimated_calls[i*3 + 1]['text'] = g_destinations[i]
            self.glos_estimated_calls[i*3 + 2]['text'] = g_times[i]
#            
#        for i in range(NUMBER_OF_CALLS):
#            item_line = QTableWidgetItem(b_lines[i])
#            item_line.setTextAlignment(Qt.AlignCenter)
#            self.brochs_bus_table.setItem(i,0,item_line)
#            item_dest = QTableWidgetItem(b_destinations[i])
#            self.brochs_bus_table.setItem(i,1,item_dest)
#            item_time = QTableWidgetItem(b_times[i])
#            self.brochs_bus_table.setItem(i,2,item_time)
        
    def updateClock(self):
        self.showTime()
        self.clock.after(200, self.updateClock)
        
            
    def updateCantinaHours(self):
        realfag_hours, hangaren_hours = getCantinaHours()
        self.cantina_hours['text'] = "Kantinetider: \n Realfag: " + realfag_hours + " \n Hangaren: " + hangaren_hours
        
    def updateHourly(self): #Include everything that should be updated hourly in this function
        self.updateCantinaHours()
        self.cantina_hours.after(3600000, self.updateHourly)
        
    def update20s(self):
        self.updateBuses()
        self.glos_estimated_calls[0].after(20000, self.update20s)

root = Tk()
root.attributes("-fullscreen", True)
deltaWall = DeltaWall(root)
deltaWall.update20s()
deltaWall.updateHourly()
root.mainloop()
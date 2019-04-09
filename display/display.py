from tkinter import Tk, Label, Button
import time

from bussapi import getBuses
from cantinahours import getCantinaHours


GLOSHAUGEN_STOP = 'NSR:StopPlace:44085'
PROF_BROCHS_STOP = 'NSR:StopPlace:41620'
NUMBER_OF_CALLS = 10

class DeltaWall:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")
        
        self.clock = Label(master, text="00:00")
        
        self.cantina_hours = Label(master, text="cantina_hours_string")
        self.cantina_hours.grid(row=1, column=0)
        
        self.glos_label = Label(master, text="Gløshaugen:")
        self.glos_label.grid(row=1, column=1)
        
        self.glos_estimated_calls = []
        for i in range(NUMBER_OF_CALLS):
            individual_call = Label(master, text="Bus placeholder")
            individual_call.grid(row=2+i, column=1)
            self.glos_estimated_calls.append(individual_call)

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
        print("Bus data fetched.")
        
        
        for i in range(NUMBER_OF_CALLS):
            self.glos_estimated_calls[i]['text'] = g_times[i] + " " + g_lines[i] + " " + g_destinations[i]
#            
#        for i in range(NUMBER_OF_CALLS):
#            item_line = QTableWidgetItem(b_lines[i])
#            item_line.setTextAlignment(Qt.AlignCenter)
#            self.brochs_bus_table.setItem(i,0,item_line)
#            item_dest = QTableWidgetItem(b_destinations[i])
#            self.brochs_bus_table.setItem(i,1,item_dest)
#            item_time = QTableWidgetItem(b_times[i])
#            self.brochs_bus_table.setItem(i,2,item_time)
        
#    def updateClock(self):
        
            
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
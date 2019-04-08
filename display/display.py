from tkinter import Tk, Label, Button

from bussapi import getBuses
from cantinahours import getCantinaHours


GLOSHAUGEN_STOP = 'NSR:StopPlace:44085'
PROF_BROCHS_STOP = 'NSR:StopPlace:41620'
NUMBER_OF_CALLS = 10

class DeltaWall:
    def __init__(self, master):
        self.master = master
        master.title("A simple GUI")
        
        self.cantina_hours = Label(master, text="cantina_hours_string")
        self.cantina_hours.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()
        
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
        
        
#        for i in range(NUMBER_OF_CALLS):
#            item_line = QTableWidgetItem(g_lines[i])
#            item_line.setTextAlignment(Qt.AlignCenter)
#            self.glos_bus_table.setItem(i,0,item_line)
#            item_dest = QTableWidgetItem(g_destinations[i])
#            self.glos_bus_table.setItem(i,1,item_dest)
#            item_time = QTableWidgetItem(g_times[i])
#            self.glos_bus_table.setItem(i,2,item_time)
#            
#        for i in range(NUMBER_OF_CALLS):
#            item_line = QTableWidgetItem(b_lines[i])
#            item_line.setTextAlignment(Qt.AlignCenter)
#            self.brochs_bus_table.setItem(i,0,item_line)
#            item_dest = QTableWidgetItem(b_destinations[i])
#            self.brochs_bus_table.setItem(i,1,item_dest)
#            item_time = QTableWidgetItem(b_times[i])
#            self.brochs_bus_table.setItem(i,2,item_time)
            
    def updateCantinaHours(self):
        realfag_hours, hangaren_hours = getCantinaHours()
        self.cantina_hours['text'] = "Kantinetider: \n Realfag: " + realfag_hours + " \n Hangaren: " + hangaren_hours
        
    def updateHourly(self): #Include everything that should be updated hourly in this function
        self.updateCantinaHours()
        self.cantina_hours.after(3600000, self.updateHourly)

root = Tk()
root.attributes("-fullscreen", True)
deltaWall = DeltaWall(root)
deltaWall.updateHourly()
root.mainloop()
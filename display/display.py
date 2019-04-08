import sys
import random
from bussapi import getBuses
import cantinahours
from PySide2.QtWidgets import (QApplication, QLabel, QPushButton,
                               QVBoxLayout, QWidget, QHBoxLayout,
                               QGridLayout, QTableWidget, QTableWidgetItem,
                               QHeaderView)
from PySide2.QtCore import Slot, Qt, QUrl, QTimer, QTime
from PySide2.QtGui import QStandardItemModel

GLOSHAUGEN_STOP = 'NSR:StopPlace:44085'
PROF_BROCHS_STOP = 'NSR:StopPlace:41620'
NUMBER_OF_CALLS = 10

class MyWidget(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        
        
        self.clock = QLabel("00:00")
        
        self.timer_clock = QTimer()
        self.timer_clock.timeout.connect(self.showTime)
        self.timer_clock.start(1000)
        
        
        self.cantina_hours = QLabel("Kantinetider: \n Realfag: na \n Hangaren: na")
        
        self.timer_cantina = QTimer()
        self.timer_cantina.timeout.connect(self.updateCantinaHours)
        self.timer_cantina.start(20000)
        
        
        self.glos_bus_table = QTableWidget()
        self.glos_bus_table.setRowCount(NUMBER_OF_CALLS)
        self.glos_bus_table.setColumnCount(3)
        self.glos_bus_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.glos_bus_table.horizontalHeader().hide()
        self.glos_bus_table.verticalHeader().hide()
        
        self.brochs_bus_table = QTableWidget()
        self.brochs_bus_table.setRowCount(NUMBER_OF_CALLS)
        self.brochs_bus_table.setColumnCount(3)
        self.brochs_bus_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.brochs_bus_table.horizontalHeader().hide()
        self.brochs_bus_table.verticalHeader().hide()
        
        
        self.timer_buses = QTimer()
        self.timer_buses.timeout.connect(self.updateBuses)
        self.timer_buses.start(10000)
        
        
        
        #self.clock.setAlignment(Qt.AlignTop)
        self.cantina_hours.setAlignment(Qt.AlignLeft)
        self.clock.setAlignment(Qt.AlignLeft)

        self.layout = QGridLayout()
        self.layout.setColumnStretch(0, 4)
        self.layout.setColumnStretch(1, 4)
        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 9)
        self.layout.setRowStretch(2, 9)
        self.layout.setRowStretch(3, 1)
        self.layout.addWidget(self.clock,0,0)
        self.layout.addWidget(self.cantina_hours,2,0)

        self.layout.addWidget(self.glos_bus_table,1,1)
        self.layout.addWidget(self.brochs_bus_table,2,1)
        
        
        self.setLayout(self.layout)
        
        self.setStyleSheet("background-color:white;")
        self.clock.setStyleSheet("font: 48pt \"Lucida Console\";")
        self.cantina_hours.setStyleSheet("font: 36pt \"Lucida Console\";")
        self.glos_bus_table.setStyleSheet("border: none;"
                                          "font: 22pt;")
        self.brochs_bus_table.setStyleSheet("border: none;"
                                            "font: 22pt;")

        
    @Slot()
    def showTime(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        if (time.second() % 2) == 0:
            text = text[:2] + " " + text[3:]
        
        self.clock.setText(text)
        
    @Slot()
    def updateBuses(self):
        g_lines, g_destinations, g_times = getBuses(GLOSHAUGEN_STOP, NUMBER_OF_CALLS)
        b_lines, b_destinations, b_times = getBuses(PROF_BROCHS_STOP, NUMBER_OF_CALLS)
        print("Bus data fetched.")
        
        
        for i in range(NUMBER_OF_CALLS):
            item_line = QTableWidgetItem(g_lines[i])
            item_line.setTextAlignment(Qt.AlignCenter)
            self.glos_bus_table.setItem(i,0,item_line)
            item_dest = QTableWidgetItem(g_destinations[i])
            self.glos_bus_table.setItem(i,1,item_dest)
            item_time = QTableWidgetItem(g_times[i])
            self.glos_bus_table.setItem(i,2,item_time)
            
        for i in range(NUMBER_OF_CALLS):
            item_line = QTableWidgetItem(b_lines[i])
            item_line.setTextAlignment(Qt.AlignCenter)
            self.brochs_bus_table.setItem(i,0,item_line)
            item_dest = QTableWidgetItem(b_destinations[i])
            self.brochs_bus_table.setItem(i,1,item_dest)
            item_time = QTableWidgetItem(b_times[i])
            self.brochs_bus_table.setItem(i,2,item_time)
            
    @Slot()
    def updateCantinaHours(self):
        realfag_hours, hangaren_hours = cantinahours.getOpeningHours()
        self.cantina_hours.setText("Kantinetider: \n Realfag: " 
                                   + realfag_hours 
                                   + " \n Hangaren: "
                                   + hangaren_hours)
        
        

if __name__ == "__main__":
    app = QApplication(sys.argv)

    widget = MyWidget()
    widget.resize(800, 600)
    widget.showFullScreen()

    sys.exit(app.exec_())
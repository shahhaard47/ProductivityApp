"""
Simple GUI Python app to help keep track of what you work on and how long
Application can be exited at the end of the day to save to csv file

Created by: Haard Shah
"""

from tkinter import *
from tkinter import messagebox
from datetime import datetime as dt
from datetime import timedelta
from datetime import date
import csv
import os

# Constants
START = "Start"
STOP = "Stop"

class Track(object):
    def __init__(self):
        self.application = Tk()
        # configure window
        self.application.title('Productivity Tracker')
        self.application.geometry('800x600')
        self.application.protocol('WM_DELETE_WINDOW', self.appCloseHandler)
        # ADD Widgets
        # self.button = Button(self.application, text=START, width=20, command=self.buttonCallback)
        self.tasks = [] # each element will be dictionary
        self.btns = []

        self.taskEntry = Entry(self.application, width=30)
        self.taskEntry.grid(row=0, column=0)
        addButton = Button(self.application, text="Add Task", command=self.addTask, anchor="w") # TODO: pass in entry as argument
        addButton.grid(row=0, column=1)

        self.taskFrame = Frame(self.application)
        self.taskFrame.grid(row=2)

        # state vars
        self.WORKING = False
        self.currentTask = None # assigned to index
        self.startTime = None # datetime
        self.totalTasks = 0

        self.initializePrevious()

        # DONE adding widgets
        self.application.mainloop()

    def strToTimedelta(self, strTime):
        days = 0
        hours = 0
        minutes = 0
        seconds = 0
        micros = 0
        if ',' in strTime:
            pass # should not work on something for days at once!
        else:
            t = strTime.split(':')
            hours = int(t[0])
            minutes = int(t[1])
            last = t[2]
            if '.' in last:
                last = last.split('.')
                seconds = int(last[0])
                micros = int(last[1])
            else:
                seconds = int(last)
        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=micros)

    def initializePrevious(self):
        '''Initialize previous tasks from today if they exist'''
        dayFile = str(date.today())+'.csv'
        if not os.path.exists(dayFile): return
        # file exists
        with open(dayFile) as f:
            reader = csv.reader(f, delimiter=',')
            first = True
            rows = [r for r in reader]
            for i, row in enumerate(rows):
                if not first: 
                    if i is not 0:
                        if row[1] != rows[i-1][1]:
                            self.addTask(taskText=row[1], totalTime=self.strToTimedelta(row[2]))
                else:
                    first = False


    def addTask(self, taskText=None, totalTime=None, timeStamps=None):
        # do nothing if taskEntry box is empty
        if taskText is None and not self.taskEntry.get():
            return
        # task
        taskText = self.taskEntry.get() if taskText is None else taskText
        task = Label(self.taskFrame, text=taskText, justify='left', anchor='w', width=40)
        task.grid(row=self.totalTasks, column=0)
        self.taskEntry.delete(0, "end")
        # start stop button
        b = self.createButton()
        b.grid(row=self.totalTasks, column=1)
        # total time label
        totalTime = timedelta() if totalTime is None else totalTime
        totTime = Label(self.taskFrame, text=str(totalTime), justify='right', width=20)
        totTime.grid(row=self.totalTasks, column=2)
        # add to tasks lst
        self.tasks.append({
            "task" : task['text'],
            "button" : b,
            "totalTime" : totalTime,
            "totalLabel" : totTime,
            "timeStamps" : [] if timeStamps is None else timeStamps
        })
        self.totalTasks += 1


    def createButton(self):
        button = Button(self.taskFrame, text=START, width=20)
        button.bind("<Button-1>", self.buttonCallback)
        # button.pack()
        return button

    def disableButton(self, btn):
        btn['state'] = 'disabled'
        btn.unbind('<Button-1>')

    def enableButton(self, btn):
        btn['state'] = 'normal'
        btn.bind('<Button-1>', self.buttonCallback)

    def startedTask(self, btn):
        # update button label
        btn['text'] = STOP
        # manage state vars
        self.WORKING = True
        self.startTime = dt.now()
        # disable clicking on all other buttons
        for i, b in enumerate(self.tasks):
            if b['button'] is not btn:
                self.disableButton(b['button'])
            else:
                self.currentTask = i

    def stoppedTask(self, btn):
        btn['text'] = START
        endTime = dt.now()
        totalTime = endTime - self.startTime
        self.tasks[self.currentTask]['totalTime'] += totalTime
        self.tasks[self.currentTask]['totalLabel']['text'] = str(self.tasks[self.currentTask]['totalTime'])
        self.tasks[self.currentTask]['timeStamps'].append(
            ( self.startTime.strftime("%H:%M:%S"), endTime.strftime("%H:%M:%S") ) )

        # manage state vars
        self.WORKING = False
        self.currentTask = None
        self.startTime = None
        # enable all buttons
        for i, b in enumerate(self.tasks):
            self.enableButton(b['button'])

    def buttonCallback(self, event):
        # print("CurrTime:", dt.now())
        if event.widget['text'] == START:
            self.startedTask(event.widget)
        else:
            self.stoppedTask(event.widget)

    def appCloseHandler(self):
        print("Exiting...")
        if self.WORKING:
            task = '"'+self.tasks[self.currentTask]['task']+'"'
            message = ' '.join([task, "is till running. Press OK to stop it and exit. "])
            result = messagebox.askokcancel("Wait", message)
            if not result:
                return
            else:
                self.stoppedTask(self.tasks[self.currentTask]['button'])
        
        # SAVE EVERYTHING
        fileName = str(date.today()) + ".csv"
        headerLine = True
        if os.path.exists(fileName): headerLine = False
        with open(fileName, "a") as f:
            writer = csv.writer(f, delimiter=",")
            today = str(date.today())
            if headerLine: writer.writerow([today, 'Task', 'Total Time', 'Start Time', 'End Time'])
            for t in self.tasks:
                # don't include task if didn't work on it
                # if len(t['timeStamps']) == 0:
                #     writer.writerow([today, t['task'], t['totalLabel']['text'], '', ''])
                for interval in t['timeStamps']:
                    writer.writerow([today, t['task'], t['totalLabel']['text'], interval[0], interval[1]])
        # DONE
        self.application.destroy()


if __name__ == "__main__":
    myApp = Track()
    

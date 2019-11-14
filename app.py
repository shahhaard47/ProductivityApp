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
# import humanize

from AutocompleteEntry import AutocompleteEntry

# Constants
START = "Start"
STOP = "Stop"
FILE_PREFIX = "data/"
KEYWORDS_FILE = FILE_PREFIX+'_keywords_.csv'
saveOften_mins = 5
saveOften_ms = int(saveOften_mins*(60*1000))

# file must be called directly from within folder containing it (if not change dir to folder containing it)
appFile = os.path.realpath(__file__)
parentDir = os.path.dirname(appFile)
cwd = os.getcwd()
if not cwd==parentDir:
    os.chdir(parentDir)
    print("changed cwd")
    print(os.getcwd())

# create data folder if doesn't exist
if not os.path.isdir(FILE_PREFIX):
    os.mkdir(FILE_PREFIX)

class Track(object):

    def __init__(self):
        self.application = Tk()
        # configure window
        self.application.title('Productivity Czar')
        self.application.geometry('800x600')
        self.application.protocol('WM_DELETE_WINDOW', self.appCloseHandler)
        # ADD Widgets
        # self.button = Button(self.application, text=START, width=20, command=self.buttonCallback)
        self.tasks = [] # each element will be dictionary
        self.btns = []

        self.taskKeyWords = [] # should be loaded from a file
        self.todaysTasks = [] # to prevent repeats from being added
        self.newKeywords = [] # keeps track of new words user adds during a session

        self.taskEntry = AutocompleteEntry(self.taskKeyWords, self.todaysTasks, self.application, width=40)
        self.taskEntry.grid(row=0, column=0, pady=10, padx=10)
        # self.taskEntry.bind('<Return>', self._addTaskWithReturnKey)
        # keyboard shortcuts
        self.bindEntryToKeys(self.taskEntry)

        addButton = Button(self.application, text="Add Task", command=self.addTask, anchor="w", width=20, height=2, background="green") # TODO: pass in entry as argument
        addButton.grid(row=0, column=1, pady=10)

        self.taskFrame = Frame(self.application)
        self.taskFrame.grid(row=2, column=0, pady=10)

        self.buttonFrame = Frame(self.application)
        self.buttonFrame.grid(row=2, column=1, pady=10)

        # state vars
        self.WORKING = False
        self.currentTask = None # assigned to index
        self.startTime = None # datetime
        self.totalTasks = 0
        self.skipSave = True  # skip autosaving when app has just turned on. but continue autosaving every `saveOften_ms` after that

        self.initializePrevious()
        self.loadPreviousTaskKeywordsFromFile()

        self.__dynamicSaveTasks__()  # must only be called once and from here

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
            if len(t) == 3: # hrs:mins:secs.micros
                hours = int(t[0])
                minutes = int(t[1])
                last = t[2]
            elif len(t) == 2: # mins:secs.micros
                minutes = int(t[0])
                last = t[1]
            else:
                print("len of time split", len(t), "time", strTime)
            if '.' in last:
                last = last.split('.')
                seconds = int(last[0])
                micros = int(last[1])
            else:
                seconds = int(last)
        return timedelta(days=days, hours=hours, minutes=minutes, seconds=seconds, microseconds=micros)


    def loadPreviousTaskKeywordsFromFile(self):
        # update self.taskKeyWords list
        keywordsFile = KEYWORDS_FILE
        if not os.path.exists(keywordsFile):
            with open(keywordsFile, "w") as f:
                pass
            return
        with open(keywordsFile) as f:
            # FILE FORMAT: all keywords on one row separated by commas
            reader = csv.reader(f, delimiter=',')
            for words in reader:
                for word in words:
                    if word not in self.todaysTasks: 
                        self.taskKeyWords.append(word)

    def initializePrevious(self):
        '''Initialize previous tasks from today if they exist'''
        dayFile = FILE_PREFIX + str(date.today())+'.csv'
        if not os.path.exists(dayFile): return
        # file exists
        with open(dayFile) as f:
            reader = csv.reader(f, delimiter=',')
            rows = [r for r in reader]
            for i in range(1, len(rows)):
                row = rows[i]
                if row[0]:
                    self.addTask(taskText=row[1], totalTime=self.strToTimedelta(row[2]))
                else: # found timestamps for prev task
                    s = row[3]
                    e = row[4]
                    self.tasks[-1]['timeStamps'].append((s, e))

    def bindEntryToKeys(self, entryObj):
        entryObj.bind('<Return>', self._addTaskWithReturnKey)
        entryObj.bind('<Control-BackSpace>', self._deleteLastWordEntry)
        entryObj.bind('<Shift-BackSpace>', self._deleteWholeEntry)

    def _addTaskWithReturnKey(self, entry):
        if self.taskEntry.get() == '': return
        self.addTask()
    
    def _deleteLastWordEntry(self, event):
        words = self.taskEntry.get()
        if words == '': return
        totallen = len(words)
        lastlen = len(words.split()[-1])
        self.taskEntry.delete(totallen-lastlen, "end")
        # return "break"

    def _deleteWholeEntry(self, event):
        self.taskEntry.delete(0, "end")

    def labelClicked(self, event):
        thisTask = None
        
        for t in self.tasks:
            if event.widget is t['taskLabel']:
                thisTask = t
        if thisTask['timeStamps']:
            se = thisTask['timeStamps'][-1]
            [s, e] = [dt.strptime(i, "%m-%d-%Y %H:%M:%S") for i in se]
            dur = str(e - s)
            dur = dur[:-7] if '.' in dur else dur
            # msg = " ".join(["Last action was", humanize.naturaldelta(dur), "long. Would you like to undo it?"])
            # result = messagebox.askyesno("Action", msg)
            if result:
                # TODO:
                print("delete last action from", thisTask)
        else:
            result = messagebox.askyesno("Action", "Would you like to delete this event?")
            if result:
                # TODO:
                print("delete the task", thisTask)

    def addTask(self, taskText=None, totalTime=None, timeStamps=None):
        # do nothing if taskEntry box is empty
        if not taskText and self.taskEntry.get() == '': return
        # task
        if not taskText: # added through GUI
            taskText = self.taskEntry.get()
            if taskText not in self.taskKeyWords:
                self.newKeywords.append(taskText)
        taskText = self.taskEntry.get() if taskText is None else taskText
        if taskText in self.todaysTasks:
            messagebox.showerror("Already Exists", taskText+" already exists. It won't be added.")
            self.taskEntry.delete(0, "end")
            return
        self.todaysTasks.append(taskText)
        task = Label(self.application, text=taskText, anchor='c', width=40, borderwidth=1, relief="solid")
        task.grid(row=self.totalTasks + 1, column=0)
        task.bind("<Button-1>", self.labelClicked)
        self.taskEntry.delete(0, "end")
        # start stop button
        b = self.createButton()
        b.grid(row=self.totalTasks + 1, column=1)
        if self.WORKING: self.disableButton(b)
        # total time label
        totalTime = timedelta() if totalTime is None else totalTime
        totTime = Label(self.application, text=str(totalTime), justify='right', width=20)
        totTime.grid(row=self.totalTasks + 1, column=2)
        # add to tasks lst
        self.tasks.append({
            "taskLabel" : task,
            "task" : task['text'],
            "button" : b,
            "totalTime" : totalTime,
            "totalLabel" : totTime,
            "timeStamps" : [] if timeStamps is None else timeStamps
        })
        self.totalTasks += 1


    def createButton(self):
        button = Button(self.application, text=START, width=20)
        button.bind("<Button-1>", self.buttonCallback)
        # button.pack()
        return button

    def disableButton(self, btn):
        btn['state'] = 'disabled'
        btn.unbind('<Button-1>')

    def enableButton(self, btn):
        btn['state'] = 'normal'
        btn.bind('<Button-1>', self.buttonCallback)

    def currentTaskCounter(self):
        '''DYNAMIC TASK'''
        if not self.WORKING: return
        curidx = self.currentTask
        prevCount = self.tasks[curidx]['totalTime']
        newCount = prevCount + (dt.now() - self.startTime)
        newCount = str(newCount)
        if '.' in newCount: newCount = newCount[:-7]
        self.tasks[curidx]['totalLabel']['text'] = newCount
        Tk.after(self.application, 1000, func=self.currentTaskCounter)

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
        self.currentTaskCounter()

    def stoppedTask(self, btn):
        btn['text'] = START
        endTime = dt.now()
        totalTime = endTime - self.startTime
        # print(self.startTime, endTime)
        self.tasks[self.currentTask]['totalTime'] += totalTime
        strTD = str(self.tasks[self.currentTask]['totalTime']) #string timeDelta
        self.tasks[self.currentTask]['totalLabel']['text'] = strTD[:-7] if '.' in strTD else strTD
        self.tasks[self.currentTask]['timeStamps'].append(
            (self.startTime.strftime("%m-%d-%Y %H:%M:%S"), endTime.strftime("%m-%d-%Y %H:%M:%S")))  # TODO: add date to the timestamp

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

    def saveTasksToFile(self):
        # Save tasks
        fileName = FILE_PREFIX + str(date.today()) + ".csv"
        # always overwrites previous file
        with open(fileName, "w") as f:
            writer = csv.writer(f, delimiter=",")
            today = str(date.today())
            writer.writerow(['SaveDate', 'Task', 'Total Time', 'Start', 'End'])
            for idx, t in enumerate(self.tasks):
                writer.writerow([today, t['task'], t['totalLabel']['text'], '', ''])
                for interval in t['timeStamps']:
                    writer.writerow(['', '', '', interval[0], interval[1]])
                if idx == self.currentTask:
                    # TODO: deal with if self.WORKING is True
                    pass

    def __dynamicSaveTasks__(self):
        if not self.skipSave:
            self.saveTasksToFile()
        else: 
            self.skipSave = False
        Tk.after(self.application, saveOften_ms, func=self.__dynamicSaveTasks__) # every 5 mins

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
        self.saveTasksToFile()

        # Save Keywords
        ##  Add self.newKeywords to _keywords_.csv if not already there
        if self.newKeywords:
            with open(KEYWORDS_FILE, "a") as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow(self.newKeywords)
        # DONE
        self.application.destroy()


if __name__ == "__main__":
    myApp = Track()
    

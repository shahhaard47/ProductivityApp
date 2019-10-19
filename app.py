from tkinter import *
from datetime import datetime as dt

# Constants
START = "Start"
STOP = "Stop"

class Track(object):
    def __init__(self):
        self.application = Tk()
        # configure window
        self.application.title('Productivity Tracker')
        self.application.geometry('600x100')
        self.application.protocol('WM_DELETE_WINDOW', self.appCloseHandler)
        # ADD Widgets
        # self.button = Button(self.application, text=START, width=20, command=self.printBS)
        self.btns = []
        self.btns.append(self.createButton())
        self.btns.append(self.createButton())

        # DONE adding widgets
        self.application.mainloop()

    def createButton(self):
        button = Button(self.application, text=START, width=20)
        button.bind("<Button-1>", self.printBS)
        button.pack()
        return button

    def printBS(self, event):
        print("CurrTime:", dt.now())
        # print("event", event.widget['text'])
        event.widget['text'] = STOP if event.widget['text'] == START else START
        # self.button['text'] = STOP if self.button['text'] == START else START

    def appCloseHandler(self):
        print("Exiting...")
        # SAVE EVERYTHING

        # DONE
        self.application.destroy()


if __name__ == "__main__":
    myApp = Track()
    

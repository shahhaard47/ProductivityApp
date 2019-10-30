"""
from here: http://code.activestate.com/recipes/578253-an-entry-with-autocompletion-for-the-tkinter-gui/
"""

from tkinter import *
import re

lista = ['a', 'actions', 'additional', 'also', 'an', 'and', 'angle', 'are', 'as', 'be', 'bind', 'bracket', 'brackets', 'button', 'can', 'cases', 'configure', 'course', 'detail', 'enter', 'event', 'events', 'example', 'field', 'fields', 'for', 'give', 'important', 'in', 'information', 'is', 'it', 'just', 'key',
         'keyboard', 'kind', 'leave', 'left', 'like', 'manager', 'many', 'match', 'modifier', 'most', 'of', 'or', 'others', 'out', 'part', 'simplify', 'space', 'specifier', 'specifies', 'string;', 'that', 'the', 'there', 'to', 'type', 'unless', 'use', 'used', 'user', 'various', 'ways', 'we', 'window', 'wish', 'you']


class AutocompleteEntry(Entry):
    def __init__(self, lista, highlightLst, *args, **kwargs):

        Entry.__init__(self, *args, **kwargs)
        self.highlightLst = highlightLst
        self.lista = lista
        self.var = self["textvariable"]
        if self.var == '':
            self.var = self["textvariable"] = StringVar()

        self.var.trace('w', self.changed)
        self.bind("<Right>", self.selection)
        self.bind("<Up>", self.up)
        self.bind("<Down>", self.down)

        self.lb_up = False

    def changed(self, name, index, mode):

        if self.var.get() == '':
            self.lb.destroy()
            self.lb_up = False
        else:
            words = self.comparison()
            if words:
                if not self.lb_up:
                    self.lb = Listbox(width=40)
                    self.lb.bind("<Double-Button-1>", self.selection)
                    self.lb.bind("<Right>", self.selection)
                    self.lb.place(x=self.winfo_x(),
                                  y=self.winfo_y()+self.winfo_height())
                    self.lb_up = True

                self.lb.delete(0, END)
                badIndices = []
                goodIndices = []
                for i, w in enumerate(words):
                    if w in self.highlightLst:
                        badIndices.append(i)
                    else:
                        goodIndices.append(i)
                    self.lb.insert(END, w)
                # highlight indices
                # colors chosen from: https://htmlcolorcodes.com 
                # for j in goodIndices: # don't color green for now
                #     self.lb.itemconfig(j, bg="#B3F4A6") # soft green
                for j in badIndices:
                    self.lb.itemconfig(j, bg="#FFDDD6") # soft red
            else:
                if self.lb_up:
                    self.lb.destroy()
                    self.lb_up = False

    def selection(self, event):

        if self.lb_up:
            self.var.set(self.lb.get(ACTIVE))
            self.lb.destroy()
            self.lb_up = False
            self.icursor(END)

    def up(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != '0':
                self.lb.selection_clear(first=index)
                index = str(int(index)-1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def down(self, event):

        if self.lb_up:
            if self.lb.curselection() == ():
                index = '0'
            else:
                index = self.lb.curselection()[0]
            if index != END:
                self.lb.selection_clear(first=index)
                index = str(int(index)+1)
                self.lb.selection_set(first=index)
                self.lb.activate(index)

    def comparison(self):
        pattern = re.compile('.*' + self.var.get() + '.*', re.IGNORECASE)
        return [w for w in (self.lista + self.highlightLst) if re.match(pattern, w)]


if __name__ == '__main__':
    root = Tk()

    entry = AutocompleteEntry(lista, root)
    entry.grid(row=0, column=0)
    Button(text='nothing').grid(row=1, column=0)
    Button(text='nothing').grid(row=2, column=0)
    Button(text='nothing').grid(row=3, column=0)

    root.mainloop()

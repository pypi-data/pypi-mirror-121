from tkinter import *
from tkinter.messagebox import *
import time

class Pack():
    def pack(self, **options):
        return self.frame.pack(**options)
    def pack_forget(self):
        return self.frame.pack_forget()
    def pack_info(self):
        return self.frame.pack_info(self)

class Grid():
    def grid(self, **options):
        return self.frame.grid(**options)
    def grid_forget(self):
        return self.frame.grid_forget()
    def grid_info(self):
        return self.frame.pack_info(self)
    def grid_bbox(self, column=None, row=None, col2=None, row2=None):
        return self.frame.grid_bbox(column, row, col2, row2)
    def grid_columnconfigure(self, index, **options):
        return self.frame.grid_columnconfigure(index, **options)
    def grid_rowconfigure(self, index, **options):
        return self.frame.grid_rowconfigure(index, **options)
    def grid_location(self, x, y):
        return self.frame.grid_location(x, y)
    def grid_remove(self):
        return self.frame.grid_remove()
    def grid_size(self):
        return self.frame.grid_size()

class Place():
    def place(self, **options):
        return self.frame.place(**options)
    def place_forget(self):
        return self.frame.forget()
    def place_info(self):
        return self.frame.pack_info(self)

class Layout(Pack, Grid, Place):
    def forget(self):
        return self.frame.forget()

class Timer():
    def __init__(self, window, mode='timer', arg=0):
        self.end = False
        self.tk = window
        self.mode = mode
        if mode == 'timer':
            self.window = Label(window, text=0)
        elif mode == 'down count':
            self.time = arg
            self.window = Label(window, text=self.time)
        elif mode == 'alarm clock':
            self.time = arg
        else:
            raise AttributeError(''' 'Time' object has no attribute '%s' ''' % mode)
    def timer(per1second):
        psecond = per1second % 100
        # Per 1 S
        second = per1second // 100
        while second >= 60:
            second -= 60
        # S
        minute = per1second // 100 // 60
        while minute >= 60:
            minute -= 60
        # Min
        hour = per1second // 100 // 60 // 60
        while hour >= 24:
            hour -= 24
        # H
        day = per1second // 100 // 60 // 60 // 24
        # D
        return '%s : %s : %s : %s : %s' % (day, hour, minute, second, psecond)
    def mainloop(self):
        if self.mode == 'timer':
            per1second = 0
            while self.end != True:
                self.window.config(text=Timer.timer(per1second))
                self.tk.update()
                time.sleep(0.01)
                per1second += 1
        elif self.mode == 'down count':
            while self.time > 0:
                self.window.config(text=Timer.timer(self.time))
                self.tk.update()
                time.sleep(0.01)
                self.time -= 1
        elif self.mode == 'alarm clock':
            while self.time > 0:
                self.tk.update()
                time.sleep(0.01)
                self.time -= 1
    def stop(self):
        self.end == True

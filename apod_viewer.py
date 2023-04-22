from tkinter import *
import inspect
import os
import apod_desktop

# Determine the path and parent directory of this script
script_path = os.path.abspath(inspect.getframeinfo(inspect.currentframe()).filename)
script_dir = os.path.dirname(script_path)

# Initialize the image cache
apod_desktop.init_apod_cache(script_dir)

# TODO: Create the GUI
root = Tk()
root.geometry('600x400')
root.title('apod desktop')

title_lab = Label(root, text= 'astronomy picture of the day')
title_lab.pack(padx=10)

date_lab = Label(root, text= 'date')
date_lab.pack(padx=10)

root.mainloop()
from tkinter import *
from tkinter import ttk
from src import MainWindow

def run():
  root = Tk()
  root.state('zoomed')
  root.resizable(0, 0) 

  root.title('Flow manager')

  root.columnconfigure(0, weight=1)
  root.rowconfigure(1, weight=1)

  mw = MainWindow(root)

  root.mainloop() 

if __name__ == '__main__':
    run() 
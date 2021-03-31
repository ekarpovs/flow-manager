from tkinter import *
from tkinter import ttk

from src import MainWindow

if __name__ == '__main__':
  root = Tk()
  root.title("Flow Manager")
  root.state('zoomed')
  root.resizable(0, 0) 

  myapp = MainWindow(root)

  root.mainloop()
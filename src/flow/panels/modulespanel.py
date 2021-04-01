from tkinter import *
from tkinter import ttk

from ...uiconst import *
from .panel import Panel

class ModulesPanel(Panel):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self['bg'] = "light yellow"
    self['text'] = 'Modules panel'

    self.grid()
    self.rowconfigure(0, weight=3)
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)

    self.tree_view = ttk.Treeview(self)
    # Inserted at the root, program chooses id:
   
    self.tree_view["columns"] = ("one", "two")
    self.tree_view.column("one", width=10)
    self.tree_view.column("two", width=50)
    self.tree_view.heading("one", text="Operation")
    self.tree_view.heading("two", text="Description")

    # self.tree_view_scrollbar = ttk.Scrollbar(self.tree_view, orient="vertical", command=self.tree_view.yview)
    # self.tree_view_scrollbar.grid(row=2, column=0, sticky=S + W + N)
    # self.tree_view.configure(yscrollcommand=self.tree_view_scrollbar.set)


    # Temporary

    # insert sub-item, method 1 by index
    id1 = self.tree_view.insert("", "end", "bsc", text="Base operations")
    self.tree_view.insert(id1, "end", values=("bsc.crop", "Crops an image."))
    self.tree_view.insert(id1, "end", values=("bsc.flip", "Flips an image."))
    #  insert sub-item, method 2 by name
    self.tree_view.insert("", "end", "blur", text="Bluring operations")
    self.tree_view.insert("blur", "end", values=("blur.avg", "Performs average bluring."))
    self.tree_view.insert("blur", "end", values=("blur.gaus", "Performs Gausian blurring"))
 
    self.tree_view.insert("", "end", "cnts", text="Contours operations")
    self.tree_view.insert("cnts", "end", values=("cnts.find", "Finds contours of an image."))
    self.tree_view.insert("cnts", "end", values=("cnts.sort", "Sorts contours."))

    # Temporary


    self.tree_view.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=S + W + E + N)


  def set_modules(self, modules):
    print("MD", modules)

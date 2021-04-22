from tkinter import *
from tkinter import ttk

from ...uiconst import *
from .view import View

'''
Path item
self.tree_view.insert(parent="", index="end", iid="p1", text="Path  to common modules")
Module item
self.tree_view.insert(parent="p1", index="end", iid="bsc", text="bsc", values=("01","Base oprations"))
Operation items
self.tree_view.insert(parent="bsc", index="end", iid="crop", text="crop", values=("01.01","Crops an image"))
self.tree_view.insert(parent="bsc", index="end", iid="flip", text="flip", values=("01.02","Flips an image"))
'''

class ModulesView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self['bg'] = "light yellow"
    self['text'] = 'Modules panel'

    # height, width = get_panel_size(parent)
    # print("modules panel size", height, width)

    self.grid()
    self.rowconfigure(0, weight=3)
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)
    # self.columnconfigure(1, weight=1)

    self.tree_view = ttk.Treeview(self)
    # Inserted at the root, program chooses id:
   
    self.tree_view["columns"] = ("one", "two")
    # self.tree_view["columns"] = ("two")
    self.tree_view.column("one", width=5)
    self.tree_view.column("two", width=50)
    self.tree_view.heading("one", text="Index")
    self.tree_view.heading("two", text="Description")

    self.tree_view_scrollbar = ttk.Scrollbar(self, orient=VERTICAL, command=self.tree_view.yview)
    self.tree_view_scrollbar.grid(row=0, column=1, sticky=N+S)
    self.tree_view.configure(yscrollcommand=self.tree_view_scrollbar.set)
    
    self.tree_view.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=S + W + E + N)

    self.btn_add = Button(self, text='Add', width=BTNW)
    self.btn_add.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=W + N)


  def set_modules_meta(self, modules_meta):
    for item in modules_meta:
      # print(modules_meta)
      parent = item['parent']
      index = item['index']
      iid = item['iid']
      text = item['text']
      if 'values' in item:
        values = (item['values'][0], item['values'][1])
        self.tree_view.insert(parent=parent, index=index, iid=iid, text=text, values=values)
      else:
        self.tree_view.insert(parent=parent, index=index, iid=iid, text=text)

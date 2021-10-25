from tkinter import *
from tkinter import ttk
from typing import List

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

    # self['bg'] = "light yellow"
    self['text'] = 'Modules'

    # height, width = get_panel_size(parent)
    # print("modules panel size", height, width)

    self.grid()
    self.rowconfigure(0, weight=3)
    self.columnconfigure(0, weight=1)
    
    # Setup Treeview
    self.tree_view = ttk.Treeview(self, columns=("index", "description"), selectmode="browse")
    # Setup the treview heading
    self.tree_view.heading('#0', text='Operation', anchor=W)
    self.tree_view.heading('#1', text='Index', anchor=W)  
    self.tree_view.heading('#2', text='Description', anchor=W)    
    
    self.tree_view.column('#0', minwidth=100, width=160, anchor=W)
    self.tree_view.column('#1', minwidth=30, width=50, anchor=W)
    self.tree_view.column('#2', minwidth=200, width=400, anchor=W)

    self.tree_view_scrollbar_y = ttk.Scrollbar(self, orient=VERTICAL, command=self.tree_view.yview)
    self.tree_view_scrollbar_y.grid(row=0, column=2, sticky=N+S)
    self.tree_view.configure(yscrollcommand=self.tree_view_scrollbar_y.set)

    self.tree_view_scrollbar_x = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tree_view.xview)
    self.tree_view_scrollbar_x.grid(row=1, column=0, columnspan=2, sticky=W+E)
    self.tree_view.configure(xscrollcommand=self.tree_view_scrollbar_x.set)

    self.tree_view.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=S + W + E + N)

  def open_children(self, parent):
    self.tree_view.item(parent, open=True)
    for child in self.tree_view.get_children(parent):
        self.open_children(child)

  def open_all(self):
    self.open_children(self.tree_view.focus())


  @property
  def modules_defs(self) -> List[str]:
    cur_id = self.tree_view.focus()
    return self.tree_view.get_children(cur_id)

  @modules_defs.setter
  def modules_defs(self, modules_defs: List[str]) ->None:
    for mdef in modules_defs:
      parent = mdef.get('parent')
      index = mdef.get('index')
      iid = mdef.get('iid')
      text = mdef.get('text')
      if 'values' in mdef:
        values = mdef.get('values')
        self.tree_view.insert(parent=parent, index=index, iid=iid, text=text, values=(values[0], values[1]))
      else:
        self.tree_view.insert(parent=parent, index=index, iid=iid, text=text)
    return


  def get_selected_operation_meta(self):
    cur_id = self.tree_view.focus()
    if len(self.tree_view.get_children(cur_id)) == 0:
      return cur_id
    else:
      return None
from tkinter import *
from tkinter import ttk
from tkscrolledframe import ScrolledFrame
from typing import List

from ....uiconst import *
from ..view import View

'''
Path item
self.tree_view.insert(parent="", index="end", iid="p1", text="Path  to common modules")
Module item
self.tree_view.insert(parent="p1", index="end", iid="bsc", text="bsc", values=("01","Base oprations"))
Operation items
self.tree_view.insert(parent="bsc", index="end", iid="crop", text="crop", values=("01.01","Crops an image"))
self.tree_view.insert(parent="bsc", index="end", iid="flip", text="flip", values=("01.02","Flips an image"))
'''

class ModuleView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self['text'] = 'Modules'

    self.grid()
    self.rowconfigure(0, weight=10)
    self.columnconfigure(0, weight=1)
    self.rowconfigure(1, weight=8)
    
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
    self.tree_view_scrollbar_y.grid(row=0, column=0, sticky=N+S+E)
    self.tree_view.configure(yscrollcommand=self.tree_view_scrollbar_y.set)
    self.tree_view_scrollbar_x = ttk.Scrollbar(self, orient=HORIZONTAL, command=self.tree_view.xview)
    self.tree_view_scrollbar_x.grid(row=0, column=0, columnspan=2, sticky=W+E+S)
    self.tree_view.configure(xscrollcommand=self.tree_view_scrollbar_x.set)
    self.tree_view.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=S + W + E + N)

    # # Opreation doc content will be scrolable
    # self.content = ScrolledFrame(self, use_ttk=True)
    # self.content.grid(row=1, column=0, padx=PADX, pady=PADY_S, sticky=W + E + N + S)
    # # Create the doc frame within the ScrolledFrame
    # self.doc_view = self.content.display_widget(Frame)
    # Doc label
    self._doc_label_var = StringVar()
    self._doc_label = Label(self, textvariable=self._doc_label_var, justify=LEFT, anchor='nw')
    self._doc_label.grid(row=1, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=S + W + E + N)

    return

  def open_children(self, parent):
    self.tree_view.item(parent, open=True)
    for child in self.tree_view.get_children(parent):
        self.open_children(child)

  def open_all(self):
    self.open_children(self.tree_view.focus())


  @property
  def module_defs(self) -> List[str]:
    cur_id = self.tree_view.focus()
    return self.tree_view.get_children(cur_id)

  @module_defs.setter
  def module_defs(self, modules_defs: List[str]) ->None:
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

  
  def get_selected_item_name(self):
    name = self.tree_view.focus()
    if len(self.tree_view.get_children(name)) == 0:
      return name
    else:
      return None

  def get_current_selection_tree(self) -> str:
    cur_item = self.tree_view.focus()
    if '.' not in cur_item:
      cur_item = ''
    return cur_item

  def set_operation_doc(self, doc):
    doc_str = ''
    for line in doc:
      doc_str += line + '\n'
    self._doc_label_var.set(doc_str)
    return

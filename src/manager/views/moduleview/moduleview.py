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
    View.__init__(self, parent)
    self['text'] = 'Modules'
    # self['bg'] = 'green'

    # setup the module view geometry
    h = self._manager_container_h
    w = int(self._manager_container_w/5)
    self['height'] = h
    self['width'] = w
    mod_view_h = int(h*0.65)
    view_w = w-PADX
    doc_view_h = int(h - mod_view_h)
    # do not resize the module frame after a widget will be added
    self.grid_propagate(False)

    self.grid()   
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    
    # setup modules/operation view
    self._modules_view = Frame(self, height=mod_view_h, width=view_w, name='modulesview')
    self._modules_view.grid(row=0, column=0, sticky=N + W + E+ S)
    self._modules_view.rowconfigure(0, weight=1)
    self._modules_view.rowconfigure(0, weight=1)
    self._modules_view.columnconfigure(0, weight=1)
    self._modules_view.columnconfigure(0, weight=1)
    self._modules_view.grid_propagate(False)
    # setup Treeview inside the frame
    self._tree_view = ttk.Treeview(self._modules_view, columns=("index", "description"), selectmode="browse")
    # Setup the treview heading
    self._tree_view.heading('#0', text='Operation', anchor=W)
    self._tree_view.heading('#1', text='Index', anchor=W)  
    self._tree_view.heading('#2', text='Description', anchor=W)     
    self._tree_view.column('#0', minwidth=100, width=160, anchor=W)
    self._tree_view.column('#1', minwidth=30, width=50, anchor=W)
    self._tree_view.column('#2', minwidth=200, width=400, anchor=W)
    self.tree_view_scrollbar_y = ttk.Scrollbar(self._modules_view, orient=VERTICAL, command=self._tree_view.yview)
    self.tree_view_scrollbar_y.grid(row=0, column=1, sticky=N+S+E)
    self._tree_view.configure(yscrollcommand=self.tree_view_scrollbar_y.set)
    self.tree_view_scrollbar_x = ttk.Scrollbar(self._modules_view, orient=HORIZONTAL, command=self._tree_view.xview)
    self.tree_view_scrollbar_x.grid(row=1, column=0, sticky=W+E+S)
    self._tree_view.configure(xscrollcommand=self.tree_view_scrollbar_x.set)
    self._tree_view.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=N + W + E + S)

    # setup doc view
    self._doc_view = Frame(self, height=doc_view_h, name='modulesdocview', bg='blue')
    self._doc_view.grid(row=1, column=0, sticky=N + W + E+ S)
    self._doc_view.rowconfigure(0, weight=1)
    # self._doc_view.rowconfigure(0, weight=1)
    self._doc_view.columnconfigure(0, weight=1)
    # self._doc_view.columnconfigure(0, weight=1)
    self._doc_view.grid_propagate(False)
    # doc view content will be scrolable
    self._content = ScrolledFrame(self._doc_view, use_ttk=True)
    self._content.grid(row=0, column=0, columnspan=2, sticky=N + W + E + S)
    # create the frame within the ScrolledFrame
    self._oper_doc_view = self._content.display_widget(Frame)
    self._oper_doc_view['width'] = view_w
    # create label, that will be dispaly a doc text within the farme
    self._doc_label_var = StringVar()
    self._doc_label = Label(self._oper_doc_view, textvariable=self._doc_label_var, justify=LEFT, anchor='nw')
    self._doc_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=S + W + E + N)
    return

  def _open_children(self, parent):
    self._tree_view.item(parent, open=True)
    for child in self._tree_view.get_children(parent):
        self._open_children(child)

  def open_all(self):
    self._open_children(self._tree_view.focus())

  @property
  def tree_view(self) -> ttk.Treeview:
    return self._tree_view

  @property
  def module_defs(self) -> List[str]:
    cur_id = self._tree_view.focus()
    return self._tree_view.get_children(cur_id)

  @module_defs.setter
  def module_defs(self, modules_defs: List[str]) ->None:
    for mdef in modules_defs:
      parent = mdef.get('parent')
      index = mdef.get('index')
      iid = mdef.get('iid')
      text = mdef.get('text')
      if 'values' in mdef:
        values = mdef.get('values')
        self._tree_view.insert(parent=parent, index=index, iid=iid, text=text, values=(values[0], values[1]))
      else:
        self._tree_view.insert(parent=parent, index=index, iid=iid, text=text)
    return
  
  def get_selected_item_name(self):
    name = self._tree_view.focus()
    if len(self._tree_view.get_children(name)) == 0:
      return name
    else:
      return None

  def get_current_selection_tree(self) -> str:
    cur_item = self._tree_view.focus()
    if '.' not in cur_item:
      cur_item = ''
    return cur_item

  def set_operation_doc(self, doc):
    doc_str = ''
    for line in doc:
      doc_str += line + '\n'
    self._doc_label_var.set(doc_str)
    return

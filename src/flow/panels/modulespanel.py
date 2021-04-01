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
    self.tree_view['columns'] = ['module', 'operation', 'descr']

    # self.tree_view_scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_view.yview)
    # self.tree_view_scrollbar.grid(row=2, column=0, sticky=S + E + N)
    # self.tree_view.configure(yscrollcommand=self.tree_view_scrollbar.set)

    self.tree_view.heading('#0', text='Index')
    self.tree_view.heading("module", text='Module')
    self.tree_view.heading("operation", text='Operation')
    self.tree_view.heading("descr", text='Description')

    self.tree_view.column("#0", width=5)
    self.tree_view.column("module", width=25)
    self.tree_view.column("operation", width=25)
    self.tree_view.column("descr", width=75)
    # self.tree_view.bind("<<tree_viewSelect>>", self.on_row_click) 
    
    self.tree_view.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=S + W + E + N)

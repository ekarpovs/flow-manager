from tkinter import *
from tkinter.ttk import Combobox
from tkscrolledframe import widget
from typing import Callable, Dict, List, Tuple

from ....uiconst import *


class FlowLinksView(Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 
    # self['bg'] = 'green'

    self.grid()
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)
    self.rowconfigure(0, weight=1)
    
    self._widgets = {'widgets':[]}
    return

  @property
  def widgets(self) -> List[Dict[str, object]]:
    return self._widgets.get('widgets')

  def _clear_widgets(self) -> None:
    # Clear view
    for child in self.winfo_children():
      child.grid_remove()
    # Clear collection
    self._widgets.get('widgets').clear()
    return

  def create_links_view(self, refs: List = [str], links: Dict[str, str] = {}, output_refs: List[str] = []) -> None:
    self._clear_widgets()
    if len(refs) > 0:
      for i, inref in enumerate(refs):
        inref_name = inref.get('name')
        get, inref_lbl, inref_combo = self._create_link_view(inref_name, links, output_refs)
        inref_lbl.grid(row=i, column=0, padx=PADX_S, pady=PADY_S, sticky=W)
        inref_combo.grid(row=i, column=1, columnspan=2, padx=PADX_S, pady=PADY_S, sticky=W)
        self._widgets['widgets'].append({'name': inref_name, 'getter': get, 'label': inref_lbl, 'combo': inref_combo})
    return

  def _create_link_view(self, inref_name: str, links: Dict[str, str], output_refs: List[str]) -> Tuple[Callable, Widget, Widget]:
    def get():
      return inref_combo.get()

    text = f'{inref_name}:'
    inref_lbl = Label(self, text=text, anchor=W, justify=LEFT, width=10)
    var = StringVar()
    inref_combo = Combobox(self, name=inref_name, justify=LEFT, width=45)
    inref_combo['values'] = output_refs
    # Assign current value
    if len(links) > 0:
      link = links.get(inref_name)
      if link is not None:
        inref_combo.set(link)
        inref_combo.textvariable = var     
    return get, inref_lbl, inref_combo

    # def _set_current_value(self, widget: Widget) -> None:
    #   return
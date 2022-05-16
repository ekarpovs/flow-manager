from turtle import width
from typing import List, Dict, Tuple, Callable
import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox, LabelFrame
from tkscrolledframe import ScrolledFrame
import copy

from flow_model import FlowModel, FlowItemModel

from ....uiconst import *
from ..view import View

class LinksView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self['text'] = 'Links'
    self.update_idletasks()
    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_reqwidth()

    self._flow = None
    self._grid_rows_descr: List[Dict] = []
    self._possible_input: List[str] = []
    self._active_wd_idx = -1

    self.grid()
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)

    self._infovar = StringVar()
    self._info_entry = Entry(self, name='flow_info',textvariable=self._infovar, width=35)
    self._info_entry.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=N+W+E)
    self._info_desr = {'getter': self._infovar.get, 'setter': self._infovar.set, 'wd': self._info_entry}
    # Content will be scrolable
    self._content = ScrolledFrame(self, use_ttk=True, height=int(h/5), width=int((w/2)))
    self._content.grid(row=1, column=0, padx=PADX, pady=PADY_S, sticky=W + E)
    # Create the params frame within the ScrolledFrame
    self._links_view = self._content.display_widget(Frame)
    return

  @property
  def descriptors(self) -> List[Dict]:
    return self._grid_rows_descr

  @property
  def info_descr(self) -> str:
    return self._info_desr

  def get_active_item_link_descriptors(self) -> List[List[Widget]]:
    if self._active_wd_idx < 0:
      return None
    descriptors = self._grid_rows_descr[self._active_wd_idx]
    return descriptors

  def clear(self) -> None:     
    self._infovar.set('')
    for child in self._links_view.winfo_children():
      child.grid_remove()
    self._grid_rows_descr.clear()
    self._content.scroll_to_top()
    self._possible_input.clear()
    self._active_wd_idx = -1
    return

  def build(self, flow: FlowModel) -> None:
    self._flow = flow
    self._infovar.set(flow.info)
    items = copy.deepcopy(flow.items)
    for i, item in enumerate(items):
      item_links_frame = self._create_item_links_container(i+1, item)
      item_links_frame.grid(row=i+1, column=0, padx=PADX, sticky=W + E)
      item_links_frame.columnconfigure(0, weight=1)
      item_links_frame.columnconfigure(1, weight=1)
      item_links_descr = self._create_item_links_widgets(item_links_frame, i, item)
      self._grid_rows_descr.append(item_links_descr)
    self._disable_all()
    self._active_wd_idx = 0
    self._hightlighte_active_wd(True)
    self._set_active_wd_state(True)
    return  

  def _create_item_links_container(self, idx: int, item: FlowItemModel) -> Widget:
    i_n = item.name.replace('.', '-')
    name = f'--{idx}-{i_n}--'
    item_links_frame = LabelFrame(self._links_view, name=name)
    return item_links_frame

  def _create_item_links_widgets(self, container: LabelFrame, idx: int, item: FlowItemModel) -> Dict:
    item_links_descr = []
    title = f'{idx}-{item.name}'
    i_n = item.name.replace('.', '-')
    name = f'--{idx}-{i_n}--'
    item_label = Label(container, name=name, text=title)
    item_label.grid(row=0, column=0, padx=PADX_S, pady=PADY_S, sticky=W)
    item_links_descr.append({'name': item_label.winfo_name(), 'getter': None, 'setter': None, 'wd': item_label})
    infovar = StringVar()
    infovar.set(item.title)
    info_entry = Entry(container, textvariable=infovar, width=38)
    info_entry.grid(row=0, column=1, padx=PADX_S, pady=PADY_S, sticky=E)
    item_links_descr.append({'name': info_entry.winfo_name(), 'getter': infovar.get, 'setter': None, 'wd': info_entry})


    inrefs_def = item.inrefs_def
    outrefs_def = item.outrefs_def

    for i, outref_def in enumerate(outrefs_def):
      outref_name = outref_def.get('name')
      self._possible_input.append(f'{title}-{outref_name}')

    links = item.links
    if len(inrefs_def) > 0:
      for i, inref_def in enumerate(inrefs_def):
        inref_name = inref_def.get('name')
        getter, inref_lbl, inref_combo = self._create_link_widget(container, inref_name, links)
        inref_lbl.grid(row=i+1, column=0, padx=PADX_S, pady=PADY_S, sticky=W)
        inref_combo.grid(row=i+1, column=1, columnspan=2, padx=PADX_S, pady=PADY_S, sticky=E)
        item_links_descr.append({'name': inref_name, 'getter': getter, 'setter': None, 'wd': inref_combo})
    return item_links_descr

  def _create_link_widget(self, container: LabelFrame, inref_name: str, links: Dict[str, str]) -> Tuple[Callable, Widget, Widget]:
    def get():
      return inref_combo.get()

    text = f'{inref_name}:'
    inref_lbl = Label(container, text=text, anchor=W, justify=LEFT, width=10)
    var = StringVar()
    inref_combo = Combobox(container, name=inref_name, justify=LEFT, width=35)
    inref_combo['values'] = copy.deepcopy(self._possible_input[:len(self._possible_input)-2])
    # Assign current value
    if len(links) > 0:
      link = links.get(inref_name)
      if link is not None:
        inref_combo.set(link)
        inref_combo.textvariable = var     
    return get, inref_lbl, inref_combo

  def set_active_wd(self, idx: int) -> None:
    self._hightlighte_active_wd()
    self._set_active_wd_state()
    self._active_wd_idx = idx
    self._hightlighte_active_wd(True)
    self._set_active_wd_state(True)
    return
  
  def _set_active_wd_state(self, active: bool = False) -> None:
    state = DISABLED
    if active:
      state = NORMAL
    descriptors = self._grid_rows_descr[self._active_wd_idx]
    for descr in descriptors:
      widget = descr.get('wd')
      widget['state'] = state
    return

  def _disable_all(self) -> None:
    for descriptors in self._grid_rows_descr:
      for descr in descriptors:
        widget = descr.get('wd')
        widget['state'] = DISABLED
    return

  # UI methods

  def _hightlighte_active_wd(self, active: bool = False) -> None:
    fg_color = 'black'
    bg_color = 'SystemButtonFace'
    if active:
      fg_color = 'white'
      bg_color = 'blue'
    descriptors = self._grid_rows_descr[self._active_wd_idx]
    for descr in descriptors:
      widget = descr.get('wd')
      name = widget.winfo_name()
      if name.startswith('--'):
        widget['fg'] = fg_color
        widget['bg'] = bg_color
        break   
    return

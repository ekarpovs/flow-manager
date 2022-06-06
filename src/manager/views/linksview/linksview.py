from turtle import width
from typing import List, Dict, Tuple, Callable
import tkinter as tk
from tkinter import *
from tkinter.ttk import Combobox, LabelFrame
from tkscrolledframe import ScrolledFrame
import copy
from tkinter import font

from flow_model import FlowModel, FlowItemModel

from ....uiconst import *
from ..view import View


class LinksView(View):
  def __init__(self, parent):
    View.__init__(self, parent)
    self['text'] = 'Links'
    # self['bg'] = 'red'
    
    h = int(self._manager_container_h * 0.22)
    w = int((self._manager_container_w / 4) * 0.95)
    self['height'] = h
    self['width'] = w

    self.grid_propagate(False)
    self.grid()
    self.rowconfigure(0, weight=1)

    # setup modules/operation view
    self._links_view = Frame(self, height=h, width=w, name='limksview')
    self._links_view.grid(row=0, column=0, sticky=N +W + E+ S)
    self._links_view.rowconfigure(0, weight=1)
    self._links_view.rowconfigure(1, weight=1)
    self._links_view.columnconfigure(0, weight=1)
    self._links_view.grid_propagate(False)

    if_h = int(h*0.15)
    self._info_farme = Frame(self._links_view, height=if_h, name='limksviewinfo')
    self._info_farme.grid(row=0, column=0, padx=PADX, sticky=N + W + E+ S)
    # self._info_farme.rowconfigure(0, weight=1)
    # self._info_farme.columnconfigure(0, weight=1)
    self._infovar = StringVar()
    self._info_entry = Entry(self._info_farme, name='flow_info',textvariable=self._infovar, width=68)
    self._info_entry.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=N+W)
    self._info_desr = {'getter': self._infovar.get, 'setter': self._infovar.set, 'wd': self._info_entry}

    sf_h = int(h*0.85)
    self._links_farme = Frame(self._links_view, height=sf_h, name='limksviewframe')
    self._links_farme.grid(row=1, column=0, padx=PADX, sticky=N + W + E+ S)
    self._links_farme.rowconfigure(0, weight=1)
    self._links_farme.columnconfigure(0, weight=1)
    self._links_farme.grid_propagate(False)
    # Content will be scrolable
    self._content = ScrolledFrame(self._links_farme, use_ttk=True, height=sf_h-PADY)
    self._content.grid(row=0, column=0, sticky=W+E)
    # Create the links frame within the ScrolledFrame
    self._links = self._content.display_widget(Frame)
    self._flow = None
    self._grid_rows_descr: List[Dict] = []
    self._possible_input: List[str] = []
    self._active_wd_idx = -1
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
    for child in self._links.winfo_children():
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
      item_links_frame = self._create_item_links_container(i, item)
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
    name = f'container--{idx}-{i_n}--'
    item_links_frame = Frame(self._links, name=name)
    return item_links_frame

  def _create_item_links_widgets(self, container: Frame, idx: int, item: FlowItemModel) -> Dict:
    item_links_descr = []
    title = f'{idx}-{item.name}'
    i_n = item.name.replace('.', '-')
    name = f'--{idx}-{i_n}--'
    item_label = Label(container, name=name, text=title, anchor=W, justify=LEFT, width=18)
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

  def _create_link_widget(self, container: Frame, inref_name: str, links: Dict[str, str]) -> Tuple[Callable, Widget, Widget]:
    def get():
      return inref_combo.get()

    text = f'{inref_name}:'
    inref_lbl = Label(container, text=text, anchor=W, justify=LEFT, width=18)
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
    direction = idx - self._active_wd_idx
    self._active_wd_idx = idx
    self._hightlighte_active_wd(True)
    self._set_active_wd_state(True)
    # scroll, when scroll bar was used
    self._stay_active_wd_visible(direction)
    if idx == 0:
      self._content.scroll_to_top()
    return
  
  def _stay_active_wd_visible(self, direction: int) -> None:
    descriptors = self._grid_rows_descr[self._active_wd_idx]
    container = descriptors[0].get('wd').master
    if direction == 0:
      # stay at the same position
      return
    forward = direction > 0
    self._scroll_to_visible(container, forward)
    return
  
  def _scroll_to_visible(self, container: Widget, forward: bool) -> None:
    container_upper_y = container.winfo_rooty()
    container_bottom_y = container_upper_y + container.winfo_reqheight()
    content_upper_y = self._content.winfo_rooty()
    content_bottom_y = content_upper_y + self._content.winfo_reqheight()
    default_font = font.nametofont("TkDefaultFont")
    fdescr = default_font.configure()
    if forward:
      if container_bottom_y > content_bottom_y:
        step = (container_bottom_y - content_bottom_y)//fdescr.get('size')
        self._content.yview(SCROLL, step, UNITS)
    else:
      if container_upper_y < content_upper_y:
        step = (container_upper_y - content_upper_y)//fdescr.get('size')
        self._content.yview(SCROLL, step, UNITS)
    return

  def _set_active_wd_state(self, active: bool = False) -> None:
    state = DISABLED
    if active:
      state = NORMAL
    descriptors = self._grid_rows_descr[self._active_wd_idx]
    for descr in descriptors:
      widget: Widget = descr.get('wd')
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
      bg_color = 'RoyalBlue'
    descriptors = self._grid_rows_descr[self._active_wd_idx]
    for descr in descriptors:
      widget = descr.get('wd')
      name = widget.winfo_name()
      if name.startswith('--'):
        widget['fg'] = fg_color
        widget['bg'] = bg_color
        break   
    return

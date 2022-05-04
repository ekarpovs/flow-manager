import numpy as np 
from typing import List, Dict, Tuple, Callable
from tkinter import *
from tkinter.ttk import LabelFrame, Style
from tkscrolledframe import ScrolledFrame

from flow_model import FlowModel, FlowItemModel

from .paramwidgetfactory import ParamWidgetFactory
from ....uiconst import *
from ..view import View

DEFAULT_VIEW_SIZE = 50
WITHOUT_PREVIEW_DATA = -1

class ParamsView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self['text'] = 'Parameters'

    self._factory = ParamWidgetFactory()

    self.update_idletasks()
    h = self.parent.winfo_reqheight()

    # Content will be scrolable
    self._content = ScrolledFrame(self, use_ttk=True, height=int(h/1.4))
    self._content.grid(row=0, column=0, padx=PADX, pady=PADY_S, sticky=W + E)
    # Create the params frame within the ScrolledFrame
    self._params_view = self._content.display_widget(Frame)
    self._grid_rows: List[Widget] = []
    self._active_wd_idx = -1
    return

  def get_active_wd_children(self) -> List[Widget]:
    if self._active_wd_idx < 0:
      return None
    children = []
    active_wd = self._grid_rows[self._active_wd_idx]
    for child in active_wd.winfo_children():
      if child.widgetName != 'label':
        children.append(child)
    return children

  def clear(self) -> None:
    for row in self._grid_rows:
      row.grid_remove()  
    self._grid_rows.clear()
    self._content.scroll_to_top()   
    self._active_wd_idx = -1
    return

  def build(self, flow: FlowModel) -> None:
    for i,item in enumerate(flow.items):
      item_params_frame = self._create_item_params_container(i, item)
      item_params_frame.grid(row=i, column=0, padx=PADX, sticky=W + E)
      self._factory.container = item_params_frame
      self._create_item_params_widgets(item)
      self._grid_rows.append(item_params_frame)
    self._active_wd_idx = 0
    self._hightlighte_active_wd(True)
    return  

  def _create_item_params_container(self, idx: int, item: FlowItemModel) -> Widget:
    # style = Style()
    # style.configure("BG.TLabel", background="green")
    # item_params_frame = LabelFrame(self._params_view, name=f'--{i}--', text=item.name, style="BG.TLabel")
    title = f'{idx}-{item.name}'
    item_params_frame = LabelFrame(self._params_view, name=f'--{idx}--', text=title)
    return item_params_frame

  def _create_item_params_widgets(self, item: FlowItemModel) -> None:
    # merge curent params with params_ws
    params = item.params # Dict
    params_ws = item.params_ws # Dict
    params_def = item.params_def # List[Dict]
    for k in params_ws.keys():
      if k in params:
        continue
      params[k] = params_ws.ket(k)
    # merge create widget, label
    for i, param_def in enumerate(params_def):
      name = param_def.get('name')
      comment = param_def.get('comment')
      pvalue = params.get(name, None)
      if pvalue is not None:
        param_def['default'] = pvalue
      getter, setter, param_widget = self._factory.create(param_def)
      param_widget.grid(row=i, column=1, padx=PADX_S, pady=PADY_S, sticky=W)
      param_label = Label(self._factory.container, text=f'{name}')
      param_label.grid(row=i, column=0, padx=PADX_S, pady=PADY_S, sticky=W)
      param_descr = Label(self._factory.container, text=f'{comment}')
      param_descr.grid(row=i, column=2, padx=PADX_S, pady=PADY_S, sticky=W)
    return 


  def set_active_wd(self, idx: int) -> None:
    self._hightlighte_active_wd()
    self._active_wd_idx = idx
    self._hightlighte_active_wd(True)
    return

  def _hightlighte_active_wd(self, active: bool = False) -> None:
    color = 'SystemButtonFace'
    if active:
      color = 'azure'
    prev_wd = self._grid_rows[self._active_wd_idx]
    children = prev_wd.winfo_children()
    if len(children) > 0: 
      children[0]['bg'] = color
    return
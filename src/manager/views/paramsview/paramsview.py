from typing import List, Dict, Tuple, Callable
from tkinter import *
from tkinter.ttk import Button, LabelFrame
from tkscrolledframe import ScrolledFrame
import copy

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

    self._flow = None
    self._grid_rows_descr: List[Dict] = []
    self._active_wd_idx = -1

    self.grid()
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)

    # Content will be scrolable
    self._content = ScrolledFrame(self, use_ttk=True, height=int(h*0.65))
    self._content.grid(row=0, column=0, padx=PADX, pady=PADY_S, sticky=N + S + W + E)
    # Create the params frame within the ScrolledFrame
    self._params_view = self._content.display_widget(Frame)

    # Setup param actions view
    self._params_actions_frame = Frame(self, highlightbackground='gray', highlightthickness=1)
    self.btn_params_reset = Button(self._params_actions_frame, text='Reset', width=BTNW_S)
    self.btn_params_default = Button(self._params_actions_frame, text='Default', width=BTNW_S)
    self.btn_params_io = Button(self._params_actions_frame, text='I/O', width=BTNW_S)
    self.btn_params_reset.grid(row=0, column=0, padx=PADX, pady=PADY_S, sticky=W+N)
    self.btn_params_default.grid(row=0, column=1, padx=PADX, pady=PADY_S, sticky=W+N)
    self.btn_params_io.grid(row=0, column=2, padx=PADX, pady=PADY_S, sticky=W+N)
    self._params_actions_frame.grid(row=1, column=0, padx=PADX, pady=PADY_S, sticky=W + E + S)

    self._activate_params_buttons()
    return

# API
  @property
  def descriptors(self) -> List[Dict]:
    return self._grid_rows_descr

  def get_active_item_params_widgets(self) -> List[Widget]:
    if self._active_wd_idx < 0:
      return None
    descriptors = self._grid_rows_descr[self._active_wd_idx]
    widgets = []
    for descr in descriptors:
      widget = descr.get('wd')
      widgets.append(widget)
    return widgets

  def get_item_name(self, idx: int) -> str:
    descriptors = self._grid_rows_descr[idx]
    widget_0 = descriptors[0].get('wd')
    parent_name = widget_0.winfo_parent()
    idx_s = parent_name.index('--')
    p_n:str = parent_name[idx_s+2: len(parent_name)-2]
    idx_point = p_n.find('-', 3)
    p_n = p_n[:idx_point] + '.' + p_n[idx_point+1:]
    return p_n

  def get_item_params(self, idx: int) -> Dict:
    params = {}
    descriptors = self._grid_rows_descr[idx]
    for descr in descriptors:
      widget = descr.get('wd')
      name = widget.winfo_name()
      if name.startswith('--'):
        continue
      getter = descr.get('getter')
      value = getter()
      params[name] =  value 
    return params

  def set_item_params(self, idx: int, params) -> None:
    if self._active_wd_idx < 0:
      return None
    descriptors = self._grid_rows_descr[idx]
    for descr in descriptors:
      widget = descr.get('wd')
      name = widget.winfo_name()
      if name.startswith('--'):
        continue
      setter = descr.get('setter')
      setter(params.get(name))
    return

  def clear(self) -> None:     
    for child in self._params_view.winfo_children():
      child.grid_remove()
    self._grid_rows_descr.clear()
    self._content.scroll_to_top()
    self._active_wd_idx = -1
    self._activate_params_buttons()   
    return

# Build
  def build(self, flow: FlowModel) -> None:
    self._flow = flow
    items = copy.deepcopy(flow.items)
    for i, item in enumerate(items):
      item_params_frame = self._create_item_params_container(i, item)
      item_params_frame.grid(row=i, column=0, padx=PADX, sticky=W + E)
      self._factory.container = item_params_frame
      item_params_descr = self._create_item_params_widgets(i, item)
      self._grid_rows_descr.append(item_params_descr)
    self._disable_all()
    self._active_wd_idx = 0
    self._hightlighte_active_wd(True)
    self._set_active_wd_state(True)
    self._activate_params_buttons(True)   
    return  

  def _create_item_params_container(self, idx: int, item: FlowItemModel) -> Widget:
    i_n = item.name.replace('.', '-')
    name = f'--{idx}-{i_n}--'
    item_params_frame = LabelFrame(self._params_view, name=name)
    return item_params_frame

  def _create_item_params_widgets(self, idx: int, item: FlowItemModel) -> Dict:
    # merge curent params with params_ws
    params = item.params # Dict
    params_ws = item.params_ws # Dict
    params_def = item.params_def # List[Dict]
    for k in params_ws.keys():
      if k in params:
        continue
      params[k] = params_ws.ket(k)
    # merge create widget, label
    item_params_descr = []
    title = f'{idx}-{item.name}'
    i_n = item.name.replace('.', '-')
    name = f'--{idx}-{i_n}--'
    item_label = Label(self._factory.container, name=name, text=title)
    item_label.grid(row=0, column=0, columnspan=3, padx=PADX_S, pady=PADY_S, sticky=W)
    item_params_descr.append({'name': item_label.winfo_name(), 'getter': None, 'setter': None, 'wd': item_label})
    for i, param_def in enumerate(params_def):
      name = param_def.get('name')
      comment = param_def.get('comment')
      pvalue = params.get(name, None)
      if pvalue is not None:
        param_def['default'] = pvalue
      getter, setter, param_widget = self._factory.create(param_def)
      param_widget.grid(row=i+1, column=1, padx=PADX_S, pady=PADY_S, sticky=W)
      param_label = Label(self._factory.container, text=f'{name}')
      param_label.grid(row=i+1, column=0, padx=PADX_S, pady=PADY_S, sticky=W)
      param_descr = Label(self._factory.container, text=f'{comment}')
      param_descr.grid(row=i+1, column=2, padx=PADX_S, pady=PADY_S, sticky=W)
      item_params_descr.append({'name': param_widget.winfo_name(), 'getter': getter, 'setter': setter, 'wd': param_widget})
    return item_params_descr

  def set_active_wd(self, idx: int) -> None:
    self._hightlighte_active_wd()
    if self._active_wd_idx > idx:
      # disable, when move backward
      self._set_active_wd_state()
    self._active_wd_idx = idx
    self._hightlighte_active_wd(True)
    self._set_active_wd_state(True)
    self._set_button_io_state(idx)
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

  def _activate_params_buttons(self, activate=False) -> None:
    state = DISABLED
    if activate:
      state = NORMAL
    self.btn_params_reset['state']=state
    self.btn_params_default['state']=state
    self.btn_params_io['state']=state
    return


  def _set_button_io_state(self, idx: int) -> None:
    flow_item = self._flow.get_item(idx)
    params_def = flow_item.params_def
    self.btn_params_io['state'] = DISABLED
    for param_def in params_def:
      if param_def.get('name') == 'path':
        self.btn_params_io['state'] = NORMAL
        break
    return

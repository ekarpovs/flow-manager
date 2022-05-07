from typing import List, Dict, Tuple, Callable
from tkinter import *
from tkinter.ttk import Button, LabelFrame
from tkscrolledframe import ScrolledFrame
import copy

from flow_model import FlowModel, FlowItemModel

from .paramwidgetfactory import ParamWidgetFactory
from .paramsutils import convert_params_def_to_dict
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
    self._content = ScrolledFrame(self, use_ttk=True, height=int(h/1.33))
    self._content.grid(row=0, column=0, padx=PADX, pady=PADY_S, sticky=W + E)
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
    self._params_actions_frame.grid(row=1, column=0, padx=PADX, pady=PADY_S, sticky=W + E)

    self._activate_params_buttons()
    return

  def apply_active_params(self, idx: int) -> None:
    '''
    From active widget to flow item 
    '''
    
    flow_item = self._flow.get_item(idx)
    params_wd = self._get_active_params()
    for k in params_wd.keys():
      flow_item.params[k] = params_wd.get(k)
    return

  def reset_active_params(self, idx: int) -> None:
    '''
    From ws definition to active widget and flow item 
    '''

    flow_item = self._flow.get_item(idx)
    params_ws = copy.deepcopy(flow_item.params_ws)
    params_def = copy.deepcopy(flow_item.params_def)
    params_new = {} 
    for param_def in params_def:
      k = param_def.get('name')
      param_new_val = params_ws.get(k)
      if param_new_val is None:
        # use default value from def
        param_new_val = param_def.get('default')
      flow_item.params[k] = param_new_val
      params_new[k] = param_new_val
    self._set_active_params(params_new)
    return

  def default_active_params(self, idx: int) -> None:
    '''
    From operation params definition to active widget and flow item 
    '''

    flow_item = self._flow.get_item(idx)
    params_def = copy.deepcopy(flow_item.params_def)
    params = convert_params_def_to_dict(params_def)    
    flow_item.params = params
    self._set_active_params(params)
    return

  def update_active_params(self, idx: int) -> None:
    flow_item = self._flow.get_item(idx)
    params = copy.deepcopy(flow_item.params)
    self._set_active_params(params)
    return

  def get_active_param_widgets(self) -> List[Widget]:
    if self._active_wd_idx < 0:
      return None
    descriptors = self._grid_rows_descr[self._active_wd_idx]
    widgets = []
    for descr in descriptors:
      widget = descr.get('wd')
      widgets.append(widget)
    return widgets

  def _get_active_params(self) -> Dict:
    if self._active_wd_idx < 0:
      return None
    params = {}
    descriptors = self._grid_rows_descr[self._active_wd_idx]
    for descr in descriptors:
      widget = descr.get('wd')
      name = widget.winfo_name()
      if name == 'item_name':
        continue
      getter = descr.get('getter')
      value = getter()
      params[name] =  value 
    return params

  def _set_active_params(self, params) -> None:
    if self._active_wd_idx < 0:
      return None
    descriptors = self._grid_rows_descr[self._active_wd_idx]
    for descr in descriptors:
      widget = descr.get('wd')
      name = widget.winfo_name()
      if name == 'item_name':
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

  def build(self, flow: FlowModel) -> None:
    self._flow = flow
    items = copy.deepcopy(flow.items)
    for i,item in enumerate(items):
      item_params_frame = self._create_item_params_container(i, item)
      item_params_frame.grid(row=i, column=0, padx=PADX, sticky=W + E)
      self._factory.container = item_params_frame
      item_params_descr = self._create_item_params_widgets(i, item)
      self._grid_rows_descr.append(item_params_descr)
    self._active_wd_idx = 0
    self._activate_params_buttons(True)   
    self._hightlighte_active_wd(True)
    return  

  def _create_item_params_container(self, idx: int, item: FlowItemModel) -> Widget:
    item_params_frame = LabelFrame(self._params_view, name=f'--{idx}--')
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
    item_label = Label(self._factory.container, name='item_name', text=title)
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
    self._active_wd_idx = idx
    self._hightlighte_active_wd(True)
    self._set_button_io_state(idx)
    return

  # UI methods

  def _hightlighte_active_wd(self, active: bool = False) -> None:
    color = 'SystemButtonFace'
    if active:
      color = 'azure'
    descriptors = self._grid_rows_descr[self._active_wd_idx]
    for descr in descriptors:
      widget = descr.get('wd')
      name = widget.winfo_name()
      if name == 'item_name':
        widget['bg'] = color
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

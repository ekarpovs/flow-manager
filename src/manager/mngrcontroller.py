from tkinter import *
from tkinter.ttk import Combobox, Spinbox, Button
from typing import Callable, Dict, List, Tuple
import cv2
import copy
import os
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename

from flow_storage import *
from flow_model import FlowItemModel, FlowItemType

from .mngrmodel import MngrModel  
from .mngrrunner import MngrRunner 
from .mngrconverter import MngrConverter  
from .mngrview import MngrView  
from ..configuration import Configuration

class MngrController():
  def __init__(self, parent):
    self._cfg = Configuration()
    self._model = MngrModel(self._cfg)
    self._runner = MngrRunner(self._cfg)
    self._converter = MngrConverter()
    self._view = MngrView(parent)
    # Bind to modules panel
    self._view.module.tree_view.bind('<<TreeviewOpen>>', self._open_all)
    self._view.module.tree_view.bind('<<TreeviewSelect>>', self._module_tree_selection_changed)
    # Bind to flows panel
    self.flows_view_idx = 0  
    self._view.flow.names_combo_box.bind('<<ComboboxSelected>>', self._worksheet_selected)
    self._view.flow.btn_reload.bind("<Button>", self._reload_ws_list)
    
    self._view.flow.btn_add.configure(command=self._add_operation_to_flow_model)
    self._view.flow.btn_remove.configure(command=self._remove_operation_from_flow_model)
    self._view.flow.btn_reset.configure(command=self._reset_flow_model)
    self._view.flow.btn_save.configure(command=self._store_flow_model_as_ws)
    self._view.flow.btn_links.configure(command=self._edit_flow_links)
    
    self._view.flow.btn_run.configure(command=self._run)   
    self._view.flow.btn_curr.configure(command=self._apply)   
    self._view.flow.btn_next.configure(command=self._next)
    self._view.flow.btn_prev.configure(command=self._prev)
    self._view.flow.btn_top.configure(command=self._top)

    self._view.flow.flow_tree_view.bind('<<TreeviewSelect>>', self._tree_selection_changed)

    self._view.flow.btn_params_reset.configure(command=self._reset)
    self._view.flow.btn_params_default.configure(command=self._default) 
    self._view.flow.btn_params_io.configure(command=self._get_io_object) 

    self._start()
    return


# Initialization
  def _start(self) -> None:
    self._update_module_view()
    self._update_worksheet_list()
    self._set_top_state()
    return

  def _update_module_view(self) -> None:   
    module_defs = self._converter.modulelist_to_module_defs(self._model.module)
    self._view.module_defs = module_defs
    return

  def _update_worksheet_list(self) -> None:
    names = self._model.flow.worksheetnames
    names.sort()
    names.insert(0, 'new <>')
    self._view.ws_names = names
    return


# Modules panel' events
  def _open_all(self, event) -> None:
    self._view.module.open_all()
    return

  def _module_tree_selection_changed(self, event) -> None:
    name = self._view.module.get_current_selection_tree()
    doc = ''
    if name != '':
      operation = self._model.module.get_operation_by_name(name)
      doc = operation._doc
    self._view.module.set_operation_doc(doc)
    return

# Flows panel's events
  def _worksheet_selected(self, event) -> None:
    ws_name = self._view.flow.names_combo_box.get()
    self._init_flow_model(ws_name)
    self._view.ws_title = self._model.flow.flow.info
    return


  def _init_flow_output_refs(self, names: List[str]) -> None:
    self._flow_output_refs: List[List[str]] = [[]]
    for i, name in enumerate(names):
      operation = self._model.module.get_operation_by_name(name)
      ref_names = [ref.get('name') for ref in operation.outrefs]
      refs = []
      for ref in operation.outrefs:
        rname = ref.get('name')
        out_ref = f'{i}-{name}-{rname}'
        refs.append(out_ref)
      self._flow_output_refs.append(refs)
    return

  # When a worksheet item is selected
  def _init_flow_model(self, ws_name: str) -> None:
    (ws_path, ws_name) = self._converter.split_ws_name(ws_name)
    # Create current flow model regarding ws defintion
    self._model.init_flow_model(ws_path, ws_name)
    names, titles = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names, titles)   
    self._update_flow_by_operations_params_def(names)
    # self._create_current_operation_params_controls(0, names[0])
    self._init_flow_output_refs(names) 
    # self._create_links_view(0, names[0])
    self._rebuild_runner()
    return

  def _unbind_params_widgets(self) -> None:
    widgets = self._view.params.get_active_param_widgets()
    for widget in widgets:
      t = type(widget) 
      if t == Scale: 
        widget.unbind("<ButtonRelease-1>")
      elif t == Spinbox:
        widget.unbind("<ButtonRelease-1>")
      elif t == Checkbutton:
        widget.configure(command=None)
      elif t == Combobox:
        widget.unbind("<<ComboboxSelected>>")
      elif t == Entry:
        widget.unbind("<Key>")
      else:
        pass
    return

  def _bind_params_widgets(self) -> None:
    widgets = self._view.params.get_active_param_widgets()
    for widget in widgets:
      t = type(widget) 
      if t == Scale: 
        widget.bind("<ButtonRelease-1>", self._apply)
      elif t == Spinbox:
        widget.bind("<ButtonRelease-1>", self._apply)
      elif t == Checkbutton:
        widget.configure(command=self._apply)
      elif t == Combobox:
        widget.bind("<<ComboboxSelected>>", self._apply)
      elif t == Entry:
        widget.bind("<Key>", self._key_pressed)
      else:
        pass
    return

  def _activate_params(self, idx: int = 0) -> None:
    self._unbind_params_widgets()
    self._view.params.set_active_wd(idx)
    self._bind_params_widgets()
    return

  def _tree_selection_changed(self, event) -> None:
    idx, name = self._view.flow.get_current_selection_tree()
    controls_idx = self._view.flow.get_current_opreation_params_idx()
    if self._model.flow.flow is not None and (controls_idx == -1 or controls_idx != idx):
      # self._create_current_operation_params_controls(idx, name)
      self._create_links_view(idx, name)
      self._activate_params(idx)
    return

  def _assign_oper_params(self, name: str, item: FlowItemModel) -> None:
    operation = self._model.module.get_operation_by_name(name)
    item.params_def = operation.params
    return

  def _update_flow_by_operations_params_def(self, names: List[str]) -> None:
    for idx, name in enumerate(names):
      item = self._model.flow.get_item(idx)
      self._assign_oper_params(name, item)
    return 


# Flows panel's commands 
  def _reload_ws_list(self, event) -> None:
    self._model.flow.reload()
    names = self._model.flow.worksheetnames
    names.insert(0, 'new <>')
    self._view.ws_names = names
    # self._view.ws_title = self._model.flow.flow.info
    if event is not None:
      # don't clear after store ws
      self._view.flow.clear_flow_tree_view()
      self._view.data.clear_view()
      self._view.ws_title = ''
      self._view.params.clear()
    return

  def _add_operation_to_flow_model(self) -> None:
    # Get destination item position before that will be added new one
    cur_idx, _ = self._view.flow.get_current_selection_tree()
    cur_idx = max(1, cur_idx)
    # Get source item position from modules view
    name = self._view.module.get_selected_item_name()   
    # Perform if operation only selected
    if name is not None:     
      new_flow_item = FlowItemModel(FlowItemType.EXEC, name)
      self._assign_oper_params(name, new_flow_item)
      self._model.flow.set_item(cur_idx, new_flow_item)
      names, titles = self._model.flow.get_names()
      self._view.flow.set_flow_item_names(names, titles)   
      self._init_flow_output_refs(names)
      self._rebuild_runner()
    return

  def _remove_operation_from_flow_model(self) -> None:
    cur_idx, _ = self._view.flow.get_current_selection_tree()
    if cur_idx == 0 or cur_idx == len(self._model.flow.items) -1:
      return
    self._model.flow.remove_item(cur_idx)
    names, titles = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names, titles)
    self._init_flow_output_refs(names)
    self._rebuild_runner()
    return

  def _reset_flow_model(self) -> None:
    ws_name = self._view.flow.names_combo_box.get()
    self._init_flow_model(ws_name)
    self._current()
    return

  def _store_flow_model_as_ws(self) -> None:
    flow_name = self._view.flow.names_combo_box.get()
    path, name = self._converter.flow.split_ws_name(flow_name)
    (new_path, stored_as) = self._model.flow.store_flow_model_as_ws(path, name)
    # TODO: implement change flow name and reload? 
    ws_name = f'{stored_as} <{new_path}>'
    self._reload_ws_list(None)
    self._view.flow.names_combo_box.set(ws_name)
    return

  def _edit_flow_links(self) -> None:
    self._view.flow.edit_flow_links(self._model.flow, self._update_flow)
    return

  def _update_flow(self) -> None:
    names, titles = self._model.flow.get_names()
    self._view.flow.set_flow_item_names(names, titles)   
    self._view.ws_title = self._model.flow.flow.info
    self._rebuild_runner()
    return 

  def _update_flow_item_params(self, idx: int) -> None:
    flow_item = self._model.flow.get_item(idx)
    params_new = self._view.params.get_active_params()
    for k in params_new.keys():
      flow_item.params[k] = params_new.get(k)
    return

# Execution commands
  def _preview_step_result(self, idx: int) -> None:
    state_id = self._runner.output_from_state
    self._view.data.preview_result(idx, state_id)
    return

  def _clear_step_result(self, idx: int) -> None:
    self._view.data.clear_preview(idx)
    return

  def _run(self) -> None:
    idx = self._runner.state_idx
    if self._ready():
      self._runner.run_all(self._model.flow.flow)
      idx = self._runner.state_idx
      self._view.flow.set_selection_tree(idx)
    return

  def _step(self, event_name: str) -> None:
    if self._ready():
      idx, _ = self._view.flow.get_current_selection_tree()
      self._update_flow_item_params(idx)
      self._runner.run_one(event_name, idx, self._model.flow.flow)
      new_idx = self._runner.state_idx
      self._view.flow.set_selection_tree(new_idx)
    return

  def _next(self)  -> int:
    self._view.data.default()
    idx, _ = self._view.flow.get_current_selection_tree()
    if self._ready() and self._runner.state_idx == idx:
      self._step('next')
      self._preview_step_result(idx)
    else:
      self._set_top_state()
    return 

  def _current(self) -> int:
    self._step('current')
    idx, _ = self._view.flow.get_current_selection_tree()
    self._preview_step_result(idx)
    return 

  def _prev(self) -> int:
    self._step('prev')
    idx = self._runner.state_idx
    self._clear_step_result(idx)
    return 

  def _top(self) -> None:
    self._set_top_state()
    return
  
  def _set_top_state(self) -> None:
    self._view.data.clear_view()
    self._view.flow.set_selection_tree()
    if self._ready():
      # self._view.flow.set_selection_tree()
      self._runner.reset()
    return

  def _run_current(self, idx: int) -> None:
    if self._ready() and self._runner.state_idx == idx:
      self._current()
    # else:
    #   self._set_top_state()
    return

# Links subpanel
  def _create_links_view(self, idx, name) -> None:
    self._unbind_links_widgets()
    flow_item = self._model.flow.get_item(idx)
    operation = self._model.module.get_operation_by_name(name)
    refs = operation.inrefs
    links = flow_item.links
    possible_refs = []
    last_idx = min(len(self._flow_output_refs)-1, idx+1)
    output_refs = self._flow_output_refs[:last_idx]
    for item_refs in output_refs:
      for ref in item_refs:
        possible_refs.append(ref)
    self._view.flow.create_links_view(refs, links, possible_refs)
    self._bind_links_widgets()
    return

  def _unbind_links_widgets(self) -> None:
    links_widgets = self._view.flow.links_widgets
    for lw in links_widgets:
      combo = lw.get('combo')
      combo.unbind("<<ComboboxSelected>>")
    return

  def _bind_links_widgets(self) -> None:
    links_widgets = self._view.flow.links_widgets
    for lw in links_widgets:
      combo = lw.get('combo')
      name = lw.get('name')
      getter = lw.get('getter')
      combo.bind("<<ComboboxSelected>>", lambda e: self._assign_link(name, getter))
    return

  def _assign_link(self, name: str, getter: Callable) -> None:
    cur_idx, flow_item_name = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(cur_idx)
    ext_ref = getter()
    flow_item.links[name] = ext_ref
    item_name = flow_item_name.split('.')[1]
    state_id = f'{cur_idx}-{item_name}'
    storage_in_ref = self._runner.storage.get_state_input_ext_ref(state_id, name)
    storage_in_ref.ext_ref = ext_ref
    self._apply()
    return

# Operation parameters sub panel's commands
  def _bind_param_controls(self, params_def) -> None:
    for param_def in params_def:
      cname = param_def.get('name')
      ctype = param_def.get('type')
      param_control = self._view.flow.get_current_operation_param_control(cname)
      t = type(param_control) 
      if t == Scale: 
        param_control.bind("<ButtonRelease-1>", self._apply)
      elif t == Spinbox:
        param_control.bind("<ButtonRelease-1>", self._apply)
      elif t == Checkbutton:
        param_control.configure(command=self._apply)
      elif t == Combobox:
        param_control.bind("<<ComboboxSelected>>", self._apply)
      elif t == Entry:
        param_control.bind("<Key>", self._key_pressed)
      else:
        pass
    return

  # def _create_current_operation_params_controls(self, idx, name) -> None:
  #   flow_item = self._model.flow.get_item(idx)
  #   params_def = flow_item.params_def
  #   # merge curent params and params_ws
  #   params = flow_item.params
  #   params_ws = flow_item.params_ws
  #   for k in params_ws.keys():
  #     if k in params:
  #       continue
  #     params[k] = params_ws.ket(k)
  #   self._view.flow.create_operation_params_controls(idx, name, params, copy.deepcopy(params_def))
  #   self._bind_param_controls(params_def)
  #   self._view.flow.btn_params_io['state'] = DISABLED
  #   path_in_def = [p for p in params_def if p.get('name') == 'path']
  #   if len(path_in_def) > 0:
  #     self._view.flow.btn_params_io['state'] = NORMAL
  #   return

  def _key_pressed(self, event) -> None:
    if event.keycode == 13:
      self._apply()
    return

  def _apply(self, event=None) -> None:
    idx, name = self._view.flow.get_current_selection_tree()
    self._run_current(idx)
    # Special treatment - activated via parameters view
    self._view.flow.btn_params_io['state'] = DISABLED
    return

  def _reset(self) -> None:
    idx, name = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def   
    params = copy.deepcopy(flow_item.params_ws)
    flow_item.params = params
    # self._view.flow.create_operation_params_controls(idx, name, params, copy.deepcopy(params_def))
    # self._bind_param_controls(params_def)

    self._run_current(idx)
    return

  def _default(self) -> None:
    idx, name = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def   
    params = self._converter.flow.convert_params_def_to_dict(flow_item.params_def)
    flow_item.params = params
    # self._view.flow.create_operation_params_controls(idx, name, params, copy.deepcopy(params_def))
    # self._bind_param_controls(params_def)

    self._run_current(idx)
    return

# Runner
  def _ready(self) -> bool:
    activate = self._runner.initialized and self._model.flow.loaded
    self._view.flow.activate_buttons(activate)
    return activate

  def _rebuild_runner(self) -> None:
    if self._model.flow:
      self._view.params.clear()
      self._view.params.build(self._model.flow.flow)
      self._activate_params()
      self._runner.build(self._model.flow.flow)
      # for plotting
      self._view.data.storage = self._runner.storage
    self._set_top_state()
    return


# Data commands
  @staticmethod
  def _set_image_location_to_params(io_obj: str, params: Dict, key: str) -> None:
    if '.' in io_obj: 
      path, name = os.path.split(io_obj)
    else:
      path = io_obj
      name = ''
    params['path'] = path
    if key == 'src':
      params['src'] = name
    else:
      params['dest'] = name
    return

  def _assign_location(self, idx: int, name: str, io_obj:str, key: str) -> None:
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def   
    params = flow_item.params

    p = [p for p in params_def if p.get('name') == 'path' or p.get('name') == 'src' or p.get('name') == 'dest']
    if p is not None:
      self._set_image_location_to_params(io_obj, params, key)
    # self._view.flow.create_operation_params_controls(idx, name, params, copy.deepcopy(params_def))
    # self._bind_param_controls(params_def)
    self._apply(None)
    return
  
  def _get_io_object(self) -> None:
    init_dir = self._cfg.input_paths
    idx, name = self._view.flow.get_current_selection_tree()
    flow_item = self._model.flow.get_item(idx)
    params_def = flow_item.params_def
    io_obj = ''
    full = False
    key = ''
    for p_def in params_def:
      key = p_def.get('name')
      if key == 'src' or key == 'dest':
        full = True
        break;
    if full and key == 'src':
      io_obj = self._get_full_file_name(init_dir)
    elif full and key == 'dest':
      io_obj = self._store_to(init_dir)
    else:
      io_obj = self._get_directory(init_dir)
    if io_obj != '':
      self._assign_location(idx, name, io_obj, key)
    return

  def _get_directory(self, init_dir: str) -> str:
    dir = askdirectory(initialdir=init_dir)
    return dir

  def _get_full_file_name(self, init_dir: str) -> str:
    ffn = askopenfilename(initialdir=init_dir, title="Select a file", filetypes=self._file_types)
    return ffn

  def _store_to(self, init_dir: str) -> str:
    ffn = asksaveasfilename(initialdir = init_dir, initialfile = '', defaultextension=".tiff", filetypes=self._file_types)
    return ffn

  @property
  def _file_types(self) -> str:
    return (("image files","*.png"), 
            ("image files","*.jpeg"), 
            ("image files","*.jpg"), 
            ("image files","*.tiff"), 
            ("json files","*.json"), 
            ("all files","*.*"))

import copy
from tkinter import *
from tkinter.ttk import Combobox
from typing import Dict, List, Tuple

import operation_loader

from flow_model.flowitemmodel import FlowItemModel
from flow_model.flowmodel import FlowModel
from tkscrolledframe import widget

from src.uiconst import *
from src.manager.models.flow.currentflowmodel import CurrentFlowModel


class ContentView(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 
    self._tmp_flow: FlowModel = None
    self._refs: List[Tuple] = []
    self._frames: List[Dict] = []

    self.grid()
    self.columnconfigure(0, weight=1)
    return

  @property
  def tmp_flow(self) -> FlowModel:
    return self._tmp_flow

  def init_content(self, flow: CurrentFlowModel) -> None:
    self._tmp_flow: FlowModel = copy.deepcopy(flow.flow)
    self._init_flow_refs()
    for i, item in enumerate(self._tmp_flow.items):
      item_frame = self._create_item_view(i, copy.copy(item))
      item_frame.grid(row=i, column=0, padx=PADX, pady=PADY, sticky=W+E)
      self._frames.append({'name': f'{i}-{item.name}', 'frame': item_frame})
    return 

  def _init_flow_refs(self) -> None:
    for i, item in enumerate(self._tmp_flow.items):
      func = operation_loader.get(item.name)
      (_, _, input_refs, output_refs) = operation_loader.parse_oper_doc(func.__doc__)
      irefs = []
      for inr in input_refs:
        irefs.append(f'{inr[0: inr.index(":")].strip()}')
      orefs = []
      oextrefs = []
      for outr in output_refs:
        oref = f'{outr[0: outr.index(":")].strip()}'
        orefs.append(oref)
        oextrefs.append(f'{i}-{item.name}-{oref}')
      self._refs.append((irefs, orefs, oextrefs))
    return

  def _get_external_refs(self, idx) -> List[str]:
    extrefs = []
    for i, trefs in enumerate(self._refs):
      (_,_,refs) = trefs
      for ref in refs:
        extrefs.append(ref)
      if i == idx-1:
        break
    return extrefs  

  def _create_item_view(self, idx: int, item: FlowItemModel) -> Frame:
    widget_idx = idx
    frame = LabelFrame(self)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    name_lbl = Label(frame, text=f'{idx}-{item.name}')
    name_lbl.grid(row=idx, column=0, sticky=W)
    
    title_var = StringVar()
    title_var.set(item.title)
    title_entry = Entry(frame, width=45, textvariable=title_var)
    title_entry.grid(row=idx, column=1, padx=PADX, sticky=W+E)

    self._create_input_view(frame, widget_idx, idx, item)
    # (input_refs, _, _) = self._refs[idx]
    # idx += len(input_refs)+1
    # self._create_output_view(frame, widget_idx, idx, item)
    return frame

  def _create_input_view(self, parent: LabelFrame, widget_idx: int, idx: int, item: FlowItemModel) -> None:
    (input_refs, _, _) = self._refs[idx]
    if len(input_refs) > 0:
      links = item.links
      for i, inref in enumerate(input_refs):
        inref_lbl = Label(parent, text=inref)
        inref_lbl.grid(row=widget_idx+1+i, column=0, padx=PADX*2, sticky=W)
        var = StringVar()
        inref_combo = Combobox(parent, name=inref, justify=LEFT, width=45)
        inref_combo['values'] = self._get_external_refs(idx)
        # Current value
        if len(links) > 0:
          link = links.get(inref)
          if link is not None:
            inref_combo.set(link)
            inref_combo.textvariable = var
        inref_combo.grid(row=widget_idx+1+i, column=1, padx=PADX, sticky=W+E)
    return

  def _create_output_view(self, parent: LabelFrame, widget_idx: int, idx: int, item: FlowItemModel) -> None:
    (input_refs, output_refs, _) = self._refs[idx]
    widget_idx += len(input_refs)+1
    if len(output_refs) > 0:
      output_lbl = Label(parent, text='output:')
      output_lbl.grid(row=widget_idx+1, column=0, padx=PADX, sticky=W)
      for i, outref in enumerate(output_refs):
        outref_lbl = Label(parent, text=outref)
        outref_lbl.grid(row=widget_idx+2+i, column=0, padx=PADX*2, sticky=W)
    return

  def update_flow(self) -> None:
    # iterate trough frames
    # iterate throuht a frame children
    # for child with type Entry:
    #  get name and value
    # set/update an link for the name 
    for frame in self._frames:
      frame_name = frame.get('name')
      idx = int(frame_name.split('-')[0])
      flow_item = copy.copy(self._tmp_flow.get_item(idx))
      frame_widget = frame.get('frame')
      children = frame_widget.winfo_children()
      for child in children:
        if type(child) == Combobox:
          link = child.get()
          if link != '':
            flow_item.links[child._name] = link
          elif len(flow_item.links) > 0 and flow_item.links.get(child._name, '') != '': 
            del(flow_item.links[child._name])
        elif type(child) == Entry:
          title = child.get()
          flow_item.title = title
        else:
          pass
      self._tmp_flow.replace_item(idx, copy.copy(flow_item))
    return
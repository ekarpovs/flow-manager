import copy
from tkinter import *
from typing import Dict, List

from flow_model.flowitemmodel import FlowItemModel
from flow_model.flowmodel import FlowModel

from ...uiconst import *
from src.manager.models.flow.currentflowmodel import CurrentFlowModel


class ContentView(Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 
    self._tmp_flow: FlowModel = None
    self._frames: List[Dict] = []

    self.grid()
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=2)
    return

  @property
  def tmp_flow(self) -> FlowModel:
    return self._tmp_flow

  def init_content(self, flow: CurrentFlowModel) -> None:
    self._tmp_flow: FlowModel = copy.deepcopy(flow.flow)
    for i, item in enumerate(self._tmp_flow.items):
      item_frame = self._create_item_view(i, item)
      item_frame.grid(row=i, column=0, sticky=W)
      self._frames.append({'name': f'{i}-{item.name}', 'frame': item_frame})
    return 

  def _create_item_view(self, idx, item: FlowItemModel) -> Frame:
    frame = Frame(self)
    name_lbl = Label(frame, text=f'{idx}-{item.name}')
    name_lbl.grid(row=idx, column=0, sticky=W)

    inrefs = item.inrefs_def
    if len(inrefs) > 0:
      input_lbl = Label(frame, text='input:')
      input_lbl.grid(row=idx+1, column=0, sticky=W)
      aliases = item.aliases
      for i, inref in enumerate(inrefs):
        iname = inref.get('name')
        inref_lbl = Label(frame, text=iname)
        inref_lbl.grid(row=idx+2+i, column=0, sticky=W)
        var = StringVar()
        if len(aliases) > 0:
          alias = aliases.get(iname)
          var.set(alias)
        inref_entry = Entry(frame, name=iname, textvariable=var, width=30)
        inref_entry.grid(row=idx+2+i, column=1, sticky=W)
    
    idx += len(inrefs)+1
    outrefs = item.outrefs_def
    if len(outrefs) > 0:
      output_lbl = Label(frame, text='output:')
      output_lbl.grid(row=idx+1, column=0, sticky=W)
      outrefs = item.outrefs_def   
      for i, outref in enumerate(outrefs):
        outref_lbl = Label(frame, text=outref.get('name'))
        outref_lbl.grid(row=idx+2+i, column=0, sticky=W)
    return frame

  def update_flow(self) -> None:
    # iterate trough frames
    # iterate throuht a frame children
    # for child with type Entry:
    #  get name and value
    # set/update an alias for the name 
    for frame in self._frames:
      frame_name = frame.get('name')
      idx = int(frame_name.split('-')[0])
      frame_widget = frame.get('frame')
      children = frame_widget.winfo_children()
      for child in children:
        if type(child) == Entry:
          flow_item = self._tmp_flow.get_item(idx)
          flow_item.aliases[child._name] = child.get()
          # print(child._name, child.get())
    return
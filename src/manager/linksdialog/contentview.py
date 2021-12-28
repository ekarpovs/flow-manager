import copy
from tkinter import *
from tkinter.ttk import Combobox
from typing import Dict, List

from flow_model.flowitemmodel import FlowItemModel
from flow_model.flowmodel import FlowModel

from src.uiconst import *
from src.manager.models.flow.currentflowmodel import CurrentFlowModel


class ContentView(LabelFrame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 
    self._tmp_flow: FlowModel = None
    # self._out_link_names: List[str] = []
    self._frames: List[Dict] = []

    self.grid()
    self.columnconfigure(0, weight=1)
    return

  @property
  def tmp_flow(self) -> FlowModel:
    return self._tmp_flow

  def init_content(self, flow: CurrentFlowModel) -> None:
    self._tmp_flow: FlowModel = copy.deepcopy(flow.flow)
    for i, item in enumerate(self._tmp_flow.items):
      item_frame = self._create_item_view(i, item)
      item_frame.grid(row=i, column=0, padx=PADX, pady=PADY, sticky=W+E)
      self._frames.append({'name': f'{i}-{item.name}', 'frame': item_frame})
    return 

  def _create_out_link_names_list(self, idx: int) -> List[str]:
    out_link_names: List[str] = []
    for i, item in enumerate(self._tmp_flow.items):
      if i >= idx: 
        break
      for outref in item.outrefs_def:
        outref_name = outref.get('name')
        out_link_names.append(f'{i}-{item.name}-{outref_name}')
    return out_link_names 

  def _create_item_view(self, idx: int, item: FlowItemModel) -> Frame:
    frame = LabelFrame(self)
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)
    name_lbl = Label(frame, text=f'{idx}-{item.name}')
    name_lbl.grid(row=idx, column=0, sticky=W)
    self._create_input_view(frame, idx, item)
    idx += len(item.inrefs_def)+1
    self._create_output_view(frame, idx, item)
    return frame

  def _create_input_view(self, parent: LabelFrame, idx: int, item: FlowItemModel) -> None:
    out_link_names = self._create_out_link_names_list(idx)
    inrefs = item.inrefs_def
    if len(inrefs) > 0:
      input_lbl = Label(parent, text='input:')
      input_lbl.grid(row=idx+1, column=0, padx=PADX, sticky=W)
      links = item.links
      for i, inref in enumerate(inrefs):
        iname = inref.get('name')
        inref_lbl = Label(parent, text=iname)
        inref_lbl.grid(row=idx+2+i, column=0, padx=PADX*2, sticky=W)
        var = StringVar()
        inref_combo = Combobox(parent, name=iname, justify=LEFT, width=30)
        inref_combo['values'] = out_link_names
        # Current value
        if len(links) > 0:
          link = links.get(iname)
          if link is not None:
            inref_combo.set(link)
            inref_combo.textvariable = var
        inref_combo.grid(row=idx+2+i, column=1, padx=PADX, sticky=E)
    return

  def _create_output_view(self, parent: LabelFrame, idx: int, item: FlowItemModel) -> None:
    outrefs = item.outrefs_def
    if len(outrefs) > 0:
      output_lbl = Label(parent, text='output:')
      output_lbl.grid(row=idx+1, column=0, padx=PADX, sticky=W)
      outrefs = item.outrefs_def   
      for i, outref in enumerate(outrefs):
        outref_lbl = Label(parent, text=outref.get('name'))
        outref_lbl.grid(row=idx+2+i, column=0, padx=PADX*2, sticky=W)
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
      frame_widget = frame.get('frame')
      children = frame_widget.winfo_children()
      for child in children:
        if type(child) == Combobox:
          flow_item = self._tmp_flow.get_item(idx)
          link = child.get()
          if link is not '':
            flow_item.links[child._name] = link
          elif len(flow_item.links) > 0 and flow_item.links.get(child._name, '') is not '': 
            del(flow_item.links[child._name])
          # print(child._name, child.get())
    return
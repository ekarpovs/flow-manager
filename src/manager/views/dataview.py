import cv2
import numpy as np 
from typing import List, Dict, Tuple, Callable
from tkinter import *
from tkinter.ttk import Button 
from tkscrolledframe import ScrolledFrame
from PIL import Image, ImageTk

from flow_storage import *

from ...uiconst import *
from .view import View
from .plotdialog import PlotDialog 

class DataView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self['text'] = 'Data'
    # self['bg'] = 'green'

    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_reqwidth()
    self.grid()
    # self.grid_propagate(False)

    self.rowconfigure(0, weight=20)
    self.rowconfigure(1, weight=1)
    # self.columnconfigure(0, pad=15)
    self.columnconfigure(0, weight=1)

    # Content will be scrolable
    self.content = ScrolledFrame(self)
    # Bind the arrow keys and scroll wheel
    self.content.bind_arrow_keys(self)
    self.content.bind_scroll_wheel(self)
    # Create the preview frame within the ScrolledFrame
    self.preview_view = self.content.display_widget(Frame)
    self.content.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + E + N + S)
    
    self.data_actions = Frame(self, highlightbackground='gray', highlightthickness=1)
    self.data_actions.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=W + E + S)
    self.data_actions.columnconfigure(0, weight=2)
    self.data_actions.columnconfigure(1, weight=2)
    self.data_actions.columnconfigure(2, weight=1)
    
    self.preview_height = 150
    self.preview_width = 150

    var_h = IntVar()
    var_h.set(self.preview_height)
    self.scale_h = Scale(self.data_actions, from_=50, to=500, resolution=50, variable=var_h, orient=HORIZONTAL)
    self.scale_h.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W+E)
    self.scale_h.bind("<ButtonRelease-1>", self._set_h)

    self.btn_save = Button(self.data_actions, text='Save', width=BTNW, command=self._save)
    self.btn_save.grid(row=0, column=2, padx=PADX, pady=PADY, sticky=E)
    
    self._out = None
    self._grid_rows: List[Widget] = []
    self._storage: FlowStorage = None
    return

  @property
  def storage(self) -> FlowStorage:
    return self._storage
  
  @storage.setter
  def storage(self, storage) -> None:
    self._storage = storage
    return


  def clear_view(self) -> None:
    self._out = None
    for row in self._grid_rows:
      row.grid_remove()  
    self._grid_rows.clear()
    return

  def _preview_size(self, image):
    (h, w) = image.shape[:2]
    ratio = w/h
    if h > self.preview_height:
      h = self.preview_height
      w = int(h*ratio)
    elif w > self.preview_width:    
      w = self.preview_width
      h = int(w/ratio)
    self.h = h
    self.w = w
    return

  def _fit_image(self, image):
    self._preview_size(image)   
    dim = (self.w, self.h)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return image

  def _preview_view(self, parent, data: Dict, name: str) -> Widget:
    preview = self._fit_image(data)
    pil_image = Image.fromarray(preview)
    photo = ImageTk.PhotoImage(pil_image)
    view = Label(parent, name=name, image=photo)
    view.image = photo   
    return view

  def _object_view(self, parent, data: Dict, name: str) -> Widget:
    view = Label(parent, name=name, border=1)
    # text = json.dumps(data, indent = 3)
    # df = pd.DataFrame(data)
    view.config(text = data)
    return view

  def _get_view(self, ref_type: str) -> Callable:
    views = {
      FlowDataType.NP_ARRAY: self._preview_view
    }
    return views.get(ref_type, self._object_view)

  def clear_preview(self, idx: int) -> None:
    if len(self._grid_rows) > 0:
      self._out = None
      # self._grid_rows.pop(idx).grid_remove()
      try:
        # remove existing item with the idx
        res = self._grid_rows.pop(idx)
        res.grid_remove()
      except IndexError:
        pass
    return

  def _calc_row_idx(self, row_idx: str) -> int:
    if len(self._grid_rows) == 0:
      return 0
    name = f'--{row_idx}--'
    for i,row in enumerate(self._grid_rows):
      if row._name == name:
        return i
    return i+1  
  
  def _create_row_output_container(self, row_idx: int, title: str) -> Widget:
    state_frame = LabelFrame(self.preview_view, name=f'--{row_idx}--', text=title)
    state_frame.rowconfigure(0, pad=15)
    state_frame.columnconfigure(0, weight=1)
    state_frame.columnconfigure(0, pad=15)
    state_frame.columnconfigure(1, weight=1)
    state_frame.columnconfigure(1, pad=15)
    state_frame.grid(row=row_idx, column=0, sticky=W)
    return state_frame

  def _create_preview(self, row_idx, title, out_data, out_refs) -> None:
    preview_frame = self._create_row_output_container(row_idx, title)
    # previews for a state outputs 
    for i, ref in enumerate(out_refs):
      (ref_extr, ref_intr, ref_type) = ref
      data = out_data.get(ref_intr)
      if data is None:
        continue
      view = self._get_view(ref_type)
      # convert to a conventional format (without '.')
      name = ref_extr.replace('.', '-')
      widget = view(preview_frame, data, name)
      widget.grid(row=0, column=i)
      widget.bind('<Button-1>', self._on_click)
    try:
      # remove existing item with the row_idx
      self._grid_rows.pop(row_idx)
    except IndexError:
      pass
    # set new one
    self._grid_rows.insert(row_idx, preview_frame)
    return

  def _preview(self) -> None:
    if self._out is None:
      return
    (out_refs, out_data) = self._out
    if len(out_refs) > 0:
      parts =out_refs[0][0].split('-')
      title = '-'.join(parts[0:len(parts)-1])
      row_idx = self._calc_row_idx(parts[0])
      self._create_preview(row_idx, title, out_data, out_refs)
    return

  def set_preview(self, out: Tuple[List[Tuple[str, FlowDataType]], Dict] = None) -> None:
    self._out = out
    self._preview()
    return
  def _on_click(self, event) -> None:
    event.widget.focus_set()
    active_widget_name = event.widget._name
    print(active_widget_name)
    for row in self._grid_rows:
      for child in row.children:
        if child == active_widget_name:
          self._plot(child)
    return

  def _plot(self, name: str) -> None:
    parts = name.split('-')
    state_id = parts[0] + '-' + parts[2]
    key = parts[3]
    data_dict = self._storage.get_state_output_data(state_id)
    data = data_dict.get(key)
    plot_dlg = PlotDialog(self, name, data)
    return

  def _set_h(self, event) -> None:
    self.preview_height = self.scale_h.get()
    self._preview()
    return

  def _save(self) -> None:
    print('save')
    return
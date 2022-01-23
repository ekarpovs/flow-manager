from re import I
from typing import List, Dict, Tuple, Callable
from tkinter import *
from tkscrolledframe import ScrolledFrame
import cv2
from PIL import Image, ImageTk

from flow_storage import *

from ...uiconst import *
from .view import View
from .plotdialog import PlotDialog 

class DataView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self['text'] = 'Data'
   
    self.grid()
    self.grid_propagate(False)

    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, pad=15)
    self.columnconfigure(0, weight=1)

    # Content will be scrolable
    self.content = ScrolledFrame(self)
    # Bind the arrow keys and scroll wheel
    self.content.bind_arrow_keys(self)
    self.content.bind_scroll_wheel(self)
    # Create the Thumbnail frame within the ScrolledFrame
    self.thumbnail_view = self.content.display_widget(Frame)
    self.content.grid(row=0, column=0, sticky=W + E + N + S)
    
    self.thumbnail_height = 150
    self.thumbnail_width = 150

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
    for row in self._grid_rows:
      row.grid_remove()  
    self._grid_rows.clear()
    return

  def _thumbnail_size(self, image):
    (h, w) = image.shape[:2]
    ratio = w/h
    if h > self.thumbnail_height:
      h = self.thumbnail_height
      w = int(h*ratio)
    elif w > self.thumbnail_width:    
      w = self.thumbnail_width
      h = int(w/ratio)
    self.h = h
    self.w = w
    return

  def _thumbnail(self, image):
    self._thumbnail_size(image)   
    dim = (self.w, self.h)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return image

  def _thumbnail_view(self, parent, data: Dict, name: str) -> Widget:
    thumbnail = self._thumbnail(data)
    pil_image = Image.fromarray(thumbnail)
    photo = ImageTk.PhotoImage(pil_image)
    view = Label(parent, name=name, image=photo)
    view.image = photo   
    return view

  def _object_view(self, parent, data: Dict, name: str) -> Widget:
    view = Label(parent, name=name, border=1)
    view.config(text = data)
    return view

  def _get_view(self, ref_type: str) -> Callable:
    views = {
      FlowDataType.NP_ARRAY: self._thumbnail_view
    }
    return views.get(ref_type, self._object_view)

  def clear_step_result(self, idx: int) -> None:
    num_of_widgets = len(self._grid_rows)
    if num_of_widgets > 0 and (idx < num_of_widgets):
      self._grid_rows.pop().grid_remove()
    return

  def _calc_row_idx(self, row_idx: str) -> int:
    if len(self._grid_rows) == 0:
      return 0
    name = f'--{row_idx}--'
    for i,row in enumerate(self._grid_rows):
      if row._name == name:
        return i
    return i+1  
  

  def set_step_result(self, idx: int, out: Tuple[List[Tuple[str, FlowDataType]], Dict] = None) -> None:
    if out is None:
      return
    (out_refs, out_data) = out
    if len(out_refs) > 0:
      parts =out_refs[0][0].split('-')
      title = '-'.join(parts[0:len(parts)-1])
      row_idx = self._calc_row_idx(parts[0])
      # container for a step outputs:
      state_frame = LabelFrame(self.thumbnail_view, name=f'--{row_idx}--', text=title)
      state_frame.rowconfigure(0, pad=15)
      state_frame.columnconfigure(0, weight=1)
      state_frame.columnconfigure(0, pad=15)
      state_frame.columnconfigure(1, weight=1)
      state_frame.columnconfigure(1, pad=15)
      state_frame.grid(row=row_idx, column=0, sticky=W)
      # previews for a step outputs 
      for ref in out_refs:
        (ref_extr, ref_intr, ref_type) = ref
        data = out_data.get(ref_intr)
        view = self._get_view(ref_type)
        # convert to conventional format (without '.')
        name = ref_extr.replace('.', '-')
        widget = view(state_frame, data, name)
        widget.grid(row=0, column=ref_type)
        widget.bind('<Button-1>', self._on_click)
      # remove existing item with the row_idx
      try:
        self._grid_rows.pop(row_idx)
      except IndexError:
        pass
      self._grid_rows.insert(row_idx, state_frame)
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
    data = self._storage.get_state_output_data(state_id)   
    plot_dlg = PlotDialog(self, name, data.get(key))
    return
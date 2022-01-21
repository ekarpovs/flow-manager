from re import I
from typing import List, Dict, Tuple, Callable
from tkinter import *
import cv2
from PIL import Image, ImageTk
# import matplotlib
# import numpy as np

# matplotlib.use("agg")
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# import matplotlib.pyplot as plt

from ...uiconst import *
from .view import View
from flow_storage import FlowDataType

class DataView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 
    self['text'] = 'Data'
   
    self.grid()

    self.panel_height = 100
    self.panel_width = 300

    self._grid_rows: List[Widget] = []
    return

  def clear_view(self) -> None:
    for row in self._grid_rows:
      row.grid_remove()  
    self._grid_rows.clear()
    return

  def _calculate_new_size(self, image):
    (h, w) = image.shape[:2]
    ratio = w/h
    if h > self.panel_height:
      h = self.panel_height
      w = int(h*ratio)
    elif w > self.panel_width:    
      w = self.panel_width
      h = int(w/ratio)   
    self.h = h
    self.w = w
    return

  def _fit_image_to_view(self, image):
    self._calculate_new_size(image)   
    dim = (self.w, self.h)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return image

  def _image_view(self, parent, data: Dict, ref_extr: str) -> Widget:
    data = self._fit_image_to_view(data)
    image = Image.fromarray(data)
    photo = ImageTk.PhotoImage(image)
    view = Label(parent, name='clickable-image', image=photo)
    view.image = photo   
    return view

  def _object_view(self, parent, data: Dict, ref_extr: str) -> Widget:
    view = Label(parent, name='clickable-object', border=1)
    view.config(text = data)
    return view

  def _get_view(self, ref_type: str) -> Callable:
    views = {
      FlowDataType.NP_ARRAY: self._image_view
    }
    return views.get(ref_type, self._object_view)

  def clear_step_result(self, idx: int) -> None:
    num_of_widgets = len(self._grid_rows)
    if num_of_widgets > 0 and (idx < num_of_widgets):
      self._grid_rows.pop().grid_remove()
    return

  def set_step_result(self, idx: int, out: Tuple[List[Tuple[str, FlowDataType]], Dict] = None) -> None:
    if out is None:
      return
    (out_refs, out_data) = out
    if len(out_refs) > 0:
      frame = Frame(self, name=f'{idx-1}-output-frame', highlightbackground="blue", highlightthickness=5)
      frame.grid(row=idx-1, column=0, sticky=W)
      frame.columnconfigure(0, weight=1)
      frame.columnconfigure(1, weight=1)

      for ref in out_refs:
        (ref_extr, ref_intr, ref_type) = ref
        data = out_data.get(ref_intr)
        view = self._get_view(ref_type)
        widget = view(frame, data, ref_extr)
        widget.grid(row=0, column=ref_type, sticky=W)
        widget.bind('<Button-1>', self.on_click)
      self._grid_rows.insert(idx-1, frame)
    return


  def on_click(self, event) -> None:
    event.widget.focus_set()
    return print(event.widget)
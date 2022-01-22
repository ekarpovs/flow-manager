from re import I
from typing import List, Dict, Tuple, Callable
from tkinter import *
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

    self.panel_height = 100
    self.panel_width = 300

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

  def _image_view(self, parent, data: Dict, name: str) -> Widget:
    data = self._fit_image_to_view(data)
    image = Image.fromarray(data)
    photo = ImageTk.PhotoImage(image)
    view = Label(parent, name=name, image=photo)
    view.image = photo   
    return view

  def _object_view(self, parent, data: Dict, name: str) -> Widget:
    view = Label(parent, name=name, border=1)
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
    i = max(idx-1, 0)
    (out_refs, out_data) = out
    if len(out_refs) > 0:
      # container for a step outputs:
      frame = Frame(self, name=f'--{i}--', highlightbackground="blue", highlightthickness=5)
      frame.grid(row=i, column=0, sticky=W)
      frame.columnconfigure(0, weight=1)
      frame.columnconfigure(1, weight=1)
      # previews for a step outputs 
      for ref in out_refs:
        (ref_extr, ref_intr, ref_type) = ref
        data = out_data.get(ref_intr)
        view = self._get_view(ref_type)
        # convert to conventional format (without '.')
        name = ref_extr.replace('.', '-')
        widget = view(frame, data, name)
        widget.grid(row=0, column=ref_type, sticky=W)
        widget.bind('<Button-1>', self._on_click)
      self._grid_rows.insert(i, frame)
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
    data = self._storage.get_state_output_data(state_id)   
    plot_dlg = PlotDialog(self, name, data.get(parts[3]))
    return
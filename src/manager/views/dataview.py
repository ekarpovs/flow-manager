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
    self.grid_propagate(False)

    self.rowconfigure(0, weight=20)
    # self.rowconfigure(1, weight=1)
    # self.rowconfigure(1, minsize=20)
    self.columnconfigure(0, minsize=800)
    self.columnconfigure(0, pad=15)

    # self.thumbnails_farme = LabelFrame(self, name='thumbnails', text='Thumbnails',highlightbackground="green", highlightthickness=5)
    self.thumbnails_farme = LabelFrame(self, name='thumbnails', text='Thumbnails')
    self.thumbnails_farme.grid(row=0, column=0, sticky=W + E + N + S)
    
    # self.controls_frame = Frame(self, name='controls', highlightbackground="red", highlightthickness=5)
    # self.controls_frame.grid(row=1, column=0, sticky=W + E + N + S)

    # scale_var_x = IntVar()
    # scale_var_x.set(100)
    # self.thumbnails_x = Scale(self, from_=100, to=300, resolution=10, variable=scale_var_x, length=200, orient=HORIZONTAL)
    # self.thumbnails_x.grid(row=1, column=0, sticky=W)

    self.thumbnail_height = 100
    self.thumbnail_width = 300

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

  def _image_view(self, parent, data: Dict, name: str) -> Widget:
    data = self._thumbnail(data)
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
      parts =out_refs[0][0].split('-')
      title = '-'.join(parts[0:len(parts)-1])
      # container for a step outputs:
      # state_frame = LabelFrame(self.thumbnails_farme, name=f'--{i}--', text=title, highlightbackground="blue", highlightthickness=2)
      state_frame = LabelFrame(self.thumbnails_farme, name=f'--{i}--', text=title)
      state_frame.rowconfigure(0, pad=15)
      state_frame.columnconfigure(0, weight=1)
      state_frame.columnconfigure(0, pad=15)
      state_frame.columnconfigure(1, weight=1)
      state_frame.columnconfigure(1, pad=15)
      state_frame.grid(row=i, column=0, sticky=W)
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
      self._grid_rows.insert(i, state_frame)
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
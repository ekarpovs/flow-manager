from ctypes import alignment
import cv2
import numpy as np 
from typing import List, Dict, Tuple, Callable
from tkinter import *
from tkinter.ttk import Button 
from tkinter import font
from tkscrolledframe import ScrolledFrame
from PIL import Image, ImageTk

from flow_storage import FlowStorage, FlowDataType

from ....uiconst import *
from ..view import View
from .plotdialog import PlotDialog 

DEFAULT_PREVIEW_SIZE = 100
WITHOUT_PREVIEW_DATA = -1
DEFAULT_VIEW_SIZE = 500


class DataView(View):
  def __init__(self, parent):
    super().__init__(parent)
    # self['bg'] = 'green'
    self['text'] = 'Data'

    # setup the module view geometry
    h = self._manager_container_h
    w = int(self._manager_container_w/2.92)
    self['height'] = h
    self['width'] = w
    # do not resize the module frame after a widget will be added
    self.grid_propagate(False)

    self.grid()
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)

    # Last existing output
    self._data_active = Frame(self, height=int(h*0.5), highlightbackground='gray', highlightthickness=1)
    self._data_active.grid(row=0, column=0, padx=PADX, pady=PADY_S, sticky=W + E + N + S)
    self._data_active.columnconfigure(0, weight=1)
    self._data_active.columnconfigure(1, weight=1)
    self._data_active.rowconfigure(0, weight=1)
    self._data_active.grid_propagate(False)

    # Preview content will be scrolable
    self.content = ScrolledFrame(self, height=int(h*0.2), use_ttk=True)
    self.content.grid(row=1, column=0, padx=PADX, pady=PADY_S, sticky=W + E + N + S)
    # Create the preview frame within the ScrolledFrame
    self.preview_view = self.content.display_widget(Frame)
   
    self._preview_height = DEFAULT_PREVIEW_SIZE
    self._preview_width = DEFAULT_PREVIEW_SIZE
    self._out = None
    self._idx_map :Dict = {}
    self._grid_rows: List[Widget] = []
    self._storage: FlowStorage = None
    self._active_view = None
    self._active_view_info = None
    return

# API
  @property
  def storage(self) -> FlowStorage:
    return self._storage
  
  @storage.setter
  def storage(self, storage) -> None:
    self._storage = storage
    return

  def clear_view(self) -> None:
    self._out = None
    self._idx_map = {}

    self._clear_active_view()
    self._clear_all_preview()
    return

  def _clear_active_view(self) -> None:
    if self._active_view is not None:
      for child in self._active_view.winfo_children():
        child.grid_remove()
      self._active_view.grid_remove()
    return

  def _clear_all_preview(self) -> None:
    for row in self._grid_rows:
      row.grid_remove()  
    self._grid_rows.clear()
    self.content.scroll_to_top()
    return

  def default(self) -> None:
    self._preview_height = DEFAULT_PREVIEW_SIZE
    self._preview_width = DEFAULT_PREVIEW_SIZE
    self._preview() 
    return

  def update_result(self, idx: int, state_id: str) -> None:
    self._show_active(state_id)
    self. _clear_preview(idx)
    return

  def show_result(self, state_id: str) -> None:
    self._show_active(state_id)
    return

  def show_preview_result(self, state_id: str, idx: int) -> None:
    self._show_preview(state_id, idx)
    self._show_active(state_id)
    return

  # Locals
  # Preview results
  def _preview(self) -> None:   
    if self._out is None:
      return
    (out_refs, out_data) = self._out
    if len(out_refs) > 0:
      state_id, title = self._parse_out_refs(out_refs)
      row_idx = self._get_row_idx(state_id)
      self._create_preview(row_idx, title, out_data, out_refs)
    return

  def _map_idx_to_row_idx(self, idx: int) -> None:
    preview_row = len(self._idx_map)
    (out_refs, out_data) = self._out
    if len(out_refs) == 0 and len(out_data) == 0:
      # No data for preview
      self._idx_map[f'{idx}'] = WITHOUT_PREVIEW_DATA
      return
    # map idx to row_idx
    self._idx_map[f'{idx}'] = min(idx, preview_row)
    return

  def _show_preview(self, state_id: str, idx: int) -> None:
    out_data = self._storage.get_state_output_data(state_id)
    refs = self._storage.get_state_output_refs(state_id)
    if out_data is None or refs is None:
      return
    out_refs = [(ref.ext_ref, ref.int_ref, ref.data_type) for ref in refs]  
    self._out = (out_refs, out_data)
    self._map_idx_to_row_idx(idx)
    self._preview()
    return

  def _preview_size(self, image) -> Tuple[int,int]:
    (h, w) = image.shape[:2]
    ratio = w/h
    if h > self._preview_height:
      h = self._preview_height
      w = int(h*ratio)
    elif w > self._preview_width:    
      w = self._preview_width
      h = int(w/ratio)
    elif h < self._preview_height and w < self._preview_width:
      h = self._preview_height
      w = int(h*ratio)
    else:
      pass
    return (w, h)

  def _fit_image_for_preview(self, image):  
    dim = self._preview_size(image)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_NEAREST)
    return image

  def _preview_image_list(self, parent, image: List[np.ndarray], name: str) -> Widget:
    image = cv2.hconcat(image)
    return self._preview_image(parent, image, name)

  def _preview_image(self, parent, image: np.ndarray, name: str) -> Widget:
    preview = self._fit_image_for_preview(image)
    pil_image = Image.fromarray(preview)
    photo = ImageTk.PhotoImage(pil_image)
    view = Label(parent, name=name, image=photo)
    view.image = photo
    return view

  def _clear_preview(self, idx: int) -> None:
    if len(self._grid_rows) > 0:
      self._out = None
      # map idx to preview idx
      row_idx = self._get_row_idx(f'{idx}')
      if row_idx == WITHOUT_PREVIEW_DATA:
        return
      row_idx = max(len(self._idx_map)-1, self._get_row_idx(f'{idx}'))
      try:
        # remove idx mapping for the idx
        if f'{row_idx}' in self._idx_map:
          self._idx_map.pop(f'{row_idx}')
        # remove existing preview item with the idx
        res = self._grid_rows.pop(row_idx, )
        res.grid_remove()
      except IndexError:
        pass
    return
  
  def _create_row_output_container(self, row_idx: int, title: str) -> Widget:
    state_frame = LabelFrame(self.preview_view, name=f'--{row_idx}--', text=title)
    state_frame.grid(row=row_idx, column=0, sticky=W+E)
    state_frame.rowconfigure(0, pad=15)
    state_frame.columnconfigure(0, weight=1)
    state_frame.columnconfigure(0, pad=15)
    # state_frame.columnconfigure(1, weight=1)
    # state_frame.columnconfigure(1, pad=15)
    return state_frame

  def _create_preview(self, row_idx, title, out_data, out_refs) -> None:
    preview_frame = self._create_row_output_container(row_idx, title)
    # previews for a state outputs 
    for i, ref in enumerate(out_refs):
      (ref_extr, ref_intr, ref_type) = ref
      data = out_data.get(ref_intr)
      if data is None:
        continue
      t = type(data)
      if t == np.ndarray:
        if data.dtype == np.dtype('uint8'):
          # convert to a conventional format (without '.')
          name = ref_extr.replace('.', '-')
          widget = self._preview_image(preview_frame, data, name)
          widget.grid(row=0, column=0, sticky=W)
          widget.bind('<Button-1>', self._on_click)
    try:
      # remove existing item with the row_idx
      self._grid_rows.pop(row_idx)
    except IndexError:
      pass
    # set new one
    self._grid_rows.insert(row_idx, preview_frame)

    # Scroll view if need
    self.update_idletasks()
    h = preview_frame.winfo_height()
    self.content.focus_set()
    self.content.yview(SCROLL, h, UNITS)
    return

  def _get_row_idx(self, state_id: str) -> int:
    row_idx = self._idx_map.get(state_id, WITHOUT_PREVIEW_DATA)
    return row_idx

  @staticmethod
  def _parse_out_refs(refs) -> Tuple[str, str]:
    parts =refs[0][0].split('-')
    state_id = parts[0]
    title = '-'.join(parts[0:len(parts)-1])
    return state_id, title

# Show active result
  def _show_active(self, state_id: str) -> None:
    out_data = self._storage.get_state_output_data(state_id)
    refs = self._storage.get_state_output_refs(state_id)
    if out_data is None or refs is None:
      return
    out_refs = [(ref.ext_ref, ref.int_ref, ref.data_type) for ref in refs]  
    if len(out_refs) > 0:
      ref = out_refs[0]
      (ref_extr, ref_intr, ref_type) = ref
      data = out_data.get(ref_intr)
      t = type(data)
      if t == np.ndarray:
        if data.dtype == np.dtype('uint8'):
          self._active_view = Frame(self._data_active, name='active data')
          self._active_view.rowconfigure(0, weight=1)
          self._active_view.rowconfigure(1, weight=1)
          self._active_view.rowconfigure(2, weight=1)
          self._active_view.rowconfigure(3, weight=1)
          self._create_active_title(ref_extr)
          self._create_active_image(data)
          self._create_active_info(data)
          self._active_view.grid(row=0, column=0, padx=PADX_S, pady=PADY_S, sticky=W + E + N + S)
        else:
          if self._active_view is not None:
            self._active_view.grid_remove()
      else:
        self._active_view = Label(self._data_active, name='active data', text = data)
        self._active_view.grid(row=0, column=0, padx=PADX_S, pady=PADY_S, sticky=W + E + N + S)
    else:
      if self._active_view is not None:
        self._active_view.grid_remove()
    return

  def _create_active_title(self, title:str) -> None:
    active_view_title = Label(self._active_view, anchor=NW, justify='left',name='active view title', text = title)
    active_view_title.grid(row=0, column=0, padx=PADX_S, pady=PADY_S, sticky=W + E + N + S)
    return

  def _create_active_image(self, data: np.ndarray) -> None:   
    scrollbar_x = Scrollbar(self._active_view, orient=HORIZONTAL)
    scrollbar_x.grid(row=2, column=0, columnspan=2, sticky=W + E)

    scrollbar_y = Scrollbar(self._active_view, orient=VERTICAL)
    scrollbar_y.grid(row=1, column=1, sticky=N + S)

    pil_image = Image.fromarray(data)
    photo = ImageTk.PhotoImage(pil_image)
    active_view_canvas = Canvas(self._active_view, width = DEFAULT_VIEW_SIZE, height = DEFAULT_VIEW_SIZE, name='active view canvas')
    active_view_canvas.grid(row=1, column=0, padx=PADX_S, pady=PADY_S, sticky=W + E + N + S)
    active_view_canvas.create_image((0, 0), anchor=NW, image=photo)
    active_view_canvas.image = photo
    # set the scrollbars to the canvas
    active_view_canvas.config( xscrollcommand=scrollbar_x.set)    
    active_view_canvas.config( yscrollcommand=scrollbar_y.set)    
    # set canvas view to the scrollbars
    scrollbar_x.config(command = active_view_canvas.xview)
    scrollbar_y.config(command = active_view_canvas.yview)
    # assign the region to be scrolled 
    active_view_canvas.config(scrollregion=active_view_canvas.bbox(ALL))
    return

  def _create_active_info(self, data: np.ndarray) -> None:
    (h, w) = data.shape[:2]
    text = f'width = {w}, height = {h}'
    active_view_info = Label(self._active_view, anchor=NW, justify='left',name='active view info', text = text)
    active_view_info.grid(row=3, column=0, padx=PADX_S, pady=PADY_S, sticky=W + E + N + S)
    return


# Plot
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


  # TODO:
  # https://stackoverflow.com/questions/28005591/how-to-create-a-scrollable-canvas-that-scrolls-without-a-scroll-bar-in-python
  def _move(self, preview_frame):
    deltay = self._preview_height
    deltax = self._preview_width
    # make sure we don't move beyond our scrollable region
    (x0,y0,x1,y1) = self.content._canvas.coords()
    deltay = 0 if (deltay > 0 and y1 >= 400) else deltay
    deltay = 0 if (deltay < 0 and y0 <= -400) else deltay
    deltax = 0 if (deltax > 0 and x1 >= 400) else deltax
    deltax = 0 if (deltax < 0 and x0 <= -400) else deltax

    # move the item, then scroll it into view
    self.content._canvas.move(preview_frame, deltax, deltay)
    self._make_visible(preview_frame)    

  def _make_visible(self, preview_frame) -> None:
    # determine the bounding box of the visible area of the screen
    (cx0,cy0) = (self.content._canvas.canvasx(0), self.content._canvas.canvasy(0))
    (cx1,cy1) = (self.content._canvas.canvasx(self.content._canvas.cget("width")), 
                  self.content._canvas.canvasy(self.content._canvas.cget("height")))

    # determine the bounding box of the thing to be made visible
    (x0,y0,x1,y1) = self.content._canvas.coords(preview_frame)

    # determine how far off the screen the object is
    deltax = x0-cx0 if x0 <= cx0 else x1-cx1 if x1 >= cx1 else 0
    deltay = y0-cy0 if y0 <= cy0 else y1-cy1 if y1 >= cy1 else 0

    # scroll the canvas to make the item visible
    self.canvas.xview("scroll", int(deltax), "units")
    self.canvas.yview("scroll", int(deltay), "units")
    return

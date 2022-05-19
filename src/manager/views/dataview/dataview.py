import cv2
import numpy as np 
from typing import List, Dict, Tuple, Callable
from tkinter import *
from tkinter.ttk import Button 
from tkscrolledframe import ScrolledFrame
from PIL import Image, ImageTk

from flow_storage import FlowStorage, FlowDataType

from ....uiconst import *
from ..view import View
from .plotdialog import PlotDialog 

DEFAULT_VIEW_SIZE = 100
WITHOUT_PREVIEW_DATA = -1

class DataView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self['text'] = 'Data'
    # self['bg'] = 'green'

    h = self.parent.winfo_reqheight()
    w = self.parent.winfo_reqwidth()
    self.grid()
    # self.grid_propagate(False)

    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)
    # self.rowconfigure(2, weight=1)
    # self.columnconfigure(0, pad=15)
    self.columnconfigure(0, weight=1)

    # Last existing output
    self._data_last = Frame(self, height=int(h*0.3), highlightbackground='gray', highlightthickness=1)
    self._data_last.grid(row=0, column=0, padx=PADX, pady=PADY_S, sticky=W + E + N + S)
    self._data_last.columnconfigure(0, weight=1)
    self._data_last.rowconfigure(0, weight=1)
    self._data_last.grid_propagate(False)
    # self._last_view = Label(self._data_last, name='last image')

    # Setup canvas inside the frame
    # self._canvas_data_last = Canvas(self._data_last, bg='green')
    # self._canvas_data_last.grid(row=0, column=0, padx=PADX_S, pady=PADY_S, sticky=W + E + N + S)

    #Add PIL image to the Canvas
    # canvas.create_image(10,10,anchor=NW,image=img)

    # Preview content will be scrolable
    self.content = ScrolledFrame(self, height=int(h*0.3), use_ttk=True)
    # Bind the arrow keys and scroll wheel
    # self.content.bind_arrow_keys(self)
    # self.content.bind_scroll_wheel(self)
    self.content.grid(row=1, column=0, padx=PADX, pady=PADY_S, sticky=W + E + N + S)
    # Create the preview frame within the ScrolledFrame
    self.preview_view = self.content.display_widget(Frame)
    
    # self.data_actions = Frame(self, height=int(h*0.2), highlightbackground='gray', highlightthickness=1)
    # self.data_actions.grid(row=2, column=0, padx=PADX, pady=PADY_S, sticky=W + E + S)
    # self.data_actions.columnconfigure(0, weight=1)
    # self.data_actions.columnconfigure(1, weight=1)
    # self.data_actions.columnconfigure(2, weight=1)
    # self.data_actions.columnconfigure(3, weight=1)
    # self.data_actions.columnconfigure(4, weight=1)
    
    # self._preview_height = DEFAULT_VIEW_SIZE
    # self._preview_width = DEFAULT_VIEW_SIZE

    # self.scale_frame = LabelFrame(self.data_actions, text='Preview size:')
    # self.scale_frame.grid(row=0, column=0, columnspan=4, padx=PADX_S, pady=PADY_S, sticky=W+E)
    # self.scale_frame.columnconfigure(0, weight=1)
    # self.scale_frame.columnconfigure(1, weight=1)
    # self.scale_frame.columnconfigure(2, weight=1)
    # self.scale_frame.columnconfigure(3, weight=1)

    # self.var_h = IntVar()
    # self.var_h.set(self._preview_height)
    # self.scale_h = Scale(self.scale_frame, from_=50, to=500, resolution=50, variable=self.var_h, orient=HORIZONTAL, length=400)
    # self.scale_h.grid(row=0, column=0, columnspan=3, padx=PADX_S, pady=PADY_S, sticky=W+E)
    # self.scale_h.bind("<ButtonRelease-1>", self._set_h)

    # self.var_fixed_size = BooleanVar()
    # self.fixed_size = Checkbutton(self.scale_frame, variable=self.var_fixed_size, text='Fixed size', onvalue=True, offvalue=False, command=self._fix_size)
    # self.fixed_size.grid(row=0, column=3, padx=PADX_S, pady=PADY_S, sticky=W+E)

    # self.btn_save = Button(self.data_actions, text='Save', width=BTNW_S, command=self._save)
    # self.btn_save.grid(row=0, column=4, padx=PADX, pady=PADY)
    
    self._out = None
    self._idx_map :Dict = {}
    self._grid_rows: List[Widget] = []
    self._storage: FlowStorage = None
    self._last_view = None
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
    self._idx_map = {}
    for row in self._grid_rows:
      row.grid_remove()  
    self._grid_rows.clear()
    self.content.scroll_to_top()
    if self._last_view is not None:
      self._last_view.grid_remove()
    return

  def default(self) -> None:
    # if self.var_fixed_size.get():
    #   return
    self._preview_height = DEFAULT_VIEW_SIZE
    self._preview_width = DEFAULT_VIEW_SIZE
    # self.var_h.set(self._preview_height)
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

  def _fit_image(self, image):  
    dim = self._preview_size(image)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_NEAREST)
    return image

  def _preview_image_list(self, parent, image: List[np.ndarray], name: str) -> Widget:
    image = cv2.hconcat(image)
    return self._preview_image(parent, image, name)

  def _preview_image(self, parent, image: np.ndarray, name: str) -> Widget:
    preview = self._fit_image(image)
    pil_image = Image.fromarray(preview)
    photo = ImageTk.PhotoImage(pil_image)
    view = Label(parent, name=name, image=photo)
    view.image = photo
    return view

  def _preview_object(self, parent, data: any, name: str) -> Widget:
    view = Label(parent, name=name, border=1)
    # text = json.dumps(data, indent = 3)
    # df = pd.DataFrame(data)
    view.config(text = data)
    return view

  def _get_preview(self, ref_type: FlowDataType) -> Callable:
    views = {
      FlowDataType.NP_ARRAY: self._preview_image,
      FlowDataType.LIST_NP_ARRAYS: self._preview_image_list
    }
    return views.get(ref_type, self._preview_object)

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
        self._idx_map.pop(f'{row_idx}')
        # remove existing preview item with the idx
        res = self._grid_rows.pop(row_idx)
        res.grid_remove()
      except IndexError:
        pass
    return
  
  def update_result(self, idx: int, state_id: str) -> None:
    self._show_last(state_id)
    self. _clear_preview(idx)
    return
 
  def _create_row_output_container(self, row_idx: int, title: str) -> Widget:
    state_frame = LabelFrame(self.preview_view, name=f'--{row_idx}--', text=title)
    state_frame.grid(row=row_idx, column=0, sticky=W)
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
      preview = self._get_preview(ref_type)
      # convert to a conventional format (without '.')
      name = ref_extr.replace('.', '-')
      widget = preview(preview_frame, data, name)
      widget.grid(row=i, column=0, sticky=W)
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

  def _show_last(self, state_id: str) -> None:
    out_data = self._storage.get_state_output_data(state_id)
    refs = self._storage.get_state_output_refs(state_id)
    if out_data is None or refs is None:
      return
    out_refs = [(ref.ext_ref, ref.int_ref, ref.data_type) for ref in refs]  
    if len(out_refs) > 0:
      ref = out_refs[0]
      (ref_extr, ref_intr, ref_type) = ref
      data = out_data.get(ref_intr)
      if data.dtype == np.dtype('uint8'):
        pil_image = Image.fromarray(data)
        photo = ImageTk.PhotoImage(pil_image)
        self._last_view = Label(self._data_last, name='last image', image=photo)
        self._last_view.image = photo 
        self._last_view.grid(row=0, column=0, padx=PADX_S, pady=PADY_S, sticky=W + E + N + S)
      else:
        self._last_view.grid_remove()
      # self._canvas_data_last.create_image(x1=10, y1=10, anchor=NW, image=photo)
    return

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

  def _show_preview(self, idx: int, state_id: str) -> None:
    out_data = self._storage.get_state_output_data(state_id)
    refs = self._storage.get_state_output_refs(state_id)
    if out_data is None or refs is None:
      return
    out_refs = [(ref.ext_ref, ref.int_ref, ref.data_type) for ref in refs]  
    self._out = (out_refs, out_data)
    self._map_idx_to_row_idx(idx)
    self._preview()
    return

  def show_result(self, idx: int, state_id: str) -> None:
    self._show_preview(idx, state_id)
    self._show_last(state_id)
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
    self._preview_height = self.scale_h.get()
    self._preview()
    return

  def _fix_size(self) -> None:
    # self.scale_h['state'] = NORMAL
    # if self.var_fixed_size.get() == True:
    #   self.scale_h['state'] = DISABLED
    return

  def _save(self) -> None:
    print('save')
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

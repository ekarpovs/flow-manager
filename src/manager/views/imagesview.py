from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import cv2
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from ...uiconst import *
from .view import View

class ImagesView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self['bg'] = "snow2"
    self['text'] = 'Images panel'

    self.panel_height, self.panel_width = get_panel_size(parent)
    
    self.grid()
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, minsize=40)
    self.rowconfigure(2, minsize=40)
    self.columnconfigure(0, weight=1)

    # Init the original image holder
    self.image_label = Label(self, text='Image', image=None, borderwidth=2, relief="solid")
    self.image_label.image = None
    self.image_label.grid(row=0, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=W + E + N + S)

    self.namesvar = StringVar()
    self.names_combo_box = ttk.Combobox(self, textvariable=self.namesvar)
    self.names_combo_box['state'] = 'readonly'

    self.btn_load = ttk.Button(self, text='Load', width=BTNW)

    self.paths = []
    self.modulesvar = StringVar(value=self.paths)
    self.file_names_list_box = Listbox(self, height=10, listvariable=self.modulesvar, selectmode=BROWSE)

    self.names_combo_box.grid(row=2, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
    self.btn_load.grid(row=2, column=1, padx=PADX, pady=PADY, sticky=W + S)
    self.file_names_list_box.grid(row=3, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=N+S+W+E)


  def set_input_paths(self, paths):
    self.names_combo_box['values'] = paths
    self.names_combo_box.current(0)
    return

  def set_file_names_list(self, file_names_list):
    self.modulesvar.set(file_names_list)
    self.set_selection()
    return

  def set_selection(self, idx=0):
    self.file_names_list_box.focus_set()
    cur_idx = self.file_names_list_box.curselection()
    if len(cur_idx) == 0:
      cur_idx = 0
    self.file_names_list_box.selection_clear(cur_idx, cur_idx)
    self.select_list_item(idx)   
    return

  def select_list_item(self, idx):
    self.file_names_list_box.activate(idx)
    self.file_names_list_box.selection_set(ACTIVE)
    self.file_names_list_box.see(idx)
    self.file_names_list_box.event_generate("<<ListboxSelect>>")
    return

  def calculate_new_size(self, image):
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

  def set_result_image(self, cv2image):
    figure = Figure(figsize=(5,5), dpi=100)
    splot = figure.add_subplot(111)
    splot.imshow(cv2image,  cmap='gray')  

    canvas = FigureCanvasTkAgg(figure, self)
    canvas.draw()
    wdg = canvas.get_tk_widget()
    wdg.grid(row=0, column=0, padx=PADX, pady=PADY, columnspan=2, sticky=W + E + N + S)

    toolbar = NavigationToolbar2Tk(canvas, wdg)
    toolbar.update()
    wdg = canvas.get_tk_widget()
    return

  # def fit_image_to_panel(self, image):
  #   self.calculate_new_size(image)   
  #   dim = (self.w, self.h)
  #   image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
  #   return image

  # def set_result_image_orig(self, cv2image):
  #   cv2image = self.fit_image_to_panel(cv2image)
  #   image = Image.fromarray(cv2image)
  #   imagetk = ImageTk.PhotoImage(image=image)
  #   # Show the image
  #   self.set_content(self.image_label, 0, 0, imagetk)
  #   return

  # def set_content(self, label, r, c, imagetk):
  #   label = Label(self, text='Image', image=imagetk, borderwidth=2, relief="solid")
  #   label.image = imagetk
  #   label.grid(row=r, column=c, padx=PADX, pady=PADY, columnspan=2, sticky=W + E + N + S)
  #   return

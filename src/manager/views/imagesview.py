from tkinter import *
# from PIL import Image, ImageTk
from tkinter import ttk
# import cv2
import matplotlib
matplotlib.use("agg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
# import matplotlib.animation as animation

from ...uiconst import *
from .view import View

class ImagesView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    # self['bg'] = "snow2"
    self['text'] = 'Input/Output'

    self.panel_height, self.panel_width = get_panel_size(parent)
    
    self.grid()
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, minsize=40)
    self.rowconfigure(2, minsize=40)
    self.rowconfigure(3, minsize=40)
    self.columnconfigure(0, weight=1)

    # Init the original image holder
    self.image_label = Label(self, text='Image', image=None, borderwidth=2, relief="solid")
    self.image_label.image = None
    self.image_label.grid(row=0, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=W + E + N + S)

    self.withoutvar = BooleanVar()
    self.without_check_button = ttk.Checkbutton(self, text = "Use without input", variable=self.withoutvar, onvalue=True, offvalue=False, command=self.without)
    self.without_check_button.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=W + S)

    self.namesvar = StringVar()
    self.names_combo_box = ttk.Combobox(self, textvariable=self.namesvar, font=("TkDefaultFont"))
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

  def set_result_image(self, cv2image):
    # !!! Memory leak
    figure = plt.figure(1); 
    plt.clf()
    plt.axis('off')

    canvas = FigureCanvasTkAgg(figure, self)
    canvas.draw()
    wdg = canvas.get_tk_widget()
    wdg.grid(row=0, column=0, padx=PADX, pady=PADY, columnspan=2, sticky=W + E + N + S)
   
    plt.imshow(cv2image, cmap='gray')
    return

  def without(self):
    if self.withoutvar.get():
      self.without_check_button.event_generate("<<CheckbuttonChecked>>")
    else:
      self.without_check_button.event_generate("<<CheckbuttonUnChecked>>")
    return

  def activate_controls(self, activate=False):
    state = DISABLED
    if activate:
      state = NORMAL
    self.names_combo_box['state']=state
    self.file_names_list_box['state']=state
    self.btn_load['state']=state
    return

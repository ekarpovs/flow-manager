from tkinter import *
from PIL import Image, ImageTk
from tkinter import ttk
import cv2

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
    # self.rowconfigure(1, weight=1)
    self.rowconfigure(2, minsize=40)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)

    # Init the original image holder
    self.image_orig_label = Label(self, text='Original', image=None, borderwidth=2, relief="solid")
    self.image_orig_label.image = None
    self.image_orig_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + E + N + S)

    # Init the output image holder
    self.image_result_label = Label(self, text='Result', image=None, borderwidth=2, relief="solid")
    self.image_result_label.image = None
    self.image_result_label.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=W + E + N + S)

    self.namesvar = StringVar()
    self.names_combo_box = ttk.Combobox(self, textvariable=self.namesvar)
    self.names_combo_box['state'] = 'readonly'

    self.btn_load = Button(self, text='Load', width=BTNW)

    self.paths = []
    self.modulesvar = StringVar(value=self.paths)
    self.file_names_list_box = Listbox(self, height=10, listvariable=self.modulesvar, selectmode=BROWSE)

    self.names_combo_box.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=N+S+W+E)
    self.btn_load.grid(row=1, column=1, padx=PADX, pady=PADY, sticky=W + S)
    self.file_names_list_box.grid(row=2, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=N+S+W+E)


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
    if h > self.panel_height//2:
      h = self.panel_height//2
      w = int(h*ratio)
    if w > self.panel_width//2:    
      w = self.panel_width//2
      h = int(w/ratio)
    
    self.h = h
    self.w = w


  def fit_image_to_panel(self, image):
    self.calculate_new_size(image)
    
    dim = (self.w, self.h)
    image = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)

    return image


  def set_original_image(self, cv2image):
    cv2image = self.fit_image_to_panel(cv2image)
    image = Image.fromarray(cv2image)
    imagetk = ImageTk.PhotoImage(image=image)

    # Show the image
    self.set_content(self.image_orig_label, 0, 0, imagetk)

    return

  def set_result_image(self, cv2image):
    cv2image = self.fit_image_to_panel(cv2image)
    image = Image.fromarray(cv2image)
    imagetk = ImageTk.PhotoImage(image=image)

    # Show the image
    self.set_content(self.image_result_label, 0, 1, imagetk)

    return

  def reset_result_image(self):
    self.set_content(self.image_result_label, 0, 1, None)

  
  def set_content(self, label, r, c, imagetk):
    label = Label(self, text='Result', image=imagetk, borderwidth=2, relief="solid")
    label.image = imagetk
    label.grid(row=r, column=c, padx=PADX, pady=PADY, sticky=W + E + N + S)

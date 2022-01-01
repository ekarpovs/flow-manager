from tkinter import *
import matplotlib
import numpy as np
matplotlib.use("agg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt

from ...uiconst import *
from .view import View

class DataView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 
    self['text'] = 'Data'

    self.panel_height, self.panel_width = get_panel_size(parent)
    
    self.grid()
    self.rowconfigure(0, weight=20)
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=50)

    self.chk_item = BooleanVar()
    self.show_output = Checkbutton(self, variable=self.chk_item, onvalue=True, offvalue=False, command=self.get)
    self.show_output.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=W)
    self.show_output_lbl = Label(self, text='Show output', anchor=W, justify=LEFT)
    self.show_output_lbl.grid(row=1, column=1, padx=PADX, pady=PADY, sticky=W)
    return

  def get(self):
    print('check', self.chk_item.get())
    if not self.chk_item.get():
      plt.close()
    else:
      self.figure = plt.figure(1)
    return

  def set_result_image(self, cv2image: np.dtype = None) -> None:
    if not self.chk_item.get():
      return
    plt.clf()
    # !!! Memory leak
    # plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    canvas = FigureCanvasTkAgg(self.figure, self)
    canvas.draw()
    tk_wd = canvas.get_tk_widget()
    tk_wd.grid(row=0, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=W + E + S + N)
    nb = NavigationToolbar2Tk(canvas, tk_wd)
    nb.update()
    if cv2image is None:
      return
    plt.imshow(cv2image, cmap='gray')
    return


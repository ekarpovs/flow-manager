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
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)

    self.figure = plt.figure(1)
    return

  def set_result_image(self, cv2image: np.dtype = None) -> None:
    plt.clf()
    # !!! Memory leak
    # plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    canvas = FigureCanvasTkAgg(self.figure, self)
    canvas.draw()
    tk_wd = canvas.get_tk_widget()
    tk_wd.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + E + S + N)
    nb = NavigationToolbar2Tk(canvas, tk_wd)
    nb.update()
    if cv2image is None:
      return
    plt.imshow(cv2image, cmap='gray')
    return


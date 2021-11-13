from tkinter import *
# from PIL import Image, ImageTk
from tkinter import ttk
# import cv2
import matplotlib
matplotlib.use("agg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
# from matplotlib.figure import Figure
import matplotlib.pyplot as plt
# import matplotlib.animation as animation

from ...uiconst import *
from .view import View

class DataView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self.panel_height, self.panel_width = get_panel_size(parent)
    
    self.grid()
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, minsize=20)
    self.columnconfigure(0, weight=1)

    self.figure = plt.figure(1); 

  def set_result_image(self, cv2image):
    plt.clf()
    # !!! Memory leak
    # plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
    canvas = FigureCanvasTkAgg(self.figure, self)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0, padx=PADX, pady=PADY, columnspan=3, sticky=W + E + N + S)
   # navigation toolbar
    tb_frame = Frame(self)
    tb_frame.grid(row=1, column=0, padx=PADX, pady=PADY, columnspan=3, sticky=W + E + N + S)
    NavigationToolbar2Tk(canvas, tb_frame)
    if cv2image is None:
      return
    plt.imshow(cv2image, cmap='gray')
    return


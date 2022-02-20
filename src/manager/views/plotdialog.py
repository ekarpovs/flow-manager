from tkinter import *
from tkinter import ttk
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

from ...uiconst import *

class PlotDialog(Toplevel):
  def __init__(self, parent, name: str, data):
    super().__init__(parent)
    
    self._name = name
    self._data = data
    # Do the dialog modal
    self.transient(parent)
    self.grab_set()
    # Define the dialog size and location
    self.title(f'Inspect: {name}')
    width = 950
    heigth = 850
    self.geometry(f'{width}x{heigth}+%d+%d' % (parent.winfo_rootx() + parent.winfo_width() - (width+PADX*2), parent.winfo_rooty()+PADY*2))
    # self.geometry("950x850+%d+%d" % (parent.winfo_rootx() + parent.winfo_width() - 975, parent.winfo_rooty()+PADY))
    self.resizable(height=FALSE, width=FALSE) 

    self.rowconfigure(0, weight=10)
    self.rowconfigure(1, minsize=20)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
    self.columnconfigure(2, weight=1)

    self._btn_cancel = ttk.Button(self, text='Close', width=BTNW_S, command=self._close)
    self._btn_cancel.grid(row=1, column=2, padx=PADX, pady=PADY, sticky=S+E)

    self._plot()
    return

  def _close(self) -> None:
    plt.clf()
    plt.close()
    self.destroy()
    return

  def _plot(self) -> None:
    t = type(self._data)
    if t == np.ndarray or t == list:
      return self._plot_image()
    return self._plot_object()

  def _plot_object(self) -> None:
    #Set the size of the matplotlib canvas
    f = plt.figure(num=0, figsize=(12,12), dpi=600)

    # creating dataframe
    # df = pd.DataFrame({
    #     'X': [1, 2, 3, 4, 5],
    #     'Y': [2, 4, 6, 10, 15]
    # })
    df = pd.DataFrame(self._data)
      
    # plotting a line graph
    # plt.plot(df["cX"], df["cY"])
    # # plotting a scatter plot
    # print("Scatter Plot:  ")
    plt.scatter(df["cX"], df["cY"])


    canvas = FigureCanvasTkAgg(f, self)
    canvas.draw()
    canvas.mpl_connect('button_press_event', self.onclick)
    tk_wd = canvas.get_tk_widget()
    tk_wd.grid(row=0, column=0, columnspan=3, padx=PADX, pady=PADY, sticky=W + E + S + N)
    nb = NavigationToolbar2Tk(canvas, tk_wd)     
    return

  def _plot_image(self) -> None:
    f = plt.figure(num=0, figsize=(8,8))

    canvas = FigureCanvasTkAgg(f, self)
    canvas.draw()
    tk_wd = canvas.get_tk_widget()
    tk_wd.grid(row=0, column=0, columnspan=3, padx=PADX, pady=PADY, sticky=W + E + S + N)
    nb = NavigationToolbar2Tk(canvas, tk_wd)
    if type(self._data) == np.ndarray: 
      images = [self._data]
    else:
      images = self._data
    self._display_multiple_img(f, images, 1, len(images))
    # plt.imshow(self._data, cmap='gray')    
    return


  @staticmethod
  def _display_multiple_img(fig, images, rows = 1, cols=1):
    axes = []
    for idx,title in enumerate(images):
      axes.append( fig.add_subplot(rows, cols, idx+1))
      plt.imshow(images[idx], cmap='gray')    
    return

  def onclick(self,event):
    if event.xdata is None or event.ydata is None:
      return
    ix, iy = float(event.xdata), float(event.ydata)
    print('x = %f, y = %f' % (ix, iy))
    return 


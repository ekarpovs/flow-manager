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
    # Define the dialog size
    self.title(f'Inspect: {name}')
    self.geometry("850x750+%d+%d" % (parent.winfo_rootx() +50, parent.winfo_rooty() + 50))
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
    if t == np.ndarray:
      return self._plot_image()
    return self._plot_object()

  def _plot_object(self) -> None:
    df = pd.DataFrame(self._data)
    print(df)
    df.plot()
    return

  def _plot_image(self) -> None:
    f = plt.figure(num=0, figsize=(8,8))

    canvas = FigureCanvasTkAgg(f, self)
    canvas.draw()
    tk_wd = canvas.get_tk_widget()
    tk_wd.grid(row=0, column=0, columnspan=3, padx=PADX, pady=PADY, sticky=W + E + S + N)
    nb = NavigationToolbar2Tk(canvas, tk_wd)
    plt.imshow(self._data, cmap='gray')    
    return

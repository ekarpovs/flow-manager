from tkinter import *
from tkinter import ttk

from ...uiconst import *

class CdActionsFrame(Frame):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self.btn_ok = ttk.Button(self, text='Apply', width=BTNW_S, command=self._apply)
    self.btn_ok.pack(padx=PADX,  pady=PADY, side = 'left')

    self.btn_cancel = ttk.Button(self, text='Cancel', width=BTNW_S, command=self._cancel)
    self.btn_cancel.pack(padx=PADX, pady=PADY, side = 'right')

  def _apply(self) -> None:
    self.parent.apply() 
    return

  def _cancel(self) -> None:
    self.parent.cancel()
    return
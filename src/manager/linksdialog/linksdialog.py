import copy

from tkinter import *
from typing import Callable
from tkscrolledframe import ScrolledFrame

from ...uiconst import *
from ..linksdialog.contentview import ContentView
from ..models.flow.currentflowmodel import CurrentFlowModel 
from .ldactionsframe import LdActionsFrame

class LinksDialog(Toplevel):
  def __init__(self, parent, flow: CurrentFlowModel, callback: Callable):
    super().__init__(parent)
    self._flow = flow
    self._callback = callback
    # Do the dialog modal
    self.transient(parent)
    self.grab_set()
    # Define the dialog size
    self.title('Configure:')
    self.geometry("550x845+%d+%d" % (parent.winfo_rootx() +920, parent.winfo_rooty() + 30))
    self.resizable(height=FALSE, width=FALSE) 
    
    self.grid()
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=20)
    self.rowconfigure(2, weight=1)

    self._info = LabelFrame(self)
    self._info.columnconfigure(0, weight=1)
    self._info.columnconfigure(1, weight=5)
    self._info_lbl = Label(self._info, text='flow info:')
    self._info_lbl.grid(row=0, column=0, sticky=W)
    self._info_name_var = StringVar()
    self._info_name_var.set(flow.flow.info)
    self._info_entry = Entry(self._info, width=50, textvariable=self._info_name_var)
    self._info_entry.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=W+E+N+S)
    self._info.grid(row=0, column=0, columnspan=2, padx=PADX, pady=PADY, sticky=W+E+N+S)

    # Content will be scrolable
    self.content = ScrolledFrame(self)
    # Bind the arrow keys and scroll wheel
    self.content.bind_arrow_keys(self)
    self.content.bind_scroll_wheel(self)
    # Create the ContentView frame within the ScrolledFrame
    self.content_view = self.content.display_widget(ContentView)
    self.content_view.init_content(flow)
    self.content.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=W+E+N+S)
    
    self.actions_frame = LdActionsFrame(self)
    self.actions_frame.grid(row=2, column=0, padx=PADX, pady=PADY, sticky=W+E+N+S)

    return

  def apply(self) -> None:
    self.content_view.update_flow()
    self._flow.flow = copy.deepcopy(self.content_view.tmp_flow)
    self._flow.flow.info = self._info_name_var.get()
    self._callback()
    self.destroy()
    return

  def cancel(self) -> None:
    self.destroy()
    return


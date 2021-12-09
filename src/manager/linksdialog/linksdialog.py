from tkinter import *
from tkscrolledframe import ScrolledFrame

from ...uiconst import *
from ..linksdialog.contentview import ContentView
from ..models.flow.currentflowmodel import CurrentFlowModel 
from .ldactionsframe import CdActionsFrame

class LinksDialog(Toplevel):
  def __init__(self, parent, flow: CurrentFlowModel):
    super().__init__(parent)
    self._flow = flow
    # Do the dialog modal
    self.transient(parent)
    self.grab_set()
    # Define the dialog size
    self.title(f'Configure links: {flow.flow.info}')
    self.geometry("400x600+%d+%d" % (parent.winfo_rootx() +920, parent.winfo_rooty() + 30))
    self.resizable(height=FALSE, width=FALSE) 
    
    self.grid()
    self.columnconfigure(0, weight=1)
    self.rowconfigure(0, weight=20)
    self.rowconfigure(1, weight=1)

    # Content will be scrolable
    self.content = ScrolledFrame(self)
    # Bind the arrow keys and scroll wheel
    self.content.bind_arrow_keys(self)
    self.content.bind_scroll_wheel(self)
    # Create the ContentView frame within the ScrolledFrame
    self.content_view = self.content.display_widget(ContentView)
    self.content_view.init_content(flow)
    self.content.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W+E+N+S)
    
    self.actions_frame = CdActionsFrame(self)
    self.actions_frame.grid(row=1, column=0, padx=PADX, pady=PADY, sticky=W+E+S)

    return

  def apply(self) -> None:
    self.content_view.update_flow()
    self._flow.flow = self.content_view.tmp_flow
    self.destroy()
    return

  def cancel(self) -> None:
    self.destroy()
    return


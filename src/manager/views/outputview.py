from tkinter import *
from PIL import Image, ImageTk

from ...uiconst import *
from .view import View

class OutputView(View):
  def __init__(self, parent):
    super().__init__(parent)
    self.parent = parent 

    self['bg'] = "snow2"
    self['text'] = 'Output panel'

    self.grid()
    self.rowconfigure(0, weight=1)
    self.rowconfigure(1, weight=1)
    self.columnconfigure(0, weight=1)
    self.columnconfigure(1, weight=1)
  


  def set_original_image(self, cv2image):
    image = Image.fromarray(cv2image)
    imagetk = ImageTk.PhotoImage(image=image)

    # Show the image
    self.image_orig_label = Label(self, text='Original', image=imagetk, borderwidth=2, relief="solid")
    self.image_orig_label.image = imagetk
    self.image_orig_label.grid(row=0, column=0, padx=PADX, pady=PADY, sticky=W + E + N + S)

    return

  def set_result_image(self, cv2image):
    image = Image.fromarray(cv2image)
    imagetk = ImageTk.PhotoImage(image=image)

    # Show the image
    self.image_result_label = Label(self, text='Result', image=imagetk, borderwidth=2, relief="solid")
    self.image_result_label.image = imagetk
    self.image_result_label.grid(row=0, column=1, padx=PADX, pady=PADY, sticky=W + E + N + S)

    return
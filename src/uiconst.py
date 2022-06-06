SCREEN_FREE_AREA = 70 

PADX = 10
PADX_S = 5
PADY = 10
PADY_S = 5
BTNW = 10
BTNW_S = 7

def calculate_reminder_height(parent, frames):
  parent.update()
  parent_height = parent.winfo_height()

  used_height = 0
  for f in frames:
    used_height += f.winfo_height() 

  return parent_height - used_height


def get_panel_size(parent):
  parent.update()
  width = parent.winfo_width()
  height = parent.winfo_height()

  return width, height
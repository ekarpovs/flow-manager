PADX = 10
PADY = 10
BTNW = 10


def calculate_reminder_height(parent, frames):
  parent.update()
  parent_height = parent.winfo_height()

  used_height = 0
  for f in frames:
    used_height += f.winfo_reqheight() 

  return parent_height - used_height - PADY*4


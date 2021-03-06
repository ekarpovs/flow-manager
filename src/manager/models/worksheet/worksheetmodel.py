'''
'''
import json
import os
from pathlib import Path
from tkinter.filedialog import asksaveasfilename
from typing import Dict, List, Tuple

class WorksheetModel():
  def __init__(self, paths: List[str]) -> None:
    self._worksheetnames: List[str] = []
    self._read_names(paths)

  @property
  def workseetnames(self) -> List[str]:
    return self._worksheetnames

  def read(self, path, name) -> List[Dict]:
    ffn = f'{path}/{name}.json'
    with open(ffn, 'rt') as f:
      data = json.load(f)
      return data
   
  def _worksheets_names(self, target_path, level=0):
    """"
    This function recursively prints all contents of a pathlib.Path object
    https://stackoverflow.com/questions/16953842/using-os-walk-to-recursively-traverse-directories-in-python
    """
    # def print_indented(folder, level):
    #   print('\t' * level + folder)
    
    # print_indented(target_path.name, level)
    
    for file in target_path.iterdir():
      if file.is_dir():
        self._worksheets_names(file, level+1)
      else:
        # print_indented(file.name, level+1)
        if file.suffix == '.json':
          self._worksheetnames.append(f'{file.stem} <{target_path}>')
    return

  def _read_names(self, paths) -> None:
    for path in paths:
      p = Path(path)
      self._worksheets_names(p)
    return

  # If indent is a non-negative integer, then JSON array elements and object members 
  # will be pretty-printed with that indent level. An indent level of 0, or negative, 
  # will only insert newlines. None (the default) selects the most compact representation.
  def store(self, path: str, name: str, ws: List[Dict]) -> Tuple[str, str]:
    new_name = name
    new_path = path
    ffn = asksaveasfilename(initialfile = '{}.json'.format(name),
      initialdir = path,
      defaultextension=".json",filetypes=[("All Files","*.*"),("Json Documents","*.json")])
    if ffn != '':
      with open(ffn, 'w') as fp:
        json.dump(ws, fp, indent=2)
        new_path, fn = os.path.split(ffn)
        new_name, ext = fn.split('.')
    # Reread 
    return (new_path, new_name)

  
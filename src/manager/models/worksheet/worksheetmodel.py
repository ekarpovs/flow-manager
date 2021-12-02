'''
'''
import json
import os
from tkinter.filedialog import asksaveasfilename
from typing import Dict, List

class WorksheetModel():
  def __init__(self, paths: List[str]) -> None:
    self._workshetnames: List[str] = []
    self._read_names(paths)

  @property
  def workseetnames(self) -> List[str]:
    return self._workshetnames

  def read(self, path, name) -> List[Dict]:
    ffn = f'{path}/{name}.json'
    with open(ffn, 'rt') as f:
      data = json.load(f)
      return data
   
  @staticmethod
  def _worksheets_names(path):
    worksheets_names = [f[:-5] for f in os.listdir(path) if f.endswith('.json')]
    return worksheets_names

  def _read_names(self, paths) -> None:
    for path in paths:
      names = self._worksheets_names(path)
      for name in names:
        self._workshetnames.append(f'{name} <{path}>')
    return

  # If indent is a non-negative integer, then JSON array elements and object members 
  # will be pretty-printed with that indent level. An indent level of 0, or negative, 
  # will only insert newlines. None (the default) selects the most compact representation.
  def store(self, path: str, name: str, ws: List[Dict]) -> str:
    new_name = name
    ffn = asksaveasfilename(initialfile = '{}.json'.format(name),
      initialdir = path,
      defaultextension=".json",filetypes=[("All Files","*.*"),("Json Documents","*.json")])
    if ffn is not '':
      with open(ffn, 'w') as fp:
        json.dump(ws, fp, indent=2)
        path, fn = os.path.split(ffn)
        new_name, ext = fn.split('.')
    # Reread 
    return new_name

  
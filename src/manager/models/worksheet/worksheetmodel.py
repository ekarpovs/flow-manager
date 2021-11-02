'''
'''
import json
import os
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
  # from tkinter.filedialog import asksaveasfilename
  # def store(self, path, name, meta):
  #   f = asksaveasfilename(initialfile = '{}.json'.format(name),
  #     initialdir = path,
  #     defaultextension=".json",filetypes=[("All Files","*.*"),("Json Documents","*.json")])
  #   if f is not '':
  #     with open(f, 'w') as fp:
  #       # if meta[0] == BEGIN_FLOW_MARKER:
  #       #   meta.pop(0)
  #       # if meta[-1] == END_FLOW_MARKER:
  #       #   meta.pop(-1)
  #       json.dump(meta, fp, indent=2)
  #     # self.worksheets_from_all_paths = []    
  #     # self.load_worksheets_from_all_paths()
  #   return

  
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

    
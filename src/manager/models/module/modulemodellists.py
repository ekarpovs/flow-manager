'''
'''

import os
from typing import List

from .modulemodellist import ModuleModelList


class ModuleModelLists():
  def __init__(self, parent, paths: List[str]) -> None:
    self._parent = parent
    self._paths: List[str] = paths
    self._modulemodellists: List[ModuleModelList] = []
    self._load()
    return

  @property
  def paths(self) -> List[str]:
    return self._paths

  @property
  def modulemodellists(self) -> List[ModuleModelList]:
    return self._modulemodellists

  def get_modulemodellist(self, path: str) -> List[ModuleModelList]:
    for mlist in self._modulemodellists:
      if mlist.path == path:
        return mlist
    return ModuleModelList()

  
  def _load(self) -> None:
    for path in self.paths:
      mlist = ModuleModelList(path)
      mlist.load()
      self._modulemodellists.append(mlist)
    return

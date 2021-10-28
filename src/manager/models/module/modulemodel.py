'''
'''
import json
from typing import List, Dict

import operation_loader

from .moduleitemmodel import ModuleItemModel

class ModuleModel():
  def __init__(self, path: str) -> None:
      self._path: str = path
      self._name: str = ''
      self._doc: str = ''
      self._items: List[ModuleItemModel] = []
      return
      

  def _parse(self, func_meta: List[Dict]) -> ModuleItemModel:
    iname = func_meta.get('name')
    idoc = func_meta.get('doc')
    item = ModuleItemModel(iname, idoc)
    return item

  @property
  def path(self) -> str:
    return self._path

  @property
  def name(self) -> str:
    return self._name

  @name.setter
  def name(self, name: str) ->None:
    self._name = name
    return

  @property
  def doc(self) -> str:
    return self._doc

  @doc.setter
  def doc(self, doc: str) ->None:
    self._doc = doc.strip()
    return
 
  @property
  def items(self) -> List[ModuleItemModel]:
    return self._items

  @property
  def loaded(self) -> bool:
    return len(self._items) > 0


  def get_item(self, name: str) -> ModuleItemModel:
    oper = None
    for item in self._items:
      iname = item.name
      if iname is not '' and iname == name:
        oper = item
        break;
    return oper


  def load(self, name: str) -> None:
    #module_meta =  {'descr': mod.__doc__, 'func': func_names, 'meta': func_metas}
    module_meta = operation_loader.get_module_meta(name)
    self.name = name
    self.doc = module_meta.get('descr', '')
    func_metas = module_meta.get('meta')
    for func_meta in func_metas:
      item = self._parse(func_meta)
      self._items.append(item)
    return


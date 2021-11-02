'''
'''

from typing import Dict, List, Tuple


class ModuleItemModel():
  def __init__(self, name: str='', doc: str='') -> None:
      self._name = name
      self._description = ''
      self._doc: List[str] = []
      self._params: List[Dict] = None
      self._inrefs: List[Dict] = None
      self._outrefs: List[Dict] = None
      self._parse_doc(doc)

  COMMENT_SEPARATOR = ';'
  NAME_SEP = ':'
  TYPE_SEP = '='

  @property
  def name(self) -> str:
    return self._name

  @property
  def description(self) -> str:
    return self._description

  @property
  def params(self) -> Dict:
    return self._params

  @property
  def inrefs(self) -> Dict:
    return self._inrefs
  
  @property
  def outrefs(self) -> Dict:
    return self._outrefs
  
  def _parse_doc(self, doc: str) -> None:
    doc = doc.strip().split('\n')
    for line in doc:
      line = line.expandtabs().strip()
      if line != "":
        self._doc.append(line)
    self._description = self._doc[0]
    idx_s = self._doc.index('Parameters:')
    idx_e = self._doc.index('Returns:')
    parameters = self._doc[idx_s+1:idx_e]
    returns_descr = self._doc[idx_e+2:]
    idx_s = parameters.index('- params:')
    idx_e = parameters.index('- data:')
    params_descr = parameters[idx_s+1:idx_e]
    data_descr = parameters[idx_e+1:]

    self._params = self._parse_descrtiptors(params_descr)
    self._inrefs = self._parse_descrtiptors(data_descr)
    self._outrefs = self._parse_descrtiptors(returns_descr)
    return 


    # 'name':'thrs1'
    # 'type':'Range'
    # 'default':'50'
    # 'p_values':'10,150,1'
    # 'comment':'threshold1'

    
    # 'name':'type'
    # 'comment':'new color space, one from cv2.COLOR_(...)'
    # 'p_values':'BGR2BGRA:0,BGR2RGB:4,BGR2GRAY:6,BGR2XYZ:32,BGR2YCrCb:36,BGR2HSV:40,BGR2LAB:44,BGR2Luv:50,BGR2HLS:52,BGR2YUV:82'
    # 'default':'BGR2GRAY'
    # 'type':'Dict'

    # 'name':'kernel'
    # 'comment':'kernel size'
    # 'p_values':'3,5,7,9'
    # 'default':'3'
    # 'type':'List'

  def _parse_descrtiptors(self, descriptors: List[str]) -> List[Dict]:
    definitions = []
    for descr in descriptors:
      #p - 'x1: int=10 ; right top coordinate'
      (descr, comment) = self._split_descriptor(descr)
      if ':' in descr:
        (name, descr) = self._split_descriptor(descr, ':')
        if '=' in descr:
          (type, default) = self._split_descriptor(descr, '=')
        else:
          type = descr
          default = None
        if '(' in type:
          idx_s = type.index('(')
          idx_e = type.index(')')
          p_values = type[idx_s+1:idx_e]
          (type, _) = self._split_descriptor(type, '(')
          if '[' in type:
            idx_s = type.index('[')
            idx_e = type.index(']')
            p_types = type[idx_s+1:idx_e]
            (type, _) = self._split_descriptor(type, '[')
        else:
          p_values = None
          p_types = None
      definition = {'name': name, 'type': type, 'default': default, 'p_types': p_types, 'p_values': p_values, 'comment': comment}
      definitions.append(definition)
    return definitions

  @staticmethod
  def _split_descriptor(descriptor: str, delimeter: str=';') -> Tuple[str, str]:
    parts = descriptor.split(delimeter, 1)
    p1 = parts[0].strip()
    p2 = parts[1].strip()
    return (p1, p2)



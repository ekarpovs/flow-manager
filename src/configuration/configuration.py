import sys
import json
from typing import List, Dict, Tuple

from flow_storage import FlowStorageConfig

class Configuration():
  def __init__(self):
    (self._cfg, self._cfg_fsm) = self._load()
    self._cfg_storage = FlowStorageConfig(self._cfg_fsm.get('storage-path', '.'))
    

  # Loaders
  @staticmethod
  def _load() ->Tuple[Dict, Dict]:
    # Read from config.json
    ffn = "{}.json".format('config')
    with open(ffn, 'rt') as ws:
      cfg = json.load(ws)
    ffn = cfg.get('fsm-cfg', './fsm-cfg.json')
    with open(ffn, 'rt') as ws:
      cfg_fsm = json.load(ws)
    # Set paths for access to modules outside of the application
    # without the modules installation
    for path in cfg.get('modules', '.'):
      sys.path.append(path)
    return (cfg, cfg_fsm)


  @property
  def input_paths(self) ->List[str]:
    return self._cfg.get('data-root', '.')

  @property
  def result_path(self) ->str:
    return self._cfg.get('results', '.')

  @property
  def modules_paths(self) ->List[str]:
    return self._cfg.get('modules', '.')

  @property
  def worksheets_paths(self) ->List[str]:
    return self._cfg.get('worksheets', '.')

  @property
  def cfg_fsm(self) ->Dict:
    return self._cfg_fsm

  @property
  def cfg_storage(self):
    return self._cfg_storage
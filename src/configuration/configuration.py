import sys
import json

class Configuration():
  def __init__(self):
    self.load_configuration()


  # Loaders
  def load_configuration(self):
    # Read from config.json
    ffn = "{}.json".format('config')
    with open(ffn, 'rt') as ws:
      self.cfg = json.load(ws)

    # Set paths for access modules outside of the application
    for path in self.cfg['modules']:
      sys.path.append(path)
    

  def get_input_paths(self):
    return self.cfg['images']

  def get_result_path(self):
    return self.cfg['results']

  def get_modules_paths(self):
    return self.cfg['modules']

  def get_worksheets_paths(self):
    return self.cfg['worksheets']

  def get_fsm_cfg(self):
    # Read from config.json
    ffn = self.cfg['fsm-cfg']
    with open(ffn, 'rt') as ws:
      fsm_cfg = json.load(ws)
    return fsm_cfg

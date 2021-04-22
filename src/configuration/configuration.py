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

    # Set paths for access factory and modules outside of the application
    for path in self.cfg['modules']:
      sys.path.append(path)
    
    # Till the operation-loader is not installed via pip
    sys.path.append(self.cfg['factory'])
    import factory
    self.factory = factory
  

  def get_factory(self):
    return self.factory

  def get_input_paths(self):
    return self.cfg['images']

  def get_result_path(self):
    return self.cfg['results']

  def get_modules_paths(self):
    return self.cfg['modules']

  def get_worksheets_paths(self):
    return self.cfg['worksheets']

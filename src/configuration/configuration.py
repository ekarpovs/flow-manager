import sys
import json

class Configuration():
  def __init__(self):
    self.load_configuration()


  # Loaders
  def load_configuration(self):
    # TODO read from config.json
    ffn = "{}.json".format('config')
    with open(ffn, 'rt') as ws:
      cfg = json.load(ws)


    self.factory_path = cfg['factory'] 
    self.input_paths = cfg['images']
    self.result_path = cfg['results']
    self.modules_paths = cfg['modules']
    self.worksheets_paths = cfg['worksheets']

    # Set paths for access factory and modules outside of the application
    for path in self.modules_paths:
      sys.path.append(path)
    # Till the operation-loader is not installed via pip
    sys.path.append(self.factory_path)
    import factory
    self.factory = factory
  

  # def load_config_file(self):
  #   ffn = "{}.json".format('config')
  #   with open(ffn, 'rt') as ws:
  #     cfg = json.load(ws)
  #     print(cfg)

  #   return cfg


  def get_factory(self):
    return self.factory

  def get_input_paths(self):
    return self.input_paths

  def get_result_path(self):
    return self.result_path

  def get_modules_paths(self):
    return self.modules_paths

  def get_worksheets_paths(self):
    return self.worksheets_paths

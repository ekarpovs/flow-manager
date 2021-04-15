from .converter import Converter

'''
  {
    'path': '../modules-and-worksheets/modules-common', 
    'modules': [
      {
        'name': 'common', 
        'meta': {
          'descr': '\nLocal module, contains common utility operations\n', 
          'func': [
            'empty', 
            'start', 
            'store', 
            'restore', 
            'clean', 
            'printkwargs'
          ]
        }
      }
    ]
  }  
'''

class ModulesConverter(Converter):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 

    print("MODULES-CONVERTER")


  def convert_meta(self, modules_meta):
    converted = []
    for i, set in enumerate(modules_meta):
      iid = "p{}".format(i)
      tl_item = self.top_level_item(iid, set)
      converted.append(tl_item)
      modules = set['modules']
      for j, module in enumerate(modules):
        v1 = str(j)
        ml_item = self.module_level_item(iid, v1, module)
        converted.append(ml_item)
        md_iid = module['name']
        operations = module['meta']['func']
        for n, oper in enumerate(operations):
          v1 = str(j)+ '.'+ str(n)
          operdoc = module['meta']['meta'][n]['doc']
          oper_item = self.operation_level_item(md_iid, v1, oper, operdoc)
          converted.append(oper_item)

    return converted

  @staticmethod
  def top_level_item(iid, set):
    return {"parent":"", "index":"end", "iid":iid, "text":set['path']}


  @staticmethod
  def module_level_item(parent_iid, v1, module):
    name = module['name']
    meta = module['meta']
    return {"parent":parent_iid, "index":"end", "iid":name, "text":name, "values": [v1, meta['descr']]}

  @staticmethod
  def operation_level_item(parent_iid, v1, name, doc):
    iid = parent_iid+'.'+name
    # return {"parent":parent_iid, "index":"end", "iid":iid, "text":name, "values": [v1, "here will be func __doc__"]}
    return {"parent":parent_iid, "index":"end", "iid":iid, "text":name, "values": [v1, doc[0]]}

import re
from .converter import Converter

'''
'''

class ModulesConverter(Converter):
  def __init__(self, parent):
    super().__init__()
    self.parent = parent 


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


  @staticmethod
  def parse_single_param_defenition(param_defenition):
    # Regarding definition --Type:domein...--
    build_data = re.findall('--([^$]*)--', param_defenition)[0]
    label_text = param_defenition[len(build_data)+4:] 
    param_type, param_domain, param_possible_valuess, param_default_value =  build_data.split(';') 

    return param_type, param_domain, param_possible_valuess, param_default_value, label_text


  @staticmethod
  def convert_params_defenition_to_params(step, params_defenition, orig_image_size = (0,0)):
    oper_params = []
    for param_def in params_defenition:
      t, d, pvs, df, l = ModulesConverter.parse_single_param_defenition(param_def)
      # print("t, d, pvs, df, l", t, d, pvs, df, l)
      p_name = l.split(':')[0].strip()
      if ('params' in step) and (p_name in step['params']):
        p_value = step['params'][p_name]
        # print("p_name: p_value", p_name, p_value)
      else:
        # Check that default value is not either 'h' or 'w' -> convert to real values from image(if exists)
        (h, w) = orig_image_size
        if (h > 0) and (w > 0):
          if df == 'h':
            df = h
          if df == 'w':
            df = w

        p_value = df

      oper_params.append({"type": t, "domain": d, "p_values": pvs, "name": p_name, "value": p_value, "label": l})

    return oper_params

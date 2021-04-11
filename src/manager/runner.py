import sys
import json 

class Runner():
  def __init__(self):

    print("RUNNER")

  
  def run_flow(flow_meta):
    kwargs = {}
    steps = flow_meta['steps']
    for step in steps:
      print("step", step)
      # load the step's function
      # operation = self.model.modules_model.load_operation(step['exec'])
      # kwargs = operation(step, **kwargs)    

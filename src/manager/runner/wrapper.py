# Decorator for an operation
def flowoperation(executor):
  def executorWrapper(step, **kwargs):
    __name__ = executor.__name__
    useorig = step.get('useorig', False)

    # Use the original image as input for the operation or
    # use the prev operation output image as input for the operation
    if useorig == True:
      kwargs['image'] = kwargs['orig'].copy()
   
    kwargs = executor(step, **kwargs)
        
    return kwargs

  return executorWrapper


  
from tkinter.filedialog import askdirectory, askopenfilename, asksaveasfilename

# Data commands
  # def _assign_location(self, idx: int, name: str, io_obj:str, key: str) -> None:
  #   flow_item = self._model.flow.get_item(idx)
  #   params_def = flow_item.params_def   
  #   params = flow_item.params

  #   p = [p for p in params_def if p.get('name') == 'path' or p.get('name') == 'src' or p.get('name') == 'dest']
  #   if p is not None:
  #     self._set_image_location_to_params(io_obj, params, key)
  #   self._view.flow.create_operation_params_controls(idx, name, params, copy.deepcopy(params_def))
  #   self._bind_param_controls(params_def)
  #   self._apply(None)
  #   return
  
  # def _get_io_object(self) -> None:
  #   init_dir = self._cfg.input_paths
  #   idx, name = self._view.flow.get_current_selection_tree()
  #   flow_item = self._model.flow.get_item(idx)
  #   params_def = flow_item.params_def
  #   io_obj = ''
  #   full = False
  #   key = ''
  #   for p_def in params_def:
  #     key = p_def.get('name')
  #     if key == 'src' or key == 'dest':
  #       full = True
  #       break;
  #   if full and key == 'src':
  #     io_obj = self._get_full_file_name(init_dir)
  #   elif full and key == 'dest':
  #     io_obj = self._store_to(init_dir)
  #   else:
  #     io_obj = self._get_directory(init_dir)
  #   if io_obj != '':
  #     self._assign_location(idx, name, io_obj, key)
  #   return

  # def _get_directory(self, init_dir: str) -> str:
  #   dir = askdirectory(initialdir=init_dir)
  #   return dir

  # def _get_full_file_name(self, init_dir: str) -> str:
  #   ffn = askopenfilename(initialdir=init_dir, title="Select a file", filetypes=self._file_types)
  #   return ffn

  # def _store_to(self, init_dir: str) -> str:
  #   ffn = asksaveasfilename(initialdir = init_dir, initialfile = '', defaultextension=".tiff", filetypes=self._file_types)
  #   return ffn

  # @property
  # def _file_types(self) -> str:
  #   return (("image files","*.png"), 
  #           ("image files","*.jpeg"), 
  #           ("image files","*.jpg"), 
  #           ("image files","*.tiff"), 
  #           ("json files","*.json"), 
  #           ("all files","*.*"))

# Flow-manager

Desktop application for create, edit, debug and tuning a flow by combination existing operations.
It is part of the [Image Processing Workshop](https://github.com/ekarpovs/image-processing-workshop) project.

## Installation

Following packages from the [Image Processing Workshop](https://github.com/ekarpovs/image-processing-workshop) have to be installed locally:

- flow_runner
- operation_loader

## Configurate

Edit config.json from . folder:

```json
{
  "modules": [
    "path_to<modules>",
    "path_to<modules-common>"
  ],
  "worksheets": [
    "path_to<worksheets>",
    "path_to<another_set_of_worksheets>"
  ],
  "images": [
    "path_to<input>",
    "path_to<another_folder_with_images>"
  ],
  "fsm-cfg": "path_to<fsm-cfg.json>"
}
```

## Run

```bash
cd flow-manager
python run.py
```

## Work

The flow-manager is in MVP status at present.

Following features are available:

- Load images
- Load a worksheet from defined folders
- Convert a worksheet to corresponding workflow
- Create/Edit workflow definition
- Run a whole workflow
- Run a workflow step by step
- Playback a workflow
- Edit/Restore/Set Default an operation's parameters
- Edit/Restore/Set Default an operation's parameters during running by step or playback

Constarains:

- Only worksheet that defines linear workflow can be processed
- UI state is not managed (Pretty much UI elements are enabled permanently)

## Road map

- [x] Implement data link (links) editor
- [x] Improve operation parameters editor builder (add combo boxes, sliders, etc)
- [x] Change flow listview to tree view
- [x] Improve data view with matplotlib
- [ ] Implement Global Statements (IF, FOR, WHILE...)
- [ ] Extend Flow Storage by h5py DB

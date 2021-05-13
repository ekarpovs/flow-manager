# Flow-manager

Desktop application for create, edit, debug and tuning a flow by combination existing operations.

## Installation

Following packages from the image processing workshop have to be installed localy:

- flow_runner
- operation_loader

## Configurate

Edit config.json from . folder:

```json
{
  "factory": "path_to<operation-loader>",
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
  "results": "path_to<output>"
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
- Create/Edit worksheets
- Run a whole worksheet
- Run a worksheet by step
- Playback a worksheet
- Edit/restore an operation's parameters
- Edit/restore an operation's parameters during running by step or playback

Constarains:

- Only worksheet that defines linear workflow can be processed
- UI state is not managed (Pretty much UI elements are enabled permanently)

## Road map

- Fix existing bugs
- Implement Statements (IF, FOR, WHILE...) for possibility to create more complicated workflows
- Improve operation parameters editor builder (add combo boxes, sliders, etc)
- Implement more modules
- Implement more worksheets for perform standard tasks

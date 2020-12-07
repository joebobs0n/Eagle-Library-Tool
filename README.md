# Eagle-Library-Tool

## Checklist
- [ ] **Menus**
  - [x] File
    - [x] Load - Loads in a library file.
      - [x] Closes out any current working library (see `Close` below).
      - [x] Prompts user with open file dialog.
      - [x] If the file does not `*.lbr`, nothing happens.
      - [x] When loaded, if `save_opened_as_same_file` is set in `settings.json`, then the same file will be used as the `export` file; otherwise, upon `export`, the user will be prompted with a save dialog to provide the save file name.
    - [x] Export - Exports the current working library to a `*.lbr` file.
      - [x] The current working library is exported to the internally saved save file name.
        - [x] If no save file name is specified (either through previous `export`/`export as` or `save_opened_as_same_file` setting), then `export as` is called.
      - [x] Writes `XML` to `*.lbr` file with appropriate header.
    - [x] Export As - Prompts user for targeted export.
      - [x] Prompts user with save file dialog and saves name temporarily.
      - [x] Checks to see if filename is `*.lbr` and not empty string.
      - [x] Saves filename internally as save target.
      - [x] Writes `XML` to `*.lbr` file with appropriate header.
    - [x] Close - Closes out current working library from window.
      - [x] Prompts user if they want to close current working library if there are unsaved changes.
        - [x] If reply is `Yes`, library is closed out without `export`.
        - [x] If reply is `Save`, library is closed out after `export`.
        - [x] If reply is `Cancel`, nothing is done.
    - [x] Exit - User selectes exit through menu option.
      - [x] Prompts user if they want to save before exit if there are unsaved changes.
        - [x] If reply is `Save`, program is exited after `export`.
        - [x] If reply is `Discard`, program is exited without `export`
        - [x] if reply is `Cancel`, nothing is done.
    - [x] Close event - User presses `X` in window corner or `ALT+F4`
      - [x] `Exit` functionality called
  - [ ] Tools
    - [ ] Bulk User Value Enabler
      - [ ] Opens new tool window.
      - [ ] Upon closing window, makes changes to current working library.
      - [ ] Updates internal flag indicating new changes.
    - [ ] Bulk Name Prefix Setter
      - [ ] Opens new tool window.
      - [ ] Upon closing window, makes changes to current working library.
      - [ ] Updates internal flag indicating new changes.
    - [ ] Library Merger
      - [ ] Opens new tool window.
      - [ ] Upon closing window, makes changes to current working library.
      - [ ] Updates internal flag indicating new changes.
  - [ ] Help
    - [x] GitHub - Opens OS default web browser to [GitHub page](https://github.com/joebobs0n/Eagle-Library-Tool).
    - [ ] README - Displays this project's `README.md` file.
    - [x] Contact Me - Opens information dialog with contact information.
    - [ ] About - Opens information dialog with information about the application.
      - [X] License
      - [ ] Version

</br>

- [ ] **Operation**
  - [ ] Library Loading
    - [x] Device list populated
      - [x] According to settings, first option in list is selected.
    - [x] Status label updated
  - [ ] Device selected (manually or automatically)
    - [x] Footprint list populated
      - [x] According to settings, first option in list is selected.
    - [x] `self.selected_device_obj` saved
      - [x] device footnote updated
    - [x] `self.selected_symbol_obj` saved
      - [x] symbol footnote updated
      - [ ] symbol drawn
  - [ ] Footprint selected (manually or automatically)
    - [x] `self.selected_footprint_obj` saved
      - [x] footprint footnote updated
      - [ ] footprint drawn

</br>

- [ ] **Known Issues/Bugs**
  - [ ] `device_footnotes` and `footprint_footnotes` not updating correctly
  - When:
    - `settings.json` set to not load first on list population
    - `testLib.lbr` loaded
    - Selected `C_CHIP` or `R_CHIP`
    - Selected `0603` or `0805`
    - Then select `C_CHIP` or `R_CHIP`
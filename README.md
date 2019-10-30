# Productivity / Activity Tracker

Simple GUI Python app to help keep track of what you work on and for how long
Application can be exited at the end of the day and saves tasks to CSV

Created by: Haard Shah

## Running

```bash
python3 app.py
```

**ALSO**
> Must be executed from within the folder because of fileIO and the use of `AutocompleteEntry.py`

## Sample

Application
![Application](sample.png)

Persistent (stores tasks in CSV)
![csvSample](csvsample.png)

## Modules used
- `humanize=0.5.1`

> default Python packages
- `tkinter`
- `datetime`
- `os`
- `csv`

## Next

- Add colors / Prettify everything
- Ability to delete tasks from current session
- Ability to VOID current running task
- Scroll (autocomplete listbox in `AutocompleteEntry.py`)
- Scroll (main window if there are too many tasks)
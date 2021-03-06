# The Productivity Czar

Simple GUI Python app to help keep track of what you work on and for how long. ProductivityCzar is persistant so it can be exited at the end of the day and saves tasks to CSV.

Created by: Haard Shah

![](images/productivityCzar.gif)

## Running

```bash
python3 <path-to-file>/app.py
```

## Sample

Application


![Application](images/sample.png "Productivity App")

Autocomplete


![Autocomplete](images/autocomplete.png "Autocomplete Feature")

Persistent (stores tasks in CSV)


![csvSample](images/csvsample.png "Persistent Storage")

## Modules used

> default Python packages
- `tkinter`
- `datetime`
- `os`
- `csv`

> Might use in future (**not using yet**)
- `humanize==0.5.1`
- `PyTweening==1.0.3`


## Next

- Add colors / Prettify everything
- Ability to delete tasks from current session
- Ability to VOID current running task
- Scroll (autocomplete listbox in `AutocompleteEntry.py`)
- Scroll (main window if there are too many tasks)

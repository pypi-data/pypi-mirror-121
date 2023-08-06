# autosave

## Installation

```sh
pip install autosave
```

## Example

```py
from autosave import File, AppStorage



# When editing multiple entries,
# use a with statement to only save on exit.

with File('my_file.json') as data:
    data['dessert'] = 'pancakes'
    data['genre'] = 'jazz'


# By indexing entries on their own, the file is saved on each edit.
# This is adviced against if you're editing multiple entries at a time,
# as it is much less performant.

file = File('my_file.json')

file['garbage'] = 'smooth' + file['genre']


# Get access to the right directories for your app,
# by using this wrapper around `appdirs`

app = AppStorage('MyApp')
app.data / 'plugins/baguette.json'
```
# Contributing

```bash
pamac install tk
```

```bash
# Install the Python package virtualenv
pip install virtualenv
# Create a new virtual environment
virtualenv venv-time-journal
# Active the environment
source venv-time-journal/bin/activate
# Install dependencies
pip install -r requirements.txt
```

## Building with PyInstaller

```bash
pyinstaller TimeJournal.py --name "TimeJournal v0.1.2-alpha" --hidden-import='PIL._tkinter_finder' --hiddenimport=['sqlalchemy.sql.default_comparator'] --add-data "assets:assets"
```

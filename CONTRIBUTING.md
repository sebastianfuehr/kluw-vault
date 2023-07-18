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
source venv-time-journal/bin/activate # Linux
venv-time-journal\Scripts\activate # Windows
# Install dependencies
pip install -r requirements.txt
```

## Building with PyInstaller

Linux:

```bash
# Arch Linux
pyinstaller app.py --name "TimeJournal v0.1.3-alpha" --hidden-import='PIL._tkinter_finder' --add-data "assets:assets"
# Windows
pyinstaller app.py --name "TimeJournal v0.1.3-alpha" --hidden-import='PIL._tkinter_finder' --hiddenimport=['sqlalchemy.sql.default_comparator'] --add-data "assets;assets"
```

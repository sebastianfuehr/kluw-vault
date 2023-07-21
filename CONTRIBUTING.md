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

## Testing

Instead of running `python -m unittest -v`, use `coverage run -m unittest -v` instead. This will measure the test coverage of the unit tests. To generat a report for the Coverage Gutter plugin, run `coverage xml`. Then VS Code should show the test coverage. `coverage report` will print an overview table to the console output. Pay attention to the fact that files are not listed, if they have 0% coverage (no test referencing them).

## Building with PyInstaller

Linux:

```bash
# Arch Linux
pyinstaller app.py --name "TimeJournal v0.1.3-alpha" --hidden-import='PIL._tkinter_finder' --add-data "assets:assets"
# Windows
pyinstaller app.py --name "TimeJournal v0.1.3-alpha" --hidden-import='PIL._tkinter_finder' --hiddenimport=['sqlalchemy.sql.default_comparator'] --add-data "assets;assets"
```

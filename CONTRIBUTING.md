# Contributing to the Time Journal

Welcome, and thank you for your interest in contributing to the time journal!

There are many ways in which you can contribute, beyond writing code. The goal of this document is to provide a high-level overview of how you can get involved.

## Reporting Issues

Have you identified a reproducible problem in the time journal? Please let me know! Here's how you can make reporting your issue as effective as possible (taken from [VS Code](https://github.com/microsoft/vscode/blob/cf4c4a0ece70d221d907a2bc0042cc164f73bb0c/CONTRIBUTING.md)).

### Look For an Existing Issue

Before you create a new issue, please do a search in [open issues](https://github.com/sebastianfuehr/time-journal-gui-app/issues) to see if the issue or feature request has already been filed.

Be sure to scan through the [most popular](https://github.com/sebastianfuehr/time-journal-gui-app/issues?q=is%3Aopen+is%3Aissue+label%3Afeature-request+sort%3Areactions-%2B1-desc+) feature requests.

If you find your issue already exists, make relevant comments and add your [reaction](https://github.blog/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/). Use a reaction in place of a "+1" comment:

👍 - upvote
👎 - downvote

If you cannot find an existing issue that describes your bug or feature, create a new issue using the guidelines below.

### Writing Good Bug Reports

File a single issue per problem and feature request. Do not enumerate multiple bugs or feature requests in the same issue.

Do not add your issue as a comment to an existing issue unless it's for the identical input. Many issues look similar, but have different causes.

The more information you can provide, the more likely someone will be successful at reproducing the issue and finding a fix.

Please include the following with each issue:

- Version of the time journal
- Your operating system
- Reproducible steps (1... 2... 3...) that cause the issue
- What you expected to see, versus what you actually saw
- Images, animations, or a link to a video showing the issue occurring
- If possible: A code snippet that demonstrates the issue or a link to a code repository the developers can easily pull down to recreate the issue locally
    - Note: Because the developers need to copy and paste the code snippet, including a code snippet as a media file (i.e. .gif) is not sufficient.

Here is a GitHub Markdown snipped which you can use as a template:

```Markdown
**Version:** Version number
**OS:** Operating system

**Reproducible steps:**

1. ...

**Expected behavior:** ...

**Experienced behavior:** ...

Additional information, like code snippets or screenshots.
```

### Final Checklist

Please remember to do the following:

- [ ] Search the issue repository to ensure your report is a new issue
- [ ] Recreate the issue to make sure it is repricable
- [ ] Simplify your code around the issue to better isolate the problem

### Follow Your Issue

Check in on your opened issue from time to time, in case that someone has a follow-up question.

## Translating

First of all, **do not touch the `base.pot` file!** `.pot` files are pure templates and should not be altered. This project uses `pybabel` to generate translations.

```bash
# Extract the strings from the source code
pybabel extract . -o locales/base.pot --ignore-dirs=<virtualenv-directory>
# Update the extracted variables
pybabel update -i locales/base.pot -d locales
# Create a new locale, if it doesn't exist yet
pybabel init -l <locale-name> -i locales/base.pot -d locales
# Create the binary files with the translations
pybabel compile -l <locale-name> -d locales
```

## Setup Development Environment

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

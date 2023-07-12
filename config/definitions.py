import os

APP_VERSION = 'v0.1.2-alpha'

APP_ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# Medal thresholds in seconds (h*m*s)
MEDAL_TH_BRONZE = 2*60*60
MEDAL_TH_SILVER = 4*60*60
MEDAL_TH_GOLD = 6*60*60

#######################################################################
# STYLING & LAYOUT
#######################################################################

# Font options
DASHBOARD_HEADING_SIZE = 24
FORM_HEADING_FONT = (None, 24, 'bold')
COMBO_BOX_FONT = (None, 16)
FONTS = {
    'default': (None, 16)
}

# Simple color name-value pairs
COLORS = {
    'text': 'white',
    'highlight': '#21eaad'
}
# Color combinations for specific components
COMPONENT_COLORS = {
    'list-item': {'text': COLORS['text'], 'highlight': COLORS['highlight']}
}

# MENUS
MAINFRAME_TABS_NAV = {
    'elements': ['Dashboard', 'Time Entries', 'Projects', 'Categories'],
    'padx': (40, 0),
    'pady': 20,
    'side': 'left',
    'anchor': 'w',
    'font': (None, 20),
    'colors': COMPONENT_COLORS['list-item']
}
FILTER_PERIODS = {
    'elements': ['Max', '1 Year', '6 Months', 'Month', 'Week'],
    'padx': 10,
    'pady': 10,
    'side': 'right',
    'anchor': 'w',
    'font': FONTS['default'],
    'colors': COMPONENT_COLORS['list-item']
}

# TABS
TAB_FRAME_LIST = {
    'sidebar': {'col': 0, 'row': 0, 'sticky': 'nsew'},
    'form': {'col': 0, 'row': 0, 'sticky': 'nsew'},
    'button': {'col': 0, 'row': 0, 'pady': 20},
    'separators': [
        {'col': 0, 'row': 1, 'orient': 'horizontal', 'sticky': 'ew', 'rowspan': 1},
        {'col': 1, 'row': 0, 'orient': 'vertical', 'sticky': 'ns', 'rowspan': 3}
    ]
}

LIST_ITEM = {
    'padx': 10,
    'pady': (20, 0),
    'side': 'top',
    'anchor': 'w',
    'font': FONTS['default'],
    'colors': COMPONENT_COLORS['list-item']
}

# FORMS
FORM_BTN_CLOSE = {'text': 'X', 'font': (None, 24), 'relx': 0.98, 'rely': 0.02, 'anchor': 'ne'}

FORM_STYLING = {
    'label': {},
    'entry': {},
    'combobox': {}
}

FORM_PROJECT_EDIT = {
    'rowconfigure': {0: 1, 8: 1},
    'columnconfigure': {0: 1, 2: 1},
    'labels': [
        {'text': 'Name', 'row': 1, 'col': 1, 'sticky': 'ew'},
        {'text': 'Description', 'row': 3, 'col': 1, 'sticky': 'ew'},
        {'text': 'Project Category', 'row': 5, 'col': 1, 'sticky': 'ew'}
    ],
    'inp_name': {'row': 2, 'col': 1},
    'inp_description': {'row': 4, 'col': 1},
    'inp_category': {'row': 6, 'col': 1},
    'btn_save': {'row': 7, 'col': 1}
}

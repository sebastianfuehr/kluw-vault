import os

APP_VERSION = 'v0.1.2-alpha'
CONFIG_FILE_VERSION = 1

APP_ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
APP_USER_DATA_FILE = os.path.join(os.getenv('HOME'), '.config', 'time-journal', 'config')
APP_DEFAULT_USER_DATA_FILE = os.path.join(APP_ROOT_DIR, 'assets', 'default.ini')

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
    'default': (None, 16),
    'form': {
        'label': (None, 16),
        'entry': (None, 16),
        'combobox': (None, 16),
        'scrolledtext': (None, 16),
        'button': (None, 16)
    },
    'view': {
        'title': (None, 34, 'bold'),
        'subtitle': (None, 30, 'bold'),
        'label': (None, 16, 'bold'),
        'text': (None, 16)
    }
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

# CARDS
VIEW_BTN_EDIT = {
    'text': 'Edit',
    'relx': 0.98,
    'rely': 0.02,
    'anchor': 'ne'
}

lbl_pady = (0, 25)
inp_pady = (5, 30)
VIEW_PROJECT_DETAIL = {
    'grid-config': {
        'rowconfigure': {},
        'columnconfigure': {0: 1, 2: 1}
    },
    'labels': [
        {'text': 'Total Time', 'row': 1, 'rowspan': 1, 'col': 0, 'columnspan': 1, 'sticky': 'w', 'padx': 0, 'pady': lbl_pady, 'font': FONTS['view']['label']},
        {'text': 'Category', 'row': 2, 'rowspan': 1, 'col': 0, 'columnspan': 2, 'sticky': 'w', 'padx': 0, 'pady': lbl_pady, 'font': FONTS['view']['label']},
        {'text': 'Description', 'row': 4, 'rowspan': 1, 'col': 0, 'columnspan': 2, 'sticky': 'w', 'padx': 0, 'pady': lbl_pady, 'font': FONTS['view']['label']},
        {'text': 'Activities', 'row': 2, 'rowspan': 1, 'col': 2, 'columnspan': 2, 'sticky': 'w', 'padx': 0, 'pady': lbl_pady, 'font': FONTS['view']['label']},
        {'text': 'Statistics', 'row': 6, 'rowspan': 1, 'col': 0, 'columnspan': 4, 'sticky': 'w', 'padx': 0, 'pady': (35, 10), 'font': FONTS['view']['subtitle']}
    ],
    'lbl_name': {'row': 0, 'rowspan': 1, 'col': 0, 'columnspan': 4, 'sticky': 'w', 'padx': 0, 'pady': (35, 20), 'font': FONTS['view']['title']}
}

# FORMS
FORM_BTN_CLOSE = {
    'text': 'X',
    'font': (None, 24),
    'relx': 0.98,
    'rely': 0.02,
    'anchor': 'ne'
}

lbl_pady = 0
inp_pady = (5, 30)
FORM_PROJECT_EDIT = {
    'grid-config': {
        'rowconfigure': {0: 1, 8: 1},
        'columnconfigure': {0: 1, 2: 1}
    },
    'labels': [
        {'text': 'Name', 'row': 1, 'rowspan': 1, 'col': 1, 'columnspan': 1, 'sticky': 'ew', 'padx': 0, 'pady': lbl_pady, 'font': FONTS['form']['label']},
        {'text': 'Description', 'row': 3, 'rowspan': 1, 'col': 1, 'columnspan': 1, 'sticky': 'ew', 'padx': 0, 'pady': lbl_pady, 'font': FONTS['form']['label']},
        {'text': 'Project Category', 'row': 5, 'rowspan': 1, 'col': 1, 'columnspan': 1, 'sticky': 'ew', 'padx': 0, 'pady': lbl_pady, 'font': FONTS['form']['label']}
    ],
    'inp_name': {'row': 2, 'col': 1, 'sticky': 'ew', 'padx': 0, 'pady': inp_pady, 'width': 40, 'font': FONTS['form']['entry']},
    'inp_description': {'row': 4, 'col': 1, 'sticky': 'ew', 'padx': 0, 'pady': inp_pady, 'height': 5, 'width': 36, 'font': FONTS['form']['scrolledtext']},
    'inp_category': {'row': 6, 'col': 1, 'sticky': 'ew', 'padx': 0, 'pady': inp_pady, 'width': 40, 'font': FONTS['form']['combobox']},
    'btn_save': {'row': 7, 'col': 1, 'sticky': '', 'padx': 0, 'pady': (25, 0), 'width': 8}
}

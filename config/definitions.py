import os

APP_VERSION = 'v0.1.2-alpha'

APP_ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# Filter options
FILTER_PERIODS = ['Max', '1 Year', '6 Months', 'Month', 'Week']

# Medal thresholds in seconds (h*m*s)
MEDAL_TH_BRONZE = 2*60*60
MEDAL_TH_SILVER = 4*60*60
MEDAL_TH_GOLD = 6*60*60

#######################################################################
# STYLING
#######################################################################

# Font options
DASHBOARD_HEADING_SIZE = 24
FORM_HEADING_FONT = (None, 24, 'bold')
COMBO_BOX_FONT = (None, 16)

# Colors
TEXT_COLOR = 'white'
HIGHLIGHT_COLOR = '#21eaad'

#######################################################################
# LAYOUT
#######################################################################

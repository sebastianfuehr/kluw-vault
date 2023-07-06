import os

APP_VERSION = 'v0.1.2-alpha'

APP_ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))

# Filter options
FILTER_PERIODS = ['Max', '1 Year', '6 Months', 'Month', 'Week']

# Medal thresholds in seconds (h*m*s)
MEDAL_TH_BRONZE = 2*60*60
MEDAL_TH_SILVER = 4*60*60
MEDAL_TH_GOLD = 6*60*60

# Font options
DASHBOARD_HEADING_SIZE = 24

# Colors
TEXT_COLOR = 'white'
HIGHLIGHT_COLOR = '#21eaad'

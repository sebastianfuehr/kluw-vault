"""This module contains all kind of constants which are semi-constants.
This file pulls from constants.py and enums.py and is used by the main
entrypoint of the application app.py.
"""

import gettext
import os
import sys

from config.constants import CONFIG_FILE_VERSION
from src.controller.settings_controller import SettingsController


class Definitions:
    """A class that loads and provides user settings and dynamically
    created properties.
    """

    # DIRECTORIES
    # APP_ROOT_DIR = os.path.realpath(os.path.join(os.path.dirname(__file__), '..'))
    APP_ROOT_DIR = os.path.dirname(os.path.realpath(sys.argv[0]))

    #######################################################################
    # STYLING & LAYOUT
    #######################################################################

    # Font options
    DASHBOARD_HEADING_SIZE = 24
    FORM_HEADING_FONT = (None, 24, "bold")
    COMBO_BOX_FONT = (None, 16)
    FONTS = {
        "default": (None, 16),
        "dashboard": {"heading": ("Nimbus Sans", 24, "bold")},
        "form": {
            "label": (None, 16),
            "entry": (None, 16),
            "combobox": (None, 16),
            "scrolledtext": (None, 16),
            "button": (None, 16),
        },
        "view": {
            "title": (None, 34, "bold"),
            "subtitle": (None, 30, "bold"),
            "section": (None, 16, "bold"),
            "label": (None, 16),
            "text": (None, 16),
        },
    }

    # Simple color name-value pairs
    COLORS = {"text": "white", "highlight": "#21eaad"}
    # Color combinations for specific components
    COMPONENT_COLORS = {
        "list-item": {"text": COLORS["text"], "highlight": COLORS["highlight"]}
    }

    # COMPONENTS
    CUSTOM_ENTITIY_ITEM_LIST = {
        "separators": [
            {"col": 0, "row": 0, "orient": "horizontal", "sticky": "ew", "rowspan": 1},
            {"col": 0, "row": 2, "orient": "horizontal", "sticky": "ew", "rowspan": 1},
        ]
    }

    # MENUS
    FILTER_PERIODS = {
        "elements": ["Max", "1 Year", "6 Months", "Month", "Week"],
        "padx": 10,
        "pady": 10,
        "side": "right",
        "anchor": "w",
        "font": FONTS["default"],
        "colors": COMPONENT_COLORS["list-item"],
    }

    # TABS
    TAB_FRAME_LIST = {
        "sidebar": {"col": 0, "row": 0, "sticky": "nsew"},
        "form": {"col": 0, "row": 0, "sticky": "nsew"},
        "button": {"col": 0, "row": 0, "pady": 20},
        "separators": [
            {"col": 0, "row": 1, "orient": "horizontal", "sticky": "ew", "rowspan": 1},
            {"col": 1, "row": 0, "orient": "vertical", "sticky": "ns", "rowspan": 3},
        ],
    }

    LIST_ITEM = {
        "padx": 10,
        "pady": 10,
        "side": "top",
        "anchor": "w",
        "font": FONTS["default"],
        "colors": COMPONENT_COLORS["list-item"],
    }

    def load_config(self):
        config = SettingsController.load_or_create_config_file(
            self.APP_ROOT_DIR, CONFIG_FILE_VERSION
        )

        print(f"Loading language {config['DEFAULT']['language']} from user settings")
        locale = gettext.translation(
            "messages", localedir="locales", languages=[config["DEFAULT"]["language"]]
        )
        locale.install()
        _ = locale.gettext

        self.generate_config_based_settings(config)
        return config

    def generate_config_based_settings(self, config):
        """Generate application settings, which are based on user
        settings, for example font size or translated label texts,
        based on the preferred language.
        """
        # Medal thresholds in seconds (h*m*s)
        medal_ths = config["gamification.rewards"]
        self.MEDAL_TH_BRONZE = (
            medal_ths.getint("medal_bronze_unit_amount")
            * medal_ths.getint("medal_bronze_unit_length")
            * 60
        )
        self.MEDAL_TH_SILVER = (
            medal_ths.getint("medal_silver_unit_amount")
            * medal_ths.getint("medal_silver_unit_length")
            * 60
        )
        self.MEDAL_TH_GOLD = (
            medal_ths.getint("medal_gold_unit_amount")
            * medal_ths.getint("medal_gold_unit_length")
            * 60
        )

        # MENUS
        self.MAINFRAME_TABS_NAV = {
            "elements": {
                "dashboard": "Dashboard",
                "time-entries": _("Time Entries"),
                "projects": _("Projects"),
                "categories": _("Categories"),
            },
            "padx": (40, 0),
            "pady": 20,
            "side": "left",
            "anchor": "w",
            "font": (None, 20),
            "colors": self.COMPONENT_COLORS["list-item"],
        }

        # CARDS
        heading_padx = 0
        heading_pady = (0, 5)
        graph_padx = 9
        graph_pady = 0
        self.VIEW_DASHBOARD = {
            "grid-config": {"rowconfigure": {}, "columnconfigure": {(0, 1): 1}},
            "labels": [
                {
                    "text": "📰 " + _("Overview"),
                    "row": 0,
                    "rowspan": 1,
                    "col": 0,
                    "columnspan": 1,
                    "sticky": "w",
                    "padx": heading_padx,
                    "pady": heading_pady,
                    "font": self.FONTS["dashboard"]["heading"],
                },
                {
                    "text": "🗓️ " + _("Time per Day"),
                    "row": 0,
                    "rowspan": 1,
                    "col": 1,
                    "columnspan": 1,
                    "sticky": "w",
                    "padx": heading_padx,
                    "pady": heading_pady,
                    "font": self.FONTS["dashboard"]["heading"],
                },
                {
                    "text": "📈 " + _("Time per Day per Project"),
                    "row": 4,
                    "rowspan": 1,
                    "col": 1,
                    "columnspan": 1,
                    "sticky": "w",
                    "padx": heading_padx,
                    "pady": heading_pady,
                    "font": self.FONTS["dashboard"]["heading"],
                },
                {
                    "text": "🏅" + _("Medal Score"),
                    "row": 2,
                    "rowspan": 1,
                    "col": 0,
                    "columnspan": 1,
                    "sticky": "w",
                    "padx": heading_padx,
                    "pady": heading_pady,
                    "font": self.FONTS["dashboard"]["heading"],
                },
            ],
            "medal_score": {
                "row": 3,
                "rowspan": 3,
                "col": 0,
                "columnspan": 1,
                "sticky": "nsew",
                "padx": graph_padx,
                "pady": graph_pady,
            },
            "graph_time_per_day": {
                "row": 1,
                "rowspan": 3,
                "col": 1,
                "columnspan": 1,
                "sticky": "nsew",
                "padx": graph_padx,
                "pady": graph_pady,
            },
            "graph_time_per_project_per_day": {
                "row": 5,
                "rowspan": 1,
                "col": 1,
                "columnspan": 1,
                "sticky": "nsew",
                "padx": graph_padx,
                "pady": graph_pady,
            },
        }

        self.VIEW_BTN_EDIT = {
            "text": _("Edit"),
            "relx": 0.98,
            "rely": 0.02,
            "anchor": "ne",
        }

        lbl_pady = (0, 25)
        inp_pady = (5, 30)
        self.VIEW_PROJECT_DETAIL = {
            "grid-config": {"rowconfigure": {}, "columnconfigure": {0: 1, 2: 1}},
            "labels": [
                {
                    "text": _("Total time:"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 0,
                    "columnspan": 1,
                    "sticky": "w",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["view"]["section"],
                },
                {
                    "text": _("Category"),
                    "row": 2,
                    "rowspan": 1,
                    "col": 0,
                    "columnspan": 2,
                    "sticky": "w",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["view"]["section"],
                },
                {
                    "text": _("Description"),
                    "row": 4,
                    "rowspan": 1,
                    "col": 0,
                    "columnspan": 2,
                    "sticky": "w",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["view"]["section"],
                },
                {
                    "text": _("Activities"),
                    "row": 2,
                    "rowspan": 1,
                    "col": 2,
                    "columnspan": 2,
                    "sticky": "w",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["view"]["section"],
                },
                {
                    "text": _("Statistics"),
                    "row": 6,
                    "rowspan": 1,
                    "col": 0,
                    "columnspan": 4,
                    "sticky": "w",
                    "padx": 0,
                    "pady": (35, 10),
                    "font": self.FONTS["view"]["subtitle"],
                },
                {
                    "text": "🗓️ " + _("Time per Day"),
                    "row": 7,
                    "rowspan": 1,
                    "col": 0,
                    "columnspan": 4,
                    "sticky": "w",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["view"]["section"],
                },
            ],
            "lbl_name": {
                "row": 0,
                "rowspan": 1,
                "col": 0,
                "columnspan": 4,
                "sticky": "w",
                "padx": 0,
                "pady": (35, 20),
                "font": self.FONTS["view"]["title"],
            },
            "lbl_category": {
                "row": 3,
                "rowspan": 1,
                "col": 0,
                "columnspan": 2,
                "sticky": "w",
                "padx": 0,
                "pady": lbl_pady,
                "font": self.FONTS["view"]["label"],
            },
            "lbl_description": {
                "row": 5,
                "rowspan": 1,
                "col": 0,
                "columnspan": 2,
                "sticky": "w",
                "height": 5,
                "width": 36,
                "padx": 0,
                "pady": lbl_pady,
                "font": self.FONTS["view"]["label"],
            },
            "lst_activities": {
                "row": 3,
                "rowspan": 3,
                "col": 2,
                "columnspan": 2,
                "sticky": "nsew",
                "padx": 0,
                "pady": lbl_pady,
                "font": self.LIST_ITEM,
            },
            "graph_time_per_day": {
                "row": 8,
                "rowspan": 1,
                "col": 0,
                "columnspan": 4,
                "sticky": "nsew",
                "padx": 0,
                "pady": lbl_pady,
            },
            # This refers to the grid method of the master component of this view!
            "frm_edit_activity": {
                "row": 0,
                "rowspan": 8,
                "col": 0,
                "columnspan": 4,
                "sticky": "nsew",
                "padx": 0,
                "pady": 0,
            },
        }

        self.VIEW_PROJECT_CATEGORY_DETAIL = {
            "grid-config": {"rowconfigure": {}, "columnconfigure": {0: 1, 2: 1}},
            "labels": [
                {
                    "text": _("Total time:"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 0,
                    "columnspan": 1,
                    "sticky": "w",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["view"]["section"],
                },
                {
                    "text": _("Description"),
                    "row": 2,
                    "rowspan": 1,
                    "col": 0,
                    "columnspan": 2,
                    "sticky": "w",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["view"]["section"],
                },
                {
                    "text": _("Goals"),
                    "row": 4,
                    "rowspan": 1,
                    "col": 0,
                    "columnspan": 4,
                    "sticky": "w",
                    "padx": 0,
                    "pady": (35, 10),
                    "font": self.FONTS["view"]["subtitle"],
                },
                {
                    "text": _("Projects"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 2,
                    "columnspan": 2,
                    "sticky": "w",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["view"]["section"],
                },
                {
                    "text": _("Statistics"),
                    "row": 6,
                    "rowspan": 1,
                    "col": 0,
                    "columnspan": 4,
                    "sticky": "w",
                    "padx": 0,
                    "pady": (35, 10),
                    "font": self.FONTS["view"]["subtitle"],
                },
            ],
            "lbl_name": {
                "row": 0,
                "rowspan": 1,
                "col": 0,
                "columnspan": 4,
                "sticky": "w",
                "padx": 0,
                "pady": (35, 20),
                "font": self.FONTS["view"]["title"],
            },
            "lbl_description": {
                "row": 3,
                "rowspan": 1,
                "col": 0,
                "columnspan": 2,
                "sticky": "w",
                "height": 5,
                "width": 36,
                "padx": 0,
                "pady": lbl_pady,
                "font": self.FONTS["view"]["label"],
            },
            "lst_projects": {
                "row": 2,
                "rowspan": 2,
                "col": 2,
                "columnspan": 2,
                "sticky": "nsew",
                "padx": 0,
                "pady": lbl_pady,
                "font": self.LIST_ITEM,
            },
            "lst_goals": {
                "row": 5,
                "rowspan": 1,
                "col": 0,
                "columnspan": 4,
                "sticky": "ew",
                "padx": 0,
                "pady": lbl_pady,
            },
            # This refers to the grid method of the master component of this view!
            "frm_edit_activity": {
                "row": 0,
                "rowspan": 8,
                "col": 0,
                "columnspan": 4,
                "sticky": "nsew",
                "padx": 0,
                "pady": 0,
            },
        }

        # Represents a table of category goals
        first_lbl_col = 0
        lbl_sticky = "ew"
        lbl_padx = 0
        lbl_pady = 0
        self.VIEW_PROJECT_CATEGORY_GOAL_DETAIL = {
            "grid_config": {
                "rowconfigure": {},
                "columnconfigure": {(0, 1, 2, 3, 4, 5, 6): 1},
            },
            "separators": [
                {
                    "col": 0,
                    "columnspan": 8,
                    "row": 1,
                    "rowspan": 1,
                    "orient": "horizontal",
                    "sticky": "ew",
                    "columnspan": 8,
                },
                {
                    "col": 0,
                    "columnspan": 8,
                    "row": 3,
                    "rowspan": 1,
                    "orient": "horizontal",
                    "sticky": "ew",
                    "columnspan": 8,
                },
            ],
            "labels": [
                {
                    "text": _("Mon"),
                    "row": 0,
                    "rowspan": 1,
                    "col": first_lbl_col,
                    "columnspan": 1,
                    "sticky": lbl_sticky,
                    "padx": lbl_padx,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Tue"),
                    "row": 0,
                    "rowspan": 1,
                    "col": first_lbl_col + 1,
                    "columnspan": 1,
                    "sticky": lbl_sticky,
                    "padx": lbl_padx,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Wed"),
                    "row": 0,
                    "rowspan": 1,
                    "col": first_lbl_col + 2,
                    "columnspan": 1,
                    "sticky": lbl_sticky,
                    "padx": lbl_padx,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Thu"),
                    "row": 0,
                    "rowspan": 1,
                    "col": first_lbl_col + 3,
                    "columnspan": 1,
                    "sticky": lbl_sticky,
                    "padx": lbl_padx,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Fri"),
                    "row": 0,
                    "rowspan": 1,
                    "col": first_lbl_col + 4,
                    "columnspan": 1,
                    "sticky": lbl_sticky,
                    "padx": lbl_padx,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Sat"),
                    "row": 0,
                    "rowspan": 1,
                    "col": first_lbl_col + 5,
                    "columnspan": 1,
                    "sticky": lbl_sticky,
                    "padx": lbl_padx,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Sun"),
                    "row": 0,
                    "rowspan": 1,
                    "col": first_lbl_col + 6,
                    "columnspan": 1,
                    "sticky": lbl_sticky,
                    "padx": lbl_padx,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
            ],
            "row_min_label": {
                "row": 2,
                "col": first_lbl_col,
                "sticky": lbl_sticky,
                "padx": lbl_padx,
                "pady": lbl_pady,
                "width": None,
                "font": self.FONTS["form"]["entry"],
            },
            "btn_edit": {
                "row": 2,
                "col": first_lbl_col + 7,
                "sticky": "",
                "padx": 0,
                "pady": 0,
                "width": 8,
            },
        }

        # FORMS
        self.FORM_BTN_CLOSE = {
            "text": "X",
            "font": (None, 24),
            "relx": 0.98,
            "rely": 0.02,
            "anchor": "ne",
        }

        lbl_pady = 0
        inp_pady = (5, 30)
        self.FORM_PROJECT_EDIT = {
            "grid-config": {
                "rowconfigure": {0: 1, 8: 1},
                "columnconfigure": {0: 1, 2: 1},
            },
            "labels": [
                {
                    "text": _("Name"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 1,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Description"),
                    "row": 3,
                    "rowspan": 1,
                    "col": 1,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Project Category"),
                    "row": 5,
                    "rowspan": 1,
                    "col": 1,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
            ],
            "inp_name": {
                "row": 2,
                "col": 1,
                "sticky": "ew",
                "padx": 0,
                "pady": inp_pady,
                "width": 40,
                "font": self.FONTS["form"]["entry"],
            },
            "inp_description": {
                "row": 4,
                "col": 1,
                "sticky": "ew",
                "padx": 0,
                "pady": inp_pady,
                "height": 5,
                "width": 36,
                "font": self.FONTS["form"]["scrolledtext"],
            },
            "inp_category": {
                "row": 6,
                "col": 1,
                "sticky": "ew",
                "padx": 0,
                "pady": inp_pady,
                "width": 40,
                "font": self.FONTS["form"]["combobox"],
            },
            "btn_save": {
                "row": 7,
                "col": 1,
                "sticky": "",
                "padx": 0,
                "pady": (25, 0),
                "width": 8,
            },
        }

        self.FORM_ACTIVITY_EDIT = {
            "grid-config": {
                "rowconfigure": {0: 1, 6: 1},
                "columnconfigure": {0: 1, 2: 1},
            },
            "labels": [
                {
                    "text": _("Name"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 1,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Description"),
                    "row": 3,
                    "rowspan": 1,
                    "col": 1,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
            ],
            "inp_name": {
                "row": 2,
                "col": 1,
                "sticky": "ew",
                "padx": 0,
                "pady": inp_pady,
                "width": 40,
                "font": self.FONTS["form"]["entry"],
            },
            "inp_description": {
                "row": 4,
                "col": 1,
                "sticky": "ew",
                "padx": 0,
                "pady": inp_pady,
                "height": 5,
                "width": 36,
                "font": self.FONTS["form"]["scrolledtext"],
            },
            "btn_save": {
                "row": 5,
                "col": 1,
                "sticky": "",
                "padx": 0,
                "pady": (25, 0),
                "width": 8,
            },
        }

        self.FORM_PROJECT_CATEGORY_EDIT = {
            "grid-config": {
                "rowconfigure": {0: 1, 6: 1},
                "columnconfigure": {0: 1, 2: 1},
            },
            "labels": [
                {
                    "text": _("Name"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 1,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Description"),
                    "row": 3,
                    "rowspan": 1,
                    "col": 1,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
            ],
            "inp_name": {
                "row": 2,
                "col": 1,
                "sticky": "ew",
                "padx": 0,
                "pady": inp_pady,
                "width": 40,
                "font": self.FONTS["form"]["entry"],
            },
            "inp_description": {
                "row": 4,
                "col": 1,
                "sticky": "ew",
                "padx": 0,
                "pady": inp_pady,
                "height": 5,
                "width": 36,
                "font": self.FONTS["form"]["scrolledtext"],
            },
            "btn_save": {
                "row": 5,
                "col": 1,
                "sticky": "",
                "padx": 0,
                "pady": (25, 0),
                "width": 8,
            },
        }

        inp_sticky = ""
        inp_padx = 5
        inp_pady = 10
        inp_width = 10
        self.FORM_PROJECT_CATEGORY_GOAL_EDIT = {
            "grid-config": {
                "rowconfigure": {0: 1, 4: 1},
                "columnconfigure": {0: 1, 8: 1},
            },
            "labels": [
                {
                    "text": _("Monday"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 1,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Tuesday"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 2,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Wednesday"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 3,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Thursday"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 4,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Friday"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 5,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Saturday"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 6,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
                {
                    "text": _("Sunday"),
                    "row": 1,
                    "rowspan": 1,
                    "col": 7,
                    "columnspan": 1,
                    "sticky": "ew",
                    "padx": 0,
                    "pady": lbl_pady,
                    "font": self.FONTS["form"]["label"],
                },
            ],
            "inp_monday": {
                "row": 2,
                "col": 1,
                "sticky": inp_sticky,
                "padx": inp_padx,
                "pady": inp_pady,
                "width": inp_width,
                "font": self.FONTS["form"]["entry"],
            },
            "inp_tuesday": {
                "row": 2,
                "col": 2,
                "sticky": inp_sticky,
                "padx": inp_padx,
                "pady": inp_pady,
                "width": inp_width,
                "font": self.FONTS["form"]["entry"],
            },
            "inp_wednesday": {
                "row": 2,
                "col": 3,
                "sticky": inp_sticky,
                "padx": inp_padx,
                "pady": inp_pady,
                "width": inp_width,
                "font": self.FONTS["form"]["entry"],
            },
            "inp_thursday": {
                "row": 2,
                "col": 4,
                "sticky": inp_sticky,
                "padx": inp_padx,
                "pady": inp_pady,
                "width": inp_width,
                "font": self.FONTS["form"]["entry"],
            },
            "inp_friday": {
                "row": 2,
                "col": 5,
                "sticky": inp_sticky,
                "padx": inp_padx,
                "pady": inp_pady,
                "width": inp_width,
                "font": self.FONTS["form"]["entry"],
            },
            "inp_saturday": {
                "row": 2,
                "col": 6,
                "sticky": inp_sticky,
                "padx": inp_padx,
                "pady": inp_pady,
                "width": inp_width,
                "font": self.FONTS["form"]["entry"],
            },
            "inp_sunday": {
                "row": 2,
                "col": 7,
                "sticky": inp_sticky,
                "padx": inp_padx,
                "pady": inp_pady,
                "width": inp_width,
                "font": self.FONTS["form"]["entry"],
            },
            "btn_save": {
                "row": 3,
                "col": 4,
                "sticky": "",
                "padx": 0,
                "pady": (25, 0),
                "width": 8,
            },
        }

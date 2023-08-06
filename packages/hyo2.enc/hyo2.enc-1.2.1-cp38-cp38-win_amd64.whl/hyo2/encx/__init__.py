"""
Hydro-Package
ENC X
"""

import os
import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from hyo2.abc.app.app_info import AppInfo

name = "ENCX"
__version__ = "1.2.1"
__author__ = "gmasetti@ccom.unh.edu"
__license__ = "LGPLv3 license"
__copyright__ = "Copyright 2021 University of New Hampshire, Center for Coastal and Ocean Mapping"


app_info = AppInfo()

app_info.app_name = name
app_info.app_version = __version__
app_info.app_author = "Giuseppe Masetti(UNH,CCOM)"
app_info.app_author_email = "gmasetti@ccom.unh.edu"

app_info.app_license = "LGPL v3"
app_info.app_license_url = "https://www.hydroffice.org/license/"

app_info.app_path = os.path.abspath(os.path.dirname(__file__))

app_info.app_url = "https://www.hydroffice.org/catools/"
app_info.app_manual_url = "https://www.hydroffice.org/manuals/catools/index.html"
app_info.app_support_email = "encx@hydroffice.org"
app_info.app_latest_url = "https://www.hydroffice.org/latest/catools.txt"

app_info.app_media_path = os.path.join(app_info.app_path, "media")
app_info.app_main_window_object_name = "MainWindow"
app_info.app_license_path = os.path.join(app_info.app_media_path, "LICENSE")
app_info.app_icon_path = os.path.join(app_info.app_media_path, "app_icon.png")

# icon size
app_info.app_tabs_icon_size = 36
app_info.app_toolbars_icon_size = 24

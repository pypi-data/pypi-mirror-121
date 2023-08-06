"""
Hyo2-Package
S57
"""

import os

import logging
logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

from hyo2.abc.lib.lib_info import LibInfo

name = "S57"
__version__ = "1.2.0"
__author__ = "gmasetti@ccom.unh.edu"
__license__ = "LGPLv3 license"
__copyright__ = "Copyright 2021 University of New Hampshire, Center for Coastal and Ocean Mapping"

lib_info = LibInfo()

lib_info.lib_name = name
lib_info.lib_version = __version__
lib_info.lib_author = "Giuseppe Masetti(UNH,CCOM)"
lib_info.lib_author_email = "gmasetti@ccom.unh.edu"

lib_info.lib_license = "LGPL v3"
lib_info.lib_license_url = "https://www.hydroffice.org/license/"

lib_info.lib_path = os.path.abspath(os.path.dirname(__file__))

lib_info.lib_url = "https://www.hydroffice.org/catools/"
lib_info.lib_manual_url = "https://www.hydroffice.org/manuals/catools/index.html"
lib_info.lib_support_email = "enc@hydroffice.org"
lib_info.lib_latest_url = "https://www.hydroffice.org/latest/catools.txt"

lib_info.lib_dep_dict = {
    "PySide2": "PySide2"
}

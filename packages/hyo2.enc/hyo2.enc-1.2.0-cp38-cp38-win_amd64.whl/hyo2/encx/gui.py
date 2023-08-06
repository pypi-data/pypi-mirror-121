import os
import sys
import traceback
from PySide2 import QtCore, QtWidgets

import logging

logger = logging.getLogger(__name__)

from hyo2.encx import __version__ as app_version
from hyo2.encx import name as app_name
from hyo2.abc.app.app_style import AppStyle
from hyo2.encx.mainwin import MainWin
from hyo2.encx.encx import ENCX


def qt_custom_handler(error_type: QtCore.QtMsgType, error_context: QtCore.QMessageLogContext, message: str):
    logger.info("Qt error: %s [%s] -> %s"
                % (error_type, error_context, message))

    for line in traceback.format_stack():
        logger.debug("- %s" % line.strip())


QtCore.qInstallMessageHandler(qt_custom_handler)


def gui():
    """Run the CA Tools gui"""

    here = os.path.abspath(os.path.dirname(__file__))  # to be overloaded
    media = os.path.join(here, "media")

    # app
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(AppStyle.load_stylesheet())
    app.setApplicationName('%s %s' % (app_name, app_version))
    app.setOrganizationName("HydrOffice")
    app.setOrganizationDomain("hyo.org")

    # main window
    main_win = MainWin()
    # enc x widget
    encx = ENCX(main_win=main_win)
    main_win.setCentralWidget(encx)
    sys.excepthook = main_win.exception_hook  # install the exception hook
    main_win.show()

    sys.exit(app.exec_())

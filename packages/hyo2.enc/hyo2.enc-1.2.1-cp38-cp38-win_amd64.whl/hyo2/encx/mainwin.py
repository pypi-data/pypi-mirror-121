import os
import sys
import traceback

from PySide2 import QtCore, QtGui, QtWidgets

import logging
logger = logging.getLogger(__name__)

from hyo2.s57 import lib_info
from hyo2.encx import app_info
from hyo2.encx import __version__ as app_version
from hyo2.encx import name as app_name

from hyo2.abc.app.dialogs.exception.exception_dialog import ExceptionDialog


class MainWin(QtWidgets.QMainWindow):

    here = os.path.abspath(os.path.dirname(__file__))
    media = os.path.join(here, "media")

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)

        self.setWindowTitle('HydrOffice %s %s' % (app_name, app_version))
        self.setMinimumSize(400, 250)
        self.resize(800, 600)
        # set icons
        icon_info = QtCore.QFileInfo(os.path.join(self.media, 'favicon.png'))
        self.setWindowIcon(QtGui.QIcon(icon_info.absoluteFilePath()))
        if (sys.platform == 'win32') or (os.name is "nt"):  # is_windows()
            try:
                # This is needed to display the app icon on the taskbar on Windows 7
                import ctypes
                app_id = '%s v.%s' % (app_name, app_version)
                ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
            except AttributeError as e:
                logger.debug("Unable to change app icon: %s" % e)

    def exception_hook(self, ex_type: type, ex_value: BaseException, tb: traceback) -> None:
        sys.__excepthook__(ex_type, ex_value, tb)

        # first manage case of not being an exception (e.g., keyboard interrupts)
        if not issubclass(ex_type, Exception):
            msg = str(ex_value)
            if not msg:
                msg = ex_value.__class__.__name__
            logger.info(msg)
            self.close()
            return

        dlg = ExceptionDialog(app_info=app_info, lib_info=lib_info, ex_type=ex_type, ex_value=ex_value, tb=tb)
        ret = dlg.exec_()
        if ret == QtWidgets.QDialog.Rejected:
            if not dlg.user_triggered:
                self.close()
        else:
            logger.warning("ignored exception")

    # Quitting #

    def do_you_really_want(self, title="Quit", text="quit"):
        msg_box = QtWidgets.QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setIconPixmap(QtGui.QPixmap(os.path.join(self.media, 'favicon.png')).scaled(QtCore.QSize(60, 60)))
        msg_box.setText('Do you really want to %s?' % text)
        msg_box.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        msg_box.setDefaultButton(QtWidgets.QMessageBox.No)
        return msg_box.exec_()

    def closeEvent(self, event):
        """ actions to be done before close the app """
        reply = self.do_you_really_want("Quit", "quit %s" % app_info.app_name)

        if reply == QtWidgets.QMessageBox.Yes:

            event.accept()
            super().closeEvent(event)

        else:

            event.ignore()

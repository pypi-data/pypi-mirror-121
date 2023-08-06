from PySide2 import QtGui, QtCore, QtWidgets

import logging
logger = logging.getLogger(__name__)

from hyo2.encx.iso_tree import IsoTree
from hyo2.iso8211.iso8211 import Iso8211


class IsoTab(QtWidgets.QMainWindow):

    def __init__(self, par_win=None):
        QtWidgets.QMainWindow.__init__(self)
        self.par_win = par_win
        self.ddf = None
        self.iso = None

        frame = QtWidgets.QFrame()
        self.setCentralWidget(frame)

        # -- add an horizontal layout
        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        frame.setLayout(hbox)

        # -- add a splitter
        self.h_splitter = QtWidgets.QSplitter(self)
        self.h_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.h_splitter.setContentsMargins(0, 0, 0, 0)
        hbox.addWidget(self.h_splitter)

        # --- add a tree
        self.tree = IsoTree(par_win=self)
        self.h_splitter.addWidget(self.tree)

        # --- add a text viewer
        self.viewer = QtWidgets.QTextEdit()
        # create a monospace font
        font = QtGui.QFont()
        font.setFamily("Courier")
        font.setStyleHint(QtGui.QFont.Monospace)
        font.setFixedPitch(True)
        font.setPointSize(9)
        metrics = QtGui.QFontMetrics(font)
        self.viewer.setFont(font)
        self.viewer.setLineWrapMode(QtWidgets.QTextEdit.NoWrap)
        # set the tab size
        self.viewer.setTabStopWidth(2 * metrics.width(' '))
        self.h_splitter.addWidget(self.viewer)
        self.viewer.setReadOnly(True)

        # set stretch
        self.h_splitter.setStretchFactor(0, 2)
        self.h_splitter.setStretchFactor(1, 4)

    def load_iso(self, iso_path):
        # reset
        self.clear_data()
        self.iso = Iso8211()
        self.iso.set_input_filename(iso_path)

        # read and parse the content
        try:
            self.iso.read()
            logger.debug('byte-content read: %sB' % self.iso.blob_size())
            logger.debug('successfully parsed')
        except RuntimeError as e:
            msg = 'Error reading the byte content of %s: %s' % (iso_path, e)
            # noinspection PyCallByClass
            QtWidgets.QMessageBox.critical(self, "Reading Error", msg, QtWidgets.QMessageBox.Ok)
            return False

        # pass the ddf to the tree after having set the viewer
        self.tree.set_viewer(self.viewer)
        success = self.tree.show_iso8211(iso8211=self.iso)
        if not success:
            msg = 'Error loading tree for %s' % iso_path
            # noinspection PyCallByClass
            QtWidgets.QMessageBox.critical(self, "Loading Tree Error", msg, QtWidgets.QMessageBox.Ok)
            return False

        return True

    def clear_data(self):
        logger.debug('clear data')
        if self.ddf:
            self.ddf.close()
        self.tree.clear_data()
        self.viewer.clear()

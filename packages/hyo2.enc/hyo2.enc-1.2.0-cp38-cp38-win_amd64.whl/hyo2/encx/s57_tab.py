from PySide2 import QtWidgets, QtGui, QtCore

import logging
logger = logging.getLogger(__name__)

from hyo2.encx.s57_tree import S57Tree
from hyo2.s57.s57 import S57


class S57Tab(QtWidgets.QMainWindow):

    def __init__(self, par_win=None):
        QtWidgets.QMainWindow.__init__(self)
        self.par_win = par_win
        self.s57 = None

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
        self.tree = S57Tree(par_win=self)
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

    def load_s57(self, s57_path):
        # reset
        self.clear_data()
        self.s57 = S57()
        self.s57.set_input_filename(s57_path)

        # read and parse the content
        try:
            self.s57.read()
            logger.debug('byte-content read: %sB' % self.s57.input_blob_size())
            logger.debug('successfully parsed')
        except RuntimeError as e:
            msg = 'Error reading the byte content of %s: %s' % (s57_path, e)
            QtWidgets.QMessageBox.critical(self, "Reading Error", msg, QtWidgets.QMessageBox.Ok)
            return False

        # pass the ddf to the tree after having set the viewer
        self.tree.set_viewer(self.viewer)
        success = self.tree.show_s57(s57=self.s57)
        if not success:
            msg = 'Error loading tree for %s' % s57_path
            QtWidgets.QMessageBox.critical(self, "Loading Tree Error", msg, QtWidgets.QMessageBox.Ok)
            return False

        return True

    def clear_data(self):
        logger.debug('clear data')
        self.s57 = None
        self.tree.clear_data()
        self.viewer.clear()

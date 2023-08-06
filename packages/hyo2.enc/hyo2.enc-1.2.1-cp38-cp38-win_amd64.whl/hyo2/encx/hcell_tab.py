from PySide2 import QtGui, QtWidgets, QtCore

import logging
logger = logging.getLogger(__name__)


class HCellTab(QtWidgets.QMainWindow):

    def __init__(self, par_win=None):
        QtWidgets.QMainWindow.__init__(self)
        self.par_win = par_win
        self.ddf = None

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

        # # --- add a tree
        # self.tree = IsoTree(par_win=self)
        # self.h_splitter.addWidget(self.tree)
        #
        # # --- add a text viewer
        # self.viewer = QtGui.QTextEdit()
        # # create a monospace font
        # font = QtGui.QFont()
        # font.setFamily("Courier")
        # font.setStyleHint(QtGui.QFont.Monospace)
        # font.setFixedPitch(True)
        # font.setPointSize(9)
        # metrics = QtGui.QFontMetrics(font)
        # self.viewer.setFont(font)
        # self.viewer.setLineWrapMode(QtGui.QTextEdit.NoWrap)
        # # set the tab size
        # self.viewer.setTabStopWidth(2 * metrics.width(' '))
        # self.h_splitter.addWidget(self.viewer)
        # self.viewer.setReadOnly(True)
        #
        # # set stretch
        # self.h_splitter.setStretchFactor(0, 2)
        # self.h_splitter.setStretchFactor(1, 4)

    def load_hcell(self, hcell_path):
        # reset
        self.clear_data()
        # self.ddf = DDF()
        #
        # # read the byte content
        # success = self.ddf.read(file_path=iso_path)
        # if success:
        #     logger.debug('byte-content read: %sB' % self.ddf.size)
        # else:
        #     msg = 'Error reading the byte content of %s' % iso_path
        #     QtGui.QMessageBox.critical(self, "Reading Error", msg, QtGui.QMessageBox.Ok)
        #     return False
        #
        # # create file indices to check file validity
        # success = self.ddf.make_indices()
        # if not success:
        #     msg = 'Error indexing the byte content of %s' % iso_path
        #     QtGui.QMessageBox.critical(self, "Indexing Error", msg, QtGui.QMessageBox.Ok)
        #     return False
        #
        # # parse the DDR and the DRs
        # success = self.ddf.parse()
        # if success:
        #     logger.debug('DDR parsed')
        # else:
        #     msg = 'Error parsing the byte content of %s' % iso_path
        #     QtGui.QMessageBox.critical(self, "Parsing Error", msg, QtGui.QMessageBox.Ok)
        #     return False
        #
        # # pass the ddf to the tree after having set the viewer
        # self.tree.set_viewer(self.viewer)
        # success = self.tree.show_ddf(ddf=self.ddf)
        # if not success:
        #     msg = 'Error loading tree for %s' % iso_path
        #     QtGui.QMessageBox.critical(self, "Loading Tree Error", msg, QtGui.QMessageBox.Ok)
        #     return False

        return True

    def clear_data(self):
        logger.debug('clear data')
        # if self.ddf:
        #     self.ddf.close()
        # self.tree.clear_data()
        # self.viewer.clear()

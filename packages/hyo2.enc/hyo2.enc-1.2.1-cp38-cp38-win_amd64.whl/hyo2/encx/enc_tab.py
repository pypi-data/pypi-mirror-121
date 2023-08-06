from PySide2 import QtWidgets, QtGui, QtCore

import logging
logger = logging.getLogger(__name__)

from .enc_tree import ENCTree
# from hyo.enc.enc import ENC


class EncTab(QtWidgets.QMainWindow):

    def __init__(self, par_win=None):
        QtWidgets.QMainWindow.__init__(self)
        self.par_win = par_win
        self.enc = None

        frame = QtWidgets.QFrame()
        self.setCentralWidget(frame)

        # -- add an horizontal layout
        self.hbox = QtWidgets.QHBoxLayout()
        self.hbox.setSpacing(0)
        self.hbox.setContentsMargins(0, 0, 0, 0)
        frame.setLayout(self.hbox)

        # -- add a splitter
        self.h_splitter = QtWidgets.QSplitter(self)
        self.h_splitter.setOrientation(QtCore.Qt.Horizontal)
        self.h_splitter.setContentsMargins(0, 0, 0, 0)
        self.hbox.addWidget(self.h_splitter)

        # --- add a tree
        self.tree = ENCTree(par_win=self)
        self.h_splitter.addWidget(self.tree)

        # -- add a right_frame
        r_frame = QtWidgets.QFrame()
        self.h_splitter.addWidget(r_frame)
        # --- add a vertical layout
        vbox = QtWidgets.QVBoxLayout()
        vbox.setSpacing(0)
        vbox.setContentsMargins(0, 0, 0, 0)
        r_frame.setLayout(vbox)

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
        vbox.addWidget(self.viewer)
        self.viewer.setReadOnly(True)

        # add an horizontal layout for buttons
        btn_hbox = QtWidgets.QHBoxLayout()
        btn_hbox.setSpacing(0)
        btn_hbox.setContentsMargins(0, 0, 0, 0)
        vbox.addLayout(btn_hbox)
        # - stretch
        btn_hbox.addStretch()
        # - add a run checks button
        run_checks = QtWidgets.QPushButton('Run checks')
        btn_hbox.addWidget(run_checks)
        run_checks.setFixedSize(QtCore.QSize(80, 30))
        run_checks.setToolTip('Run checks based on IHO S57 PS')
        # noinspection PyUnresolvedReferences
        run_checks.clicked.connect(self.click_run_checks)
        # - stretch
        btn_hbox.addStretch()

        # set stretch
        self.h_splitter.setStretchFactor(0, 2)
        self.h_splitter.setStretchFactor(1, 4)

    def load_enc(self, enc_path):
        # reset
        self.clear_data()
        # try:
        #     self.enc = ENC(file_path=enc_path)
        # except RuntimeError as e:
        #     msg = 'Error reading the file: %s' % e
        #     QtGui.QMessageBox.critical(self, "Reading Error", msg, QtGui.QMessageBox.Ok)
        #     return False
        #
        # # pass the ddf to the tree after having set the viewer
        # self.tree.set_viewer(self.viewer)
        # success = self.tree.show_enc(enc=self.enc)
        # if not success:
        #     msg = 'Error loading tree for %s' % enc_path
        #     QtGui.QMessageBox.critical(self, "Loading Tree Error", msg, QtGui.QMessageBox.Ok)
        #     return False

        return True

    def clear_data(self):
        logger.debug('clear data')
        if self.enc:
            self.enc.close()
            self.enc = None
        self.tree.clear_data()
        self.viewer.clear()

    def click_run_checks(self):
        logger.debug('run checks')
        self.viewer.clear()
        if self.enc:
            self.viewer.append(self.enc.checks())


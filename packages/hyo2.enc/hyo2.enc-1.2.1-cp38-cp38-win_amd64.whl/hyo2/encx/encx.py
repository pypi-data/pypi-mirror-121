import os

from PySide2 import QtGui, QtCore, QtWidgets

import logging
logger = logging.getLogger(__name__)

from hyo2.abc.app.qt_progress import QtProgress

from hyo2.encx.iso_tab import IsoTab
from hyo2.encx.s57_tab import S57Tab
from hyo2.encx.s57features_tab import S57FeaturesTab
from hyo2.encx.enc_tab import EncTab
from hyo2.encx.hcell_tab import HCellTab


class ENCX(QtWidgets.QMainWindow):

    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))  # to be overloaded
    media = os.path.join(here, "media")

    def __init__(self, main_win):
        QtWidgets.QMainWindow.__init__(self)
        self.main_win = main_win

        # set palette and layout
        self.setContentsMargins(0, 0, 0, 0)
        self.setMinimumSize(QtCore.QSize(800, 600))

        # add a progress dialog
        self.progress = QtProgress(parent=self)

        # init default settings
        settings = QtCore.QSettings()
        export_folder = settings.value("export_folder")
        if (export_folder is None) or (not os.path.exists(export_folder)):
            settings.setValue("export_folder", self.here)
        import_folder = settings.value("import_folder")
        if (import_folder is None) or (not os.path.exists(import_folder)):
            settings.setValue("import_folder", self.here)

        # add a frame and a vertical layout
        self.frame = QtWidgets.QFrame()
        self.setCentralWidget(self.frame)
        # add a vertical layout
        self.vbox = QtWidgets.QVBoxLayout()
        self.vbox.setSpacing(0)
        self.vbox.setContentsMargins(0, 0, 0, 0)
        self.frame.setLayout(self.vbox)

        # add tabs
        self.tabs = None
        self.tab_iso = None
        self.tab_s57 = None
        self.tab_s57features = None
        self.tab_hcell = None
        self.tab_enc = None
        self._make_tabs()

        # add bottom buttons
        self._make_buttons()

    def _make_tabs(self):
        # make tabs
        self.tabs = QtWidgets.QTabWidget()
        self.vbox.addWidget(self.tabs)
        self.tabs.setTabPosition(QtWidgets.QTabWidget.South)
        self.tabs.setIconSize(QtCore.QSize(20, 20))

        # ISO tab
        self.tab_iso = IsoTab(par_win=self)
        idx = self.tabs.insertTab(0, self.tab_iso,
                                  QtGui.QIcon(os.path.join(self.media, 'iso.png')), "")
        self.tabs.setTabToolTip(idx, "ISO 8211 view")

        # S57 tab
        self.tab_s57 = S57Tab(par_win=self)
        idx = self.tabs.insertTab(1, self.tab_s57,
                                  QtGui.QIcon(os.path.join(self.media, 's57.png')), "")
        self.tabs.setTabToolTip(idx, "S57 view")

        # S57features tab
        self.tab_s57features = S57FeaturesTab(par_win=self)
        idx = self.tabs.insertTab(2, self.tab_s57features,
                                  QtGui.QIcon(os.path.join(self.media, 'objs.png')), "")
        self.tabs.setTabToolTip(idx, "S57 objects view")

        # HCell tab
        self.tab_hcell = HCellTab(par_win=self)
        idx = self.tabs.insertTab(3, self.tab_hcell,
                                  QtGui.QIcon(os.path.join(self.media, 'hcell.png')), "")
        self.tabs.setTabToolTip(idx, "HCell view")
        self.tabs.setTabEnabled(idx, False)

        # ENC tab
        self.tab_enc = EncTab(par_win=self)
        idx = self.tabs.insertTab(4, self.tab_enc,
                                  QtGui.QIcon(os.path.join(self.media, 'enc.png')), "")
        self.tabs.setTabToolTip(idx, "ENC view")
        self.tabs.setTabEnabled(idx, False)

    def _make_buttons(self):
        # add a frame to the bottom
        frame = QtWidgets.QFrame()
        self.vbox.addWidget(frame)

        # add an horizontal layout
        hbox = QtWidgets.QHBoxLayout()
        hbox.setSpacing(0)
        hbox.setContentsMargins(0, 0, 0, 0)
        frame.setLayout(hbox)

        # - stretch
        hbox.addStretch()

        # - add a load ISO button
        load_iso = QtWidgets.QPushButton('ISO 8211')
        hbox.addWidget(load_iso)
        load_iso.setFixedSize(QtCore.QSize(80, 30))
        load_iso.setToolTip('Load a file as ISO 8211')
        # noinspection PyUnresolvedReferences
        load_iso.clicked.connect(self.click_load_iso)

        # - add a load s57 button
        load_s57 = QtWidgets.QPushButton('IHO S57')
        hbox.addWidget(load_s57)
        load_s57.setFixedSize(QtCore.QSize(80, 30))
        load_s57.setToolTip('Load a file as S57')
        # noinspection PyUnresolvedReferences
        load_s57.clicked.connect(self.click_load_s57)

        # - add a load s57 features button
        load_s57_features = QtWidgets.QPushButton('S57 Objects')
        hbox.addWidget(load_s57_features)
        load_s57_features.setFixedSize(QtCore.QSize(80, 30))
        load_s57_features.setToolTip('Load a file as IHO S57 Objects')
        # noinspection PyUnresolvedReferences
        load_s57_features.clicked.connect(self.click_load_s57_features)

        # - add a load HCell button
        load_hcell = QtWidgets.QPushButton('NOAA HCell')
        hbox.addWidget(load_hcell)
        load_hcell.setFixedSize(QtCore.QSize(80, 30))
        load_hcell.setToolTip('Load a file as NOAA HCell')
        # noinspection PyUnresolvedReferences
        load_hcell.clicked.connect(self.click_load_hcell)
        load_hcell.setDisabled(True)

        # - add a load ENC button
        load_enc = QtWidgets.QPushButton('IHO ENC')
        hbox.addWidget(load_enc)
        load_enc.setFixedSize(QtCore.QSize(80, 30))
        load_enc.setToolTip('Load a file as ENC')
        # noinspection PyUnresolvedReferences
        load_enc.clicked.connect(self.click_load_enc)
        load_enc.setDisabled(True)

        # - add a clear button
        clear_all = QtWidgets.QPushButton('Clear')
        hbox.addWidget(clear_all)
        clear_all.setFixedSize(QtCore.QSize(80, 30))
        clear_all.setToolTip('Clear all the loaded data')
        # noinspection PyUnresolvedReferences
        clear_all.clicked.connect(self.click_clear_all)

        # - stretch
        hbox.addStretch()

        self.vbox.addSpacing(6)

    def click_load_iso(self):
        """ Load the file as ISO"""
        logger.debug('user wants to load as ISO8211 file')

        # ask the file path to the user
        settings = QtCore.QSettings()
        # noinspection PyCallByClass
        selection, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load file as ISO 8211",
                                                             settings.value("import_folder"),
                                                             "S57 file (*.000);;All files (*.*)")
        if not selection:
            return
        logger.debug('user selection: %s' % selection)
        settings.setValue("import_folder", os.path.dirname(selection))
        self.progress.start()
        self.progress.update(30)

        # attempt to read the data
        success = self.tab_iso.load_iso(iso_path=selection)
        if not success:
            self.progress.end()
            return
        self.progress.update(50)
        logger.debug('iso successfully read')

        self.tabs.setCurrentWidget(self.tab_iso)

        self.progress.end()

    def click_load_s57(self):
        """ Load the S57 file"""
        logger.debug('user wants to load an S57 file')

        # ask the file path to the user
        settings = QtCore.QSettings()
        # noinspection PyCallByClass
        selection, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load file as IHO S57",
                                                             settings.value("import_folder"),
                                                             "IHO S57 file (*.000);;All files (*.*)")
        if not selection:
            return
        logger.debug('user selection: %s' % selection)
        settings.setValue("import_folder", os.path.dirname(selection))
        self.progress.start()
        self.progress.update(30)

        # attempt to read the data
        success = self.tab_s57.load_s57(s57_path=selection)
        if not success:
            self.progress.end()
            return
        self.progress.update(50)
        logger.debug('s57 successfully read')

        self.tabs.setCurrentWidget(self.tab_s57)

        self.progress.end()

    def click_load_s57_features(self):
        """ Load the S57 file"""
        logger.debug('user wants to load S57 features')

        # ask the file path to the user
        settings = QtCore.QSettings()
        # noinspection PyCallByClass
        selection, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load file as IHO S57 features",
                                                             settings.value("import_folder"),
                                                             "IHO S57 file (*.000);;All files (*.*)")
        if not selection:
            return
        logger.debug('user selection: %s' % selection)
        settings.setValue("import_folder", os.path.dirname(selection))
        self.progress.start()
        self.progress.update(30)

        # attempt to read the data
        success = self.tab_s57features.load_s57(s57_path=selection)
        if not success:
            self.progress.end()
            return
        self.progress.update(50)
        logger.debug('s57 successfully read')

        self.tabs.setCurrentWidget(self.tab_s57features)

        self.progress.end()

    def click_load_enc(self):
        """ Load the ENC file"""
        logger.debug('user wants to load an ENC file')

        # ask the file path to the user
        settings = QtCore.QSettings()
        # noinspection PyCallByClass
        selection, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load file as IHO ENC",
                                                             settings.value("import_folder"),
                                                             "IHO ENC file (*.000);;All files (*.*)")
        if not selection:
            return
        logger.debug('user selection: %s' % selection)
        settings.setValue("import_folder", os.path.dirname(selection))
        self.progress.start()
        self.progress.update(30)

        # attempt to read the data
        success = self.tab_enc.load_enc(enc_path=selection)
        if not success:
            self.progress.end()
            return
        self.progress.update(50)
        logger.debug('iso successfully read')

        self.tabs.setCurrentWidget(self.tab_enc)

        self.progress.end()

    def click_load_hcell(self):
        """ Load the HCell file"""
        logger.debug('user wants to load a NOAA HCell file')

        # ask the file path to the user
        settings = QtCore.QSettings()
        # noinspection PyCallByClass
        selection, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Load file as NOAA HCell",
                                                             settings.value("import_folder"),
                                                             "NOAA HCell file (*.000);;All files (*.*)")
        if not selection:
            return
        logger.debug('user selection: %s' % selection)
        settings.setValue("import_folder", os.path.dirname(selection))
        self.progress.start()
        self.progress.update(30)

        # attempt to read the data
        success = self.tab_hcell.load_hcell(hcell_path=selection)
        if not success:
            self.progress.end()
            return
        self.progress.update(50)
        logger.debug('hcell successfully read')

        self.tabs.setCurrentWidget(self.tab_hcell)

        self.progress.end()

    def click_clear_all(self):
        """Clear all the data"""
        logger.debug('user wants to clear all the data')
        self.tab_iso.clear_data()
        self.tab_s57.clear_data()
        self.tab_s57features.clear_data()
        self.tab_enc.clear_data()
        self.tab_hcell.clear_data()

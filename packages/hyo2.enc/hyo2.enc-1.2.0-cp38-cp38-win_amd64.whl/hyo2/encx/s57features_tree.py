import os

from PySide2 import QtWidgets, QtGui, QtCore

import logging
logger = logging.getLogger(__name__)

from hyo2.s57.s57 import S57
from hyo2.abc.app.qt_progress import QtProgress


class S57FeaturesTree(QtWidgets.QTreeWidget):

    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))  # to be overloaded
    media = os.path.join(here, "media")

    s57_dict = {
        'S57_FILE': 'S57 Objects',
    }

    def __init__(self, par_win=None):
        QtWidgets.QTreeWidget.__init__(self)
        self.par_win = par_win
        self.s57 = None
        self.s57file = None
        self.rec10s = None

        # items
        self.root = None
        # records-specific
        self.rec10s_i = None

        self._viewer = None

        self.setIconSize(QtCore.QSize(36, 36))

        labels = ['Node', 'Info']
        self.setColumnCount(len(labels))
        self.setHeaderLabels(labels)
        self.header().close()

        self.setIndentation(8)
        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.setFocus()
        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.currentModelItem = None
        # noinspection PyUnresolvedReferences
        self.customContextMenuRequested.connect(self.make_context_menu)

        # noinspection PyUnresolvedReferences
        self.itemSelectionChanged.connect(self.new_selection)

        # add a progress dialog
        self.progress = QtProgress(parent=self)

    def set_viewer(self, viewer):
        self._viewer = viewer

    def show_s57(self, s57):
        self.clear_data()

        if not isinstance(s57, S57):
            logger.error('passed invalid S57')
            return False
        self.s57 = s57

        self.s57file = self.s57.input_s57file
        if not self.s57file.is_valid:
            logger.error('passed invalid S57File')
            return False

        # 100 rec
        self.rec10s = self.s57file.rec10s
        if len(self.rec10s) == 0:
            logger.error('passed empty REC10s')

        # create root tree item
        self.root = QtWidgets.QTreeWidgetItem(None)
        self.root.setText(1, self.s57_dict['S57_FILE'])
        self.root.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'file.png')))
        self.addTopLevelItem(self.root)
        if self.root:
            self.setCurrentItem(self.root)

        # add objects
        success = self._show_objects()
        if not success:
            return False

        return True

    def _show_objects(self):
        if not self.root:
            logger.error('passed empty root item')
            return False

        for rec in self.rec10s:
            rec_i = QtWidgets.QTreeWidgetItem()
            rec_i.setText(1, '%s' % rec.acronym)
            rec_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'obj.png')))
            self.root.addChild(rec_i)

        return True

    def new_selection(self):
        self.progress.start()

        try:
            sel_item = self.selectedItems()[0]
        except IndexError as e:
            logger.info('invalid selection: %s' % e)
            return
        try:
            par_item = sel_item.parent()
        except Exception:
            par_item = None
        try:
            grand_par_item = par_item.parent()
        except Exception:
            grand_par_item = None

        logger.debug('item changed: %s [lng: %s, %s]'
                     % (sel_item.text(1), (par_item.text(1) if par_item else "None"),
                        (grand_par_item.text(1) if grand_par_item else "None")))
        self._viewer.clear()

        item_name = sel_item.text(1)
        if par_item:
            par_name = par_item.text(1)
        else:
            par_name = None
        if grand_par_item:
            grand_par_name = grand_par_item.text(1)
        else:
            grand_par_name = None

        if item_name == self.s57_dict['S57_FILE']:
            self._viewer.append("Objects: %s" % (len(self.rec10s) if (self.rec10s is not None) else "None"))
        else:
            if par_name == self.s57_dict['S57_FILE']:
                rec_nr = par_item.indexOfChild(sel_item)
                self._viewer.append("%s" % self.rec10s[rec_nr].feature_info())

        self.progress.end()

    def make_context_menu(self):
        logger.debug('context menu')

    def clear_data(self):
        logger.debug('clear data')
        self.s57 = None
        self.rec10s = None

        self.root = None
        self.rec10s_i = None

        self.clear()

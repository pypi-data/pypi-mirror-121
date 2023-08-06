import os

from PySide2 import QtWidgets, QtGui, QtCore

import logging
logger = logging.getLogger(__name__)

from hyo2.s57.s57 import S57
from hyo2.abc.app.qt_progress import QtProgress


class S57Tree(QtWidgets.QTreeWidget):

    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))  # to be overloaded
    media = os.path.join(here, "media")

    s57_dict = {
        'S57_FILE': 'S57 File',
        'S57_REC01S': 'General Information',
        'S57_REC02S': 'Geographic Reference',
        'S57_REC10S': 'Features',
        'S57_REC11S': 'Isolated Nodes',
        'S57_REC12S': 'Connected Nodes',
        'S57_REC13S': 'Edges',
    }

    def __init__(self, par_win=None):
        QtWidgets.QTreeWidget.__init__(self)
        self.par_win = par_win
        self.s57 = None
        self.s57file = None
        self.rec01s = None
        self.rec02s = None
        self.rec10s = None
        self.rec11s = None
        self.rec12s = None
        self.rec13s = None
        self.rec14s = None

        # items
        self.root = None
        # records-specific
        self.rec01s_i = None
        self.rec02s_i = None
        self.rec03s_i = None
        self.rec04s_i = None
        self.rec05s_i = None
        self.rec06s_i = None
        self.rec07s_i = None
        self.rec08s_i = None
        self.rec09s_i = None
        self.rec10s_i = None
        self.rec11s_i = None
        self.rec12s_i = None
        self.rec13s_i = None
        self.rec14s_i = None

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

        # create root tree item
        self.root = QtWidgets.QTreeWidgetItem(None)
        self.root.setText(1, self.s57_dict['S57_FILE'])
        self.root.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'file.png')))
        self.addTopLevelItem(self.root)
        if self.root:
            self.setCurrentItem(self.root)

        # add records
        success = self._show_records()
        if not success:
            return False

        return True

    def _show_records(self):
        if not self.root:
            logger.error('passed empty root item')
            return False

        # 10 rec
        self.rec01s = self.s57file.rec01s
        if len(self.rec01s) == 0:
            logger.error('passed empty REC01s')
        else:
            self.rec01s_i = QtWidgets.QTreeWidgetItem()
            self.rec01s_i.setText(1, self.s57_dict['S57_REC01S'])
            self.rec01s_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'rec.png')))
            self.root.addChild(self.rec01s_i)

        # 20 rec
        self.rec02s = self.s57file.rec02s
        if len(self.rec02s) == 0:
            logger.error('passed empty REC02s')
        else:
            self.rec02s_i = QtWidgets.QTreeWidgetItem()
            self.rec02s_i.setText(1, self.s57_dict['S57_REC02S'])
            self.rec02s_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'rec.png')))
            self.root.addChild(self.rec02s_i)

        # 100 rec
        self.rec10s = self.s57file.rec10s
        if len(self.rec10s) == 0:
            logger.error('passed empty REC10s')
        else:
            self.rec10s_i = QtWidgets.QTreeWidgetItem()
            self.rec10s_i.setText(1, self.s57_dict['S57_REC10S'])
            self.rec10s_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'recs.png')))
            self.root.addChild(self.rec10s_i)

            for i, rec in enumerate(self.rec10s):
                rec_i = QtWidgets.QTreeWidgetItem()
                rec_i.setText(1, '#%05d' % i)
                rec_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'rec.png')))
                self.rec10s_i.addChild(rec_i)

        # 110 rec
        self.rec11s = self.s57file.rec11s
        if len(self.rec11s) == 0:
            logger.error('passed empty REC11s')
        else:
            self.rec11s_i = QtWidgets.QTreeWidgetItem()
            self.rec11s_i.setText(1, self.s57_dict['S57_REC11S'])
            self.rec11s_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'recs.png')))
            self.root.addChild(self.rec11s_i)

            for i, rec in enumerate(self.rec11s):
                rec_i = QtWidgets.QTreeWidgetItem()
                rec_i.setText(1, '#%05d' % i)
                rec_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'rec.png')))
                self.rec11s_i.addChild(rec_i)

        # 120 rec
        self.rec12s = self.s57file.rec12s
        if len(self.rec12s) == 0:
            logger.error('passed empty REC12s')
        else:
            self.rec12s_i = QtWidgets.QTreeWidgetItem()
            self.rec12s_i.setText(1, self.s57_dict['S57_REC12S'])
            self.rec12s_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'recs.png')))
            self.root.addChild(self.rec12s_i)

            for i, rec in enumerate(self.rec12s):
                rec_i = QtWidgets.QTreeWidgetItem()
                rec_i.setText(1, '#%05d' % i)
                rec_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'rec.png')))
                self.rec12s_i.addChild(rec_i)

        # 130 rec
        self.rec13s = self.s57file.rec13s
        if len(self.rec13s) == 0:
            logger.error('passed empty REC13s')
        else:
            self.rec13s_i = QtWidgets.QTreeWidgetItem()
            self.rec13s_i.setText(1, self.s57_dict['S57_REC13S'])
            self.rec13s_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'recs.png')))
            self.root.addChild(self.rec13s_i)

            for i, rec in enumerate(self.rec13s):
                rec_i = QtWidgets.QTreeWidgetItem()
                rec_i.setText(1, '#%05d' % i)
                rec_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'rec.png')))
                self.rec13s_i.addChild(rec_i)

        return True

    def _add_to_viewer(self, info_list):
        """Helper function to display info into the passed viewer"""
        for info in info_list:
            info_tag = ("%s:" % info[0]).ljust(20)
            self._viewer.append("%s %s" % (info_tag, info[1]))

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
        # logger.debug('item name: %s' % item_name)
        if par_item:
            par_name = par_item.text(1)
        else:
            par_name = None
        # logger.debug('par name: %s' % par_name)

        if grand_par_item:
            grand_par_name = grand_par_item.text(1)
        else:
            grand_par_name = None

        if item_name == self.s57_dict['S57_FILE']:
            self._viewer.append("%s" % self.s57file)
        elif item_name == self.s57_dict['S57_REC01S']:
            self._viewer.append("%s" % self.rec01s[0])  # since there should be just 1 rec 10
        elif item_name == self.s57_dict['S57_REC02S']:
            self._viewer.append("%s" % self.rec02s[0])  # since there should be just 1 rec 20
        elif item_name == self.s57_dict['S57_REC10S']:
            self._viewer.append("records: %s" % len(self.rec10s))
        elif item_name == self.s57_dict['S57_REC11S']:
            self._viewer.append("records: %s" % len(self.rec11s))
        elif item_name == self.s57_dict['S57_REC12S']:
            self._viewer.append("records: %s" % len(self.rec12s))
        elif item_name == self.s57_dict['S57_REC13S']:
            self._viewer.append("records: %s" % len(self.rec13s))

        elif item_name[:1] == '#':
            rec_nr = int(item_name[1:])
            logger.debug('rec nr: %s' % rec_nr)

            if par_name == self.s57_dict['S57_REC10S']:
                self._viewer.append("%s" % self.rec10s[rec_nr])
            elif par_name == self.s57_dict['S57_REC11S']:
                self._viewer.append("%s" % self.rec11s[rec_nr])
            elif par_name == self.s57_dict['S57_REC12S']:
                self._viewer.append("%s" % self.rec12s[rec_nr])
            elif par_name == self.s57_dict['S57_REC13S']:
                self._viewer.append("%s" % self.rec13s[rec_nr])

        self.progress.end()

    def make_context_menu(self):
        logger.debug('context menu')

    def clear_data(self):
        logger.debug('clear data')
        self.s57 = None
        self.rec01s = None
        self.rec02s = None
        self.rec10s = None
        self.rec11s = None
        self.rec12s = None
        self.rec13s = None
        self.rec14s = None

        self.root = None
        self.rec01s_i = None
        self.rec02s_i = None
        self.rec03s_i = None
        self.rec04s_i = None
        self.rec05s_i = None
        self.rec06s_i = None
        self.rec07s_i = None
        self.rec08s_i = None
        self.rec09s_i = None
        self.rec10s_i = None
        self.rec11s_i = None
        self.rec12s_i = None
        self.rec13s_i = None
        self.rec14s_i = None

        self.clear()

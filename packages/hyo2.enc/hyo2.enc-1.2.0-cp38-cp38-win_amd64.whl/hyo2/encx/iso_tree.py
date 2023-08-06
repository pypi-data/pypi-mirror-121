import os
from PySide2 import QtWidgets, QtGui, QtCore

import logging
logger = logging.getLogger(__name__)

from hyo2.iso8211.iso8211 import Iso8211
from hyo2.abc.app.qt_progress import QtProgress


class IsoTree(QtWidgets.QTreeWidget):

    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))  # to be overloaded
    media = os.path.join(here, "media")

    iso_dict = {
        'DDF': 'Data Descriptive File',
        'DDR': 'Data Descriptive Record',
        'DDR_LDR': 'DDR Leader',
        'DDR_DIR': 'DDR Directory',
        'DDA': 'Data Descriptive Area',
        'DRs': 'Data Records',
        'DR': 'Data Record',   # unused -> DR index in place
        'DR_LDR': 'DR Leader',
        'DR_DIR': 'DR Directory',
        'UDA': 'User Data Area',
    }

    def __init__(self, par_win=None):
        QtWidgets.QTreeWidget.__init__(self)
        self.par_win = par_win
        self.iso = None
        self.ddf = None
        self.ddr = None
        self.drs = None

        # items
        self.root = None
        # ddr-specific
        self.ddr_i = None
        # drs-specific
        self.drs_i = None
        self.dr_list = None

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

    def show_iso8211(self, iso8211):
        self.clear_data()

        if not isinstance(iso8211, Iso8211):
            logger.error('passed invalid ISO8211')
            return False
        self.iso = iso8211
        self.ddf = iso8211.input_ddf

        # create root tree item
        self.root = QtWidgets.QTreeWidgetItem(None)
        self.root.setText(1, self.iso_dict['DDF'])
        self.root.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'ddf.png')))
        self.addTopLevelItem(self.root)
        if self.root:
            self.setCurrentItem(self.root)

        # add ddr sub-tree
        success = self._show_ddr()
        if not success:
            return False

        # add drs sub-tree
        success = self._show_drs()
        if not success:
            return False

        return True

    def _show_ddr(self):
        if not self.root:
            logger.error('passed empty root item')
            return False
        self.ddr = self.iso.input_ddf.ddr
        if not self.ddr.is_valid:
            logger.error('passed invalid DDR')
            return False

        self.ddr_i = QtWidgets.QTreeWidgetItem()
        self.ddr_i.setText(1, self.iso_dict['DDR'])
        self.ddr_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'ddr.png')))
        self.root.addChild(self.ddr_i)

        ldr = self.ddr.leader
        if not ldr.is_valid:
            logger.error('passed invalid DDR leader')
            return False
        item = QtWidgets.QTreeWidgetItem()
        item.setText(1, self.iso_dict['DDR_LDR'])
        item.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'ldr.png')))
        self.ddr_i.addChild(item)

        directory = self.ddr.directory
        if not directory.is_valid:
            logger.error('passed invalid DDR leader')
            return False
        item = QtWidgets.QTreeWidgetItem()
        item.setText(1, self.iso_dict['DDR_DIR'])
        item.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'dir.png')))
        self.ddr_i.addChild(item)

        dda = self.ddr.dda
        if not dda.is_valid:
            logger.error('passed invalid DDR DDA')
            return False
        dda_item = QtWidgets.QTreeWidgetItem()
        dda_item.setText(1, self.iso_dict['DDA'])
        dda_item.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'dda.png')))
        self.ddr_i.addChild(dda_item)

        # if not self.ddf.ddr.area.fields_list:
        #     logger.error('passed empty DDA fields list')
        #     return False
        # for i, tag in enumerate(self.ddf.ddr.area.tags_list):
        #     tag_item = QtGui.QTreeWidgetItem()
        #     tag_item.setText(1, "%s" % tag)
        #     tag_item.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'tag.png')))
        #     dda_item.addChild(tag_item)

        return True

    def _show_drs(self):
        if not self.root:
            logger.error('passed empty root item')
            return False
        self.drs = self.iso.input_ddf.drs
        if len(self.drs) == 0:
            logger.error('passed empty DRs')
            return False

        self.drs_i = QtWidgets.QTreeWidgetItem()
        self.drs_i.setText(1, self.iso_dict['DRs'])
        self.drs_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'drs.png')))
        self.root.addChild(self.drs_i)

        for i, dr in enumerate(self.drs):
            dr_i = QtWidgets.QTreeWidgetItem()
            dr_i.setText(1, '#%05d' % i)
            dr_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'dr.png')))
            self.drs_i.addChild(dr_i)

            if not dr.leader.is_valid:
                logger.error('passed invalid DR #%d Leader' % i)
                return False
            item = QtWidgets.QTreeWidgetItem()
            item.setText(1, self.iso_dict['DR_LDR'])
            item.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'ldr.png')))
            dr_i.addChild(item)

            if not dr.directory.is_valid:
                logger.error('passed invalid DR #%d Directory' % i)
                return False
            item = QtWidgets.QTreeWidgetItem()
            item.setText(1, self.iso_dict['DR_DIR'])
            item.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'dir.png')))
            dr_i.addChild(item)

            if not dr.uda.is_valid:
                logger.error('passed invalid DR #%d UDA' % i)
                return False
            uda_i = QtWidgets.QTreeWidgetItem()
            uda_i.setText(1, self.iso_dict['UDA'])
            uda_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'uda.png')))
            dr_i.addChild(uda_i)

        #     # fields
        #     for field in dr.area.tags_list:
        #         field_i = QtGui.QTreeWidgetItem()
        #         field_i.setText(1, '%s' % field)
        #         field_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'fld.png')))
        #         uda_i.addChild(field_i)

        return True

    def _add_to_viewer(self, info_list):
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
        if par_item:
            par_name = par_item.text(1)
        else:
            par_name = None
        if grand_par_item:
            grand_par_name = grand_par_item.text(1)
        else:
            grand_par_name = None

        if item_name == self.iso_dict['DDF']:
            self._viewer.append("%s\n\n" % (self.iso))
            self._viewer.append("%s\n\n%s" % (self.iso, self.ddf))
        elif item_name == self.iso_dict['DDR']:
            self._viewer.append("%s" % self.ddr)
        elif item_name == self.iso_dict['DDR_LDR']:
            self._viewer.append("%s" % self.ddr.leader)
        elif item_name == self.iso_dict['DDR_DIR']:
            self._viewer.append("%s" % self.ddr.directory)
        elif item_name == self.iso_dict['DDA']:
            self._viewer.append("%s" % self.ddr.dda)
        elif item_name == self.iso_dict['DRs']:
            self._viewer.append("Data records: %s" % len(self.drs))
        elif item_name[:1] == b'#':
            dr_nr = int(item_name[1:])
            self._viewer.append("%s" % self.drs[dr_nr])
        elif item_name == self.iso_dict['DR_LDR']:
            dr_nr = int(par_name[1:])
            self._viewer.append("%s" % self.drs[dr_nr].leader)
        elif item_name == self.iso_dict['DR_DIR']:
            dr_nr = int(par_name[1:])
            self._viewer.append("%s" % self.drs[dr_nr].directory)
        elif item_name == self.iso_dict['UDA']:
            dr_nr = int(par_name[1:])
            self._viewer.append("%s" % self.drs[dr_nr].uda)
        # else:
        #     if par_name == self.iso_dict['DDA']:
        #         e_idx = self.ddf.ddr.area.tags_list.index(item_name)
        #         element = self.ddf.ddr.area.fields_list[e_idx]
        #         self._add_to_viewer(element.info_list)
        #     elif par_name == b'Data':
        #         self.progress.forceShow()
        #         self.progress.setValue(30)
        #
        #         dr_nr = int(grand_par_name[1:])
        #         e_idx = self.ddf.dr_list[dr_nr].area.tags_list.index(item_name)
        #         element = self.ddf.dr_list[dr_nr].area.fields_list[e_idx]
        #         self._add_to_viewer(element.info_list)
        #     elif grand_par_name == b'Data':
        #         self.progress.forceShow()
        #         self.progress.setValue(30)
        #
        #         dr_nr = int(grand_par_item.parent().text()[1:])
        #         # print('subfield: %s' % dr_nr)
        else:
            logger.warning('invalid selection')

        self.progress.end()

    def make_context_menu(self):
        logger.debug('context menu')

    def clear_data(self):
        logger.debug('clear data')
        self.iso = None
        self.ddf = None
        self.ddr = None
        self.drs = None
        # tree elements
        self.ddr_i = None
        self.drs_i = None
        self.dr_list = None
        self.root = None
        self.clear()

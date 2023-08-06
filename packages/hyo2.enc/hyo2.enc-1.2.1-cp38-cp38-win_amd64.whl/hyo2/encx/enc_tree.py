import os

from PySide2 import QtWidgets, QtGui, QtCore

import logging
logger = logging.getLogger(__name__)

from hyo2.abc.app.qt_progress import QtProgress


class ENCTree(QtWidgets.QTreeWidget):

    here = os.path.abspath(os.path.join(os.path.dirname(__file__)))  # to be overloaded
    media = os.path.join(here, "media")

    enc_dict = {
        'ENC_FILE': 'ENC File',
        'META_OBJS': 'Meta Objects',
        'COLL_OBJS': 'Collections',
        'GEO_OBJS': 'Geo Objects',
        'GROUP1_OBJS': 'Skin of the earth',
        'GROUP2_OBJS': 'Other objects',
        'VEC_OBJS': 'Vector Objects',
        'ISOL_NODES': 'Isolated Nodes',
        'CONN_NODES': 'Connected Nodes',
        'EDGES': 'Edges',
    }

    def __init__(self, par_win=None):
        QtWidgets.QTreeWidget.__init__(self)
        self.par_win = par_win
        self.enc = None

        # items
        self.root = None
        # feature-specific
        self.metas_i = None
        self.colls_i = None
        self.geos_i = None
        self.group1_i = None
        self.group2_i = None
        # vector-specific
        self.vecs_i = None
        self.isol_nodes_i = None
        self.conn_nodes_i = None
        self.edges_i = None

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

    def show_enc(self, enc):
        self.clear_data()
        self.enc = enc

        if not self.enc:
            logger.error('passed empty ENC file')
            return False

        # create root tree item
        self.root = QtWidgets.QTreeWidgetItem(None)
        self.root.setText(1, self.enc_dict['ENC_FILE'])
        self.root.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'file.png')))
        self.addTopLevelItem(self.root)
        if self.root:
            self.setCurrentItem(self.root)

        # add feature sub-tree
        success = self._show_objects()
        if not success:
            return False

        # add vector sub-tree
        success = self._show_vectors()
        if not success:
            return False

        return True

    def _show_objects(self):
        if not self.root:
            logger.error('passed empty root item')
            return False

        _ = self._show_meta_objects()
        _ = self._show_collections()
        _ = self._show_features()

        return True

    def _show_meta_objects(self):
        if not self.enc.meta_objects:
            logger.error('passed empty meta object list')
            return False

        self.colls_i = QtWidgets.QTreeWidgetItem()
        self.colls_i.setText(1, self.enc_dict['COLL_OBJS'])
        self.colls_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'coll.png')))
        self.root.addChild(self.colls_i)

        for i, obj in enumerate(self.enc.collections):
            obj_i = QtWidgets.QTreeWidgetItem()
            obj_i.setText(1, '%s' % obj.name)
            obj_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'obj.png')))
            self.colls_i.addChild(obj_i)

        return True

    def _show_collections(self):
        if not self.enc.collections:
            logger.error('passed empty collection list')
            return False

        self.metas_i = QtWidgets.QTreeWidgetItem()
        self.metas_i.setText(1, self.enc_dict['META_OBJS'])
        self.metas_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'meta.png')))
        self.root.addChild(self.metas_i)

        for i, obj in enumerate(self.enc.meta_objects):
            rec_i = QtWidgets.QTreeWidgetItem()
            rec_i.setText(1, '%s' % obj.name)
            rec_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'obj.png')))
            self.metas_i.addChild(rec_i)

        return True

    def _show_features(self):
        if not self.enc.group1 or not self.enc.group2:
            logger.error('passed empty group 1 and group 2 lists')
            return False

        self.geos_i = QtWidgets.QTreeWidgetItem()
        self.geos_i.setText(1, self.enc_dict['GEO_OBJS'])
        self.geos_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'geo.png')))
        self.root.addChild(self.geos_i)

        if self.enc.group1:
            self.group1_i = QtWidgets.QTreeWidgetItem()
            self.group1_i.setText(1, self.enc_dict['GROUP1_OBJS'])
            self.group1_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'group1.png')))
            self.geos_i.addChild(self.group1_i)

            for i, obj in enumerate(self.enc.group1):
                rec_i = QtWidgets.QTreeWidgetItem()
                rec_i.setText(1, '%s' % obj.name)
                rec_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'obj.png')))
                self.group1_i.addChild(rec_i)

        if self.enc.group2:
            self.group2_i = QtWidgets.QTreeWidgetItem()
            self.group2_i.setText(1, self.enc_dict['GROUP2_OBJS'])
            self.group2_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'group2.png')))
            self.geos_i.addChild(self.group2_i)

            for i, obj in enumerate(self.enc.group2):
                rec_i = QtWidgets.QTreeWidgetItem()
                rec_i.setText(1, '%s' % obj.name)
                rec_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'obj.png')))
                self.group2_i.addChild(rec_i)

        return True

    def _show_vectors(self):
        if not self.enc.isolated_nodes or not self.enc.connected_nodes or not self.enc.edges:
            logger.error('passed empty vectors')
            return False

        self.vecs_i = QtWidgets.QTreeWidgetItem()
        self.vecs_i.setText(1, self.enc_dict['VEC_OBJS'])
        self.vecs_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'vec.png')))
        self.root.addChild(self.vecs_i)

        if self.enc.isolated_nodes:
            self.isol_nodes_i = QtWidgets.QTreeWidgetItem()
            self.isol_nodes_i.setText(1, self.enc_dict['ISOL_NODES'])
            self.isol_nodes_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'isol_node.png')))
            self.vecs_i.addChild(self.isol_nodes_i)

            for i, obj in enumerate(self.enc.isolated_nodes):
                rec_i = QtWidgets.QTreeWidgetItem()
                rec_i.setText(1, '%s' % obj.id)
                rec_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'obj.png')))
                self.isol_nodes_i.addChild(rec_i)

        if self.enc.connected_nodes:
            self.conn_nodes_i = QtWidgets.QTreeWidgetItem()
            self.conn_nodes_i.setText(1, self.enc_dict['CONN_NODES'])
            self.conn_nodes_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'conn_node.png')))
            self.vecs_i.addChild(self.conn_nodes_i)

            for i, obj in enumerate(self.enc.connected_nodes):
                rec_i = QtWidgets.QTreeWidgetItem()
                rec_i.setText(1, '%s' % obj.id)
                rec_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'obj.png')))
                self.conn_nodes_i.addChild(rec_i)

        if self.enc.edges:
            self.edges_i = QtWidgets.QTreeWidgetItem()
            self.edges_i.setText(1, self.enc_dict['EDGES'])
            self.edges_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'edge.png')))
            self.vecs_i.addChild(self.edges_i)

            for i, obj in enumerate(self.enc.edges):
                rec_i = QtWidgets.QTreeWidgetItem()
                rec_i.setText(1, '%s' % obj.id)
                rec_i.setIcon(0, QtGui.QIcon(os.path.join(self.media, 'obj.png')))
                self.edges_i.addChild(rec_i)

        return True

    def _add_to_viewer(self, info_list):
        for info in info_list:
            info_tag = ("%s:" % info[0]).ljust(20)
            self._viewer.append("%s %s" % (info_tag, info[1]))

    def new_selection(self):
        self.progress.start()
        self.progress.update(30)

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

        if item_name == self.enc_dict['ENC_FILE']:
            self._add_to_viewer(self.enc.info_list)
        elif item_name == self.enc_dict['META_OBJS']:
            self._add_to_viewer([('meta objects', '%d' % len(self.enc.meta_objects)),])
        elif item_name == self.enc_dict['COLL_OBJS']:
            self._add_to_viewer([('collections', '%d' % len(self.enc.collections)),])
        elif item_name == self.enc_dict['GEO_OBJS']:
            self._add_to_viewer([('group 1', '%d' % len(self.enc.group1)),
                                 ('group 2', '%d' % len(self.enc.group2))
                                 ])
        elif item_name == self.enc_dict['GROUP1_OBJS']:
            self._add_to_viewer([('group 1', '%d' % len(self.enc.group1))])
        elif item_name == self.enc_dict['GROUP2_OBJS']:
            self._add_to_viewer([('group 2', '%d' % len(self.enc.group2))])
        elif item_name == self.enc_dict['VEC_OBJS']:
            self._add_to_viewer([('isolated nodes', '%d' % len(self.enc.isolated_nodes)),
                                 ('connected nodes', '%d' % len(self.enc.connected_nodes)),
                                 ('edges', '%d' % len(self.enc.edges))
                                 ])
        elif item_name == self.enc_dict['ISOL_NODES']:
            self._add_to_viewer([('isolated nodes', '%d' % len(self.enc.isolated_nodes))])
        elif item_name == self.enc_dict['CONN_NODES']:
            self._add_to_viewer([('connected nodes', '%d' % len(self.enc.connected_nodes))])
        elif item_name == self.enc_dict['EDGES']:
            self._add_to_viewer([('edges', '%d' % len(self.enc.edges))])
        else:
            if par_name == self.enc_dict['META_OBJS']:
                obj_idx = par_item.indexOfChild(sel_item)
                self._add_to_viewer(self.enc.meta_objects[obj_idx].info_list)
            elif par_name == self.enc_dict['COLL_OBJS']:
                obj_idx = par_item.indexOfChild(sel_item)
                self._add_to_viewer(self.enc.collections[obj_idx].info_list)
            elif par_name == self.enc_dict['GROUP1_OBJS']:
                obj_idx = par_item.indexOfChild(sel_item)
                self._add_to_viewer(self.enc.group1[obj_idx].info_list)
            elif par_name == self.enc_dict['GROUP2_OBJS']:
                obj_idx = par_item.indexOfChild(sel_item)
                self._add_to_viewer(self.enc.group2[obj_idx].info_list)
            elif par_name == self.enc_dict['ISOL_NODES']:
                obj_idx = par_item.indexOfChild(sel_item)
                self._add_to_viewer(self.enc.isolated_nodes[obj_idx].info_list)
            elif par_name == self.enc_dict['CONN_NODES']:
                obj_idx = par_item.indexOfChild(sel_item)
                self._add_to_viewer(self.enc.connected_nodes[obj_idx].info_list)
            elif par_name == self.enc_dict['EDGES']:
                obj_idx = par_item.indexOfChild(sel_item)
                self._add_to_viewer(self.enc.edges[obj_idx].info_list)
            else:
                logger.warning('invalid selection')

        self.progress.end()

    def make_context_menu(self):
        logger.debug('context menu')

    def clear_data(self):
        logger.debug('clear data')
        self.enc = None
        self.root = None
        self.clear()

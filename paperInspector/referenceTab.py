from PySide6.QtCore import Slot
from backend.referenceTab.reference import Reference
from PySide6.QtWidgets import QFileDialog
from PySide6 import QtGui
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
import log

class ReferenceTab:

    def __init__(self, app):
        self.app = app
        self.window = app.window
        self.backend = app.backend
        self.table = self.window.refTableView

        self.model = RefTab(self.app)
        self.table.setModel(self.model)
        self.set_interaction_logic()
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView)

    def set_interaction_logic(self):

        self.window.addButton.clicked.connect(self._on_add_click)
        self.window.removeButton.clicked.connect(self._on_remove_click)
        self.window.parseButton.clicked.connect(self._on_parse)
        

    @Slot()
    def _on_add_click(self):

        # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QFileDialog.html#PySide6.QtWidgets.PySide6.QtWidgets.QFileDialog.getOpenFileNames
        refPaths, selectedFilter = QFileDialog.getOpenFileNames(
            caption="Select one or more files to open", filter="PDF (*.pdf)", dir="Desktop")

        for refPath in refPaths:

            # widgetres = []
            # # 获取listwidget中条目数
            # count = window.refView.count()
            # 遍历listwidget中的内容
            # for i in range(count):
            #     widgetres.append(self.listWidget.item(i).text())
            # print(widgetres)
            refTitle = refPath.split('/')[-1]
            if refTitle not in self.model.references:
                # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QListWidget.html
                # self.window.refView.addItem(QListWidgetItem(refTitle))
                self.model.addRef(refTitle, refPath)
                self.model.layoutChanged.emit()

            else:
                continue
        self.table.resizeColumnsToContents()
        self.update()
        log.applog.info(f'add {len(refPaths)} references')

    @Slot()
    def _on_remove_click(self):
        
        selecteds = self.table.selectedIndexes()
        toDelete = []
        for index in selecteds[1::self.model.columnCount()]:
            toDelete.append(self.model.data(index, role=Qt.DisplayRole))
        self.backend.removeRef(toDelete)
        
        self.model.layoutChanged.emit()
        self.update()
        log.applog.info(f'remove {len(toDelete)} references')

    @Slot()
    def _on_parse(self):
        self.backend.parse_ref()

    def update(self):
        self.window.refCountNum.setText(str(self.model.rowCount()))


class RefTab(QAbstractTableModel):

    def __init__(self, app):
        super().__init__()
        self.app = app
        self.columnName = ['Status', 'Title', 'Author', 'Journal', 'Year']

    @property
    def references(self):
        return self.app.backend.references

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.references)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.columnName) 

    def data(self, index: QModelIndex, role: int):
        i = index.row()
        j = index.column()
        columnName = self.columnName[j].lower()

        if role == Qt.DisplayRole and columnName != 'status':
            return f'{getattr(self.references[i], columnName, "None")}'

        if role == Qt.DecorationRole and columnName == 'status':
            parsed = self.references[i].isParsed

            if parsed:
                return QtGui.QIcon('assets/tick.png')
            return QtGui.QIcon('assets/cross.png')

    def headerData(self, section, orientation, role):
        # section: int
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columnName[section]
            if orientation == Qt.Vertical:
                return section

    def addRef(self, refTitle, refPath):

        self.app.backend.addRef(refTitle, refPath)


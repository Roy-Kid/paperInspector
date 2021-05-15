from PySide6 import QtCore
from PySide6.QtGui import QStandardItemModel
from PySide6.QtWidgets import QFileDialog, QListWidgetItem, QTableView
from base import Tab
from PySide6.QtCore import QAbstractListModel, QAbstractTableModel, QModelIndex, Slot, Qt

class Reference:

    def __init__(self, title, path):
        self.title = title
        self.path = path

    def __eq__(self, o: object) -> bool:
        return self.title == o

    def __str__(self) -> str:
        return f'<Reference: {self.title}>'

    __repr__ = __str__

class RefTab(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self.references = []
        self.columnName = ['title', 'author', 'journal', 'year']

    def rowCount(self, parent=QModelIndex()) -> int:
        return len(self.references)

    def columnCount(self, parent=QModelIndex()) -> int:
        return len(self.columnName) 

    def data(self, index: QModelIndex, role: int):
        if role == Qt.DisplayRole:
            i = index.row()
            j = index.column()
            return f'{getattr(self.references[i], self.columnName[j], "None")}'

    def headerData(self, section, orientation, role):
        # section: int
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return self.columnName[section]
            if orientation == Qt.Vertical:
                return section


class ReferenceTab(Tab):

    def __init__(self, app, window, backend):
        super().__init__(app, window, backend)

        self.table = self.window.refTableView
        self.model = RefTab()
        self.table.setModel(self.model)

    @property
    def references(self):
        return self.model.references

    @property
    def columnName(self):
        return self.model.columnName

    def set_interaction_logic(self):

        ####### Reference Count Section #######
        self.window.addButton.clicked.connect(self._on_add_click)
        self.window.removeButton.clicked.connect(self._on_remove_click)
        

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
            if refTitle not in self.references:
                # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QListWidget.html
                # self.window.refView.addItem(QListWidgetItem(refTitle))
                self.model.references.append(Reference(refTitle, refPath))
                self.model.layoutChanged.emit()

            else:
                continue

        self.update()

    @Slot()
    def _on_remove_click(self):
        
        selecteds = self.table.selectedIndexes()
        toDelete = []
        for index in selecteds[::self.model.columnCount()]:
            toDelete.append(self.references[index.row()].title)

        self.model.references = [ref for ref in self.references if ref not in toDelete]
        self.model.layoutChanged.emit()
        print(self.references)

    def update(self):
        self.window.refCountNum.setText(str(self.model.rowCount()))

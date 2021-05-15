# from backend.referenceTab.refParse import ParseQueue

from PySide6.QtCore import Slot
from backend.referenceTab.reference import RefTab, Reference
from PySide6.QtWidgets import QFileDialog
from base import Tab



class ReferenceTab(Tab):

    def __init__(self, app, window, backend):
        super().__init__(app, window, backend)

        self.table = self.window.refTableView

        self.model = RefTab()
        self.table.setModel(self.model)
        # self.table.horizontalHeader().setSectionResizeMode(QHeaderView)

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
            if refTitle not in self.references:
                # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QListWidget.html
                # self.window.refView.addItem(QListWidgetItem(refTitle))
                self.model.references.append(Reference(refTitle, refPath))
                self.model.layoutChanged.emit()

            else:
                continue
        self.table.resizeColumnsToContents()
        self.update()

    @Slot()
    def _on_remove_click(self):
        
        selecteds = self.table.selectedIndexes()
        toDelete = []
        for index in selecteds[::self.model.columnCount()]:
            toDelete.append(self.references[index.row()].title)

        self.model.references = [ref for ref in self.references if ref not in toDelete]
        self.model.layoutChanged.emit()
        self.update()

    @Slot()
    def _on_parse(self):
        self.backend.parse_ref(self.references, self.window)

        # self.parseQueue = ParseQueue(self.references, self.window)
        # self.parseQueue.updateProgress.connect(lambda x: self.window.progressBar.setValue(x))
        # self.parseQueue.start()

    def update(self):
        self.window.refCountNum.setText(str(self.model.rowCount()))



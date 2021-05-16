from PySide6 import QtGui
from PySide6.QtCore import QAbstractTableModel, QModelIndex, Qt
from itertools import compress

class Reference:

    def __init__(self, title, path):
        self.title = title
        self.path = path
        self.isParsed = False

    def __eq__(self, o: object) -> bool:
        return self.title == o

    def __str__(self) -> str:
        return f'<Reference: {self.title}>'

    __repr__ = __str__

    @property
    def excludedWords(self):
        return list(compress(self.words, self.exclude_word_mask))

class RefTab(QAbstractTableModel):

    def __init__(self):
        super().__init__()
        self.references = []
        self.columnName = ['Status', 'Title', 'Author', 'Journal', 'Year']

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

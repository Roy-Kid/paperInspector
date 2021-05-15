from backend.referenceTab.parser import PdfParser
from PySide6.QtCore import QModelIndex, QThread, Signal, Slot


class ParseQueue(QThread):

    updateProgress = Signal(int)


    def __init__(self, references, window):
        super().__init__()

        self.references = references
        self.window = window
        self.parser = PdfParser()

    @Slot()
    def run(self):

        total = len(self.references)

        for i, ref in enumerate(self.references):
            # update progress

        
            # actual work
            if ref.isParsed is False:
                self.parser(ref)
            else:
                continue

            progress = int(i*100/total)
            self.updateProgress.emit(progress)
            

        self.updateProgress.emit(100)
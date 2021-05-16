from backend.referenceTab.parser import PdfParser
from PySide6.QtCore import QThread, Signal, Slot


class RefParseWorker(QThread):

    updateProgress = Signal(int)


    def __init__(self, model, references, window):
        super().__init__()
        self.model = model
        self.references = references
        self.window = window
        self.parser = PdfParser()

    @Slot()
    def run(self):

        total = len(self.references)

        for i, ref in enumerate(self.references):

            if ref.isParsed is False:
                self.parser(ref)
            else:
                continue
            index = self.model.index(i, 0)
            progress = int(i*100/total)
            self.updateProgress.emit(progress)    
            self.model.dataChanged.emit(index, index)

        self.updateProgress.emit(100)


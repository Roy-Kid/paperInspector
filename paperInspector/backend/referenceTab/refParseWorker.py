from backend.referenceTab.parser import PdfParser
from PySide6.QtCore import QModelIndex, QRunnable, Signal, Slot, QObject
import log


class WokerSignals(QObject):

    finished = Signal()
    progress = Signal(int)
    # error = Signal(str)
    # result = Signal(dict)


class RefParseWorker(QRunnable):

    signals = WokerSignals()
    
    def __init__(self, backend):
        super().__init__()
        self.backend = backend
        self.references = backend.references

        self.parser = PdfParser()

    @Slot()
    def run(self):

        for i, ref in enumerate(self.references, 1):

            log.applog.info(f'parsing {ref.title}...')
            if ref.isParsed is False:
                self.parser(ref)
            else:
                continue

            self.signals.progress.emit(int(i*100/len(self.references)))

        self.signals.finished.emit()


from backend.scihubTab.scihubpy.scihub.scihub import SciHub
from PySide6.QtCore import QObject, QThread, Signal, Slot

class WokerSignals(QObject):

    finished = Signal()
    error = Signal(str)
    result = Signal(dict)

class ScihubWorker(QThread):

    signals = WokerSignals()

    def __init__(self, backend, execFn, *args, **kwargs) -> None:
        super().__init__()
        self.sh = backend.sh
        self.execFn = execFn
        self.args = args
        self.kwargs = kwargs


    @Slot()
    def run(self):

        result = self.execFn(*self.args)
            
        self.signals.result.emit(result)

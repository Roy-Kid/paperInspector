
from PySide6.QtCore import QObject, QThread, Signal, Slot
import sys

class WokerSignals(QObject):

    start = Signal()
    finish = Signal()
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

        self.signals.start.emit()

        try:
            result = self.execFn(*self.args)
            self.signals.result.emit(result)
        except ValueError as e:
            self.signals.error.emit(e)
            self.signals.finish.emit()
        else:
            print('error: ', sys.exc_info[0] )
            self.signals.error.emit(sys.exc_info[0])
            self.signals.finish.emit()

        self.signals.finish.emit()
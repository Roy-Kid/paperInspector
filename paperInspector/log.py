# version: 0.0.1
# data: 2021.05.22
# author: Roy Kid
# contact: lijichen365@126.com

from PySide6.QtCore import QObject, Signal

import logging

logging.basicConfig(level=logging.WARNING,
                    # filename='paperInspector.log',
                    # filemode='w',
                    format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'
                )
# logging.info('test')

applog = logging.getLogger('app')
applog.setLevel(logging.INFO)

class QLogSingal(QObject):

    logSignal = Signal(str)

class QLogHandler(logging.Handler):

    def __init__(self, emitter):
        super().__init__()
        self._emitter = emitter
        self.setFormatter(logging.Formatter('[%(name)s %(levelname)s]: %(message)s  --  %(filename)s[line:%(lineno)d]'))

    def bind_gui(self, widget):
        self.emitter.logSignal.connect(widget.appendPlainText)

    @property
    def emitter(self):
        return self._emitter

    def emit(self, record):
        msg = self.format(record)
        self.emitter.logSignal.emit(msg)

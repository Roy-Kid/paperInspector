# version: 0.0.1
# data: 2021.04.26
# author: Roy Kid
# contact: lijichen365@126.com


from referenceTab import ReferenceTab
import sys

from PySide6.QtCore import QFile, QIODevice, QObject, Signal
# sys.path.append(os.getcwd())
from backend.backend import Backend
from scihubTab import ScihubTab
from wordFreqTab import WordFreqTab
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from backend.backend import Backend
from log import QLogHandler, QLogSingal, applog


class PaperSpider:

    def __init__(self) -> None:
        self.app, self.window = self.initUI("mainWindow.ui")
        self.applog = applog
        QlogHandler = QLogHandler(QLogSingal())
        QlogHandler.bind_gui(self.window.logBrowser)
        self.applog.addHandler(QlogHandler)
        self.applog.info('Welcome to use paperInspector!')


        self.backend = Backend(self)

        self.referenceTab = ReferenceTab(self)
        self.model = self.referenceTab.model
        self.applog.info('referenceTab init successfully')
        
        self.scihubTab = ScihubTab(self)

        self.applog.info('scihubTab init successfully')
        # self.wordFreqTab = WordFreqTab(self.window)


    def initUI(self, uiname):

        app = QApplication(sys.argv)

        ui_file_name = uiname
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            self.applog.critical(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        window = loader.load(ui_file)
        window.setWindowTitle('paperInspector')
        ui_file.close()
        if not window:
            self.applog.critical(loader.errorString())
            sys.exit(-1)
        window.show()

        window.logBrowser.setReadOnly(True)
        window.logBrowser.setStyleSheet("background-color: transparent;")
        # set the log box to half of the size
        # window.logBrowser.setMaximumHeight(window.logBrowser.sizeHint().height()/2)

        return app, window

if __name__ == "__main__":

    mainWindow = PaperSpider()

    exec_ = mainWindow.app.exec_()

    sys.exit(exec_)


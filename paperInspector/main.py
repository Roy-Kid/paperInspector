# version: 0.0.1
# data: 2021.04.26
# author: Roy Kid
# contact: lijichen365@126.com


from referenceTab import ReferenceTab
import sys, os, logging

from PySide6.QtCore import QFile, QIODevice, QThreadPool
# sys.path.append(os.getcwd())
from backend.backend import Backend
from scihubTab import ScihubTab
from wordFreqTab import WordFreqTab
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from backend.backend import Backend

### log section ###
LOG_FORMAT = logging.BASIC_FORMAT
DATE_FORMAT = '%Y-%m-%d  %H:%M:%S %a '

# record software status
log = logging.getLogger('root')
log.addHandler(logging.StreamHandler())
# record gui info
loggui = logging.getLogger('gui')
# record scihubTab info
logsh = logging.getLogger('sh')
# record wordFreqTab info
logwf = logging.getLogger('wf')


class PaperSpider:

    def __init__(self) -> None:
        
        self.app, self.window = self.initUI("mainWindow.ui")
        self.backend = Backend(self)

        self.referenceTab = ReferenceTab(self)
        self.model = self.referenceTab.model
        

        self.scihubTab = ScihubTab(self)
        # self.wordFreqTab = WordFreqTab(self.window)



    def initUI(self, uiname):

        app = QApplication(sys.argv)

        ui_file_name = uiname
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            loggui.critical(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        window = loader.load(ui_file)
        window.setWindowTitle('paperInspector')
        ui_file.close()
        if not window:
            loggui.critical(loader.errorString())
            sys.exit(-1)
        window.show()

        window.logBrowser.setReadOnly(True)
        window.logBrowser.setStyleSheet("background-color: transparent;")
        # set the log box to half of the size
        # window.logBrowser.setMaximumHeight(window.logBrowser.sizeHint().height()/2)

        return app, window

if __name__ == "__main__":

    log.info(f'paperInspector launch')

    mainWindow = PaperSpider()

    exec_ = mainWindow.app.exec_()

    log.info(f'paperInspector terminate')

    sys.exit(exec_)


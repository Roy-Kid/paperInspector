# version: 0.0.1
# data: 2021.04.26
# author: Roy Kid
# contact: lijichen365@126.com


import sys, os
# sys.path.append(os.getcwd())
from PySide6.QtGui import QAction, QImage, QPixmap
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QFileDialog, QGraphicsPixmapItem, QGraphicsScene, QMenu
from PySide6.QtCore import QFile, QIODevice, Slot
from backend.backend import Backend


class Scihub:

    def __init__(self, app, window, backend) -> None:
        self.app = app
        self.window = window
        self.backend = backend

        self.SOURCE = []

        self.window.sourceList.addItems(self.SOURCE)

        self.window.refIdentifierEdit.setPlaceholderText('DOI|PMID|URL')
        self.window.proxyEdit.setPlaceholderText('http://127.0.0.1:8889')

        self.set_interaction_logic()

    def set_interaction_logic(self):

        self.window.refreshSourceButton.clicked.connect(self._on_refresh)
        self.window.submitButton.clicked.connect(self._on_submit)
        self.window.setProxyButton.clicked.connect(self._on_proxy_set)
        self.window.downloadButton.clicked.connect(self._on_download)

    @Slot()
    def _on_submit(self):
        refSource = self.window.refIdentifierEdit.text()
        data = self.backend.parse_doi_arXiv(refSource)
        self.window.metaDataDisplay.setPlainText(str(data))

    @Slot()
    def _on_refresh(self):
        # set both min & max to 0 to switch progressBar to BUSY state
        # see: https://doc.qt.io/qtforpython/PySide6/QtWidgets/QProgressBar.html
        # use progressBar.setValue(int) to determine progress
        self.window.progressBar.setMinimum(0)
        self.window.progressBar.setMaximum(0)
        urls = self.backend.find_avaliable_scihub_urls()
        self.window.sourceList.addItems(urls)
        self.window.progressBar.setMinimum(0)
        self.window.progressBar.setMaximum(100)

    @Slot()
    def _on_proxy_set(self):
        proxy = self.window.proxyEdit.text()
        print(proxy)
        self.backend.set_proxy_using_by_scihub(proxy)

    @Slot()
    def _on_proxy_clear(self):
        self.backend.clear_proxy_using_by_scihub()

    @Slot()
    def _on_download(self):
        refSource = self.window.refIdentifierEdit.text()
        self.backend.download_from_scihub(refSource)

class PaperSpider:

    def __init__(self) -> None:
        self.app, self.window = self.initUI("mainWindow.ui")

        # OOPize:
        # self.wordfreqModule = WordFreq()
        self.backend = Backend()
        self.set_interaction_logic()
        self.scihubModule = Scihub(self.app, self.window, self.backend)


    def initUI(self, uiname):
        # release mode
        # TODO: convert .ui to py code
        app = QApplication(sys.argv)


        ui_file_name = uiname
        ui_file = QFile(ui_file_name)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        window = loader.load(ui_file)
        ui_file.close()
        if not window:
            print(loader.errorString())
            sys.exit(-1)
        window.show()

        window.logBrowser.setReadOnly(True)
        window.logBrowser.setStyleSheet("background-color: transparent;")
        # set the log box to half of the size
        # window.logBrowser.setMaximumHeight(window.logBrowser.sizeHint().height()/2)

        return app, window

    def set_interaction_logic(self):

        ####### Reference Count Section #######
        self.window.addButton.clicked.connect(self._on_add_click)
        self.window.removeButton.clicked.connect(self._on_remove_click)

        ####### Word Freq Section #############
        # TODO: right click menu
        # https://blog.csdn.net/qq_39858109/article/details/108778860
        self.window.calcWordFreqButton.clicked.connect(self._on_calculate_word_freq)

        ####### Scihub Section ################

    @Slot()
    def _on_add_click(self):

        # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QFileDialog.html#PySide6.QtWidgets.PySide6.QtWidgets.QFileDialog.getOpenFileNames
        self.refPaths, selectedFilter = QFileDialog.getOpenFileNames(
            caption="Select one or more files to open", filter="PDF (*.pdf)", dir="Desktop")
        # add refname to the item container
        self.refNames = []
        for refPath in self.refPaths:

            # widgetres = []
            # # 获取listwidget中条目数
            # count = window.refList.count()
            # 遍历listwidget中的内容
            # for i in range(count):
            #     widgetres.append(self.listWidget.item(i).text())
            # print(widgetres)
            refName = refPath.split('/')[-1]
            if refName not in self.refNames:
                # https://doc.qt.io/qtforpython/PySide6/QtWidgets/QListWidget.html
                self.window.refListView.addItem(refName)
                self.refNames.append(refName)
            else:
                continue

        self.update()

    @Slot()
    def _on_remove_click(self):
        
        selecteds = self.window.refListView.selectedIndexes()
        
        for selected in selecteds:
            index = selected.row()
            self.window.refListView.takeItem(index)
            print(self.refNames)
            del self.refNames[index]
            del self.refPaths[index]
            print(self.refNames)
        # self.update()

    @Slot()
    def _on_calculate_word_freq(self):
        # one reference
        # selected = self.window.refListView.currentIndex().row()
        # refPath = self.refPaths[selected]
        selecteds = self.window.refListView.selectedIndexes()
        selectedRefPaths = []
        for selected in selecteds:
            selectedRefPaths.append(self.refPaths[selected.row()])

        self.backend.update_refs(selectedRefPaths)
        wordCloudDraw = self.backend.drawWordCloud()

        # binary
        biWordCloudDraw = wordCloudDraw.to_array()


        x = biWordCloudDraw.shape[1]
        y = biWordCloudDraw.shape[0]
        channel = biWordCloudDraw.shape[2]
        frame = QImage(biWordCloudDraw, x, y, QImage.Format_RGB888)
        pix = QPixmap.fromImage(frame)
        scene = QGraphicsScene()
        item = QGraphicsPixmapItem(pix)
        scene.addItem(item)

        self.window.wordCloudView.setScene(scene)
        
        def fit_view():
            self.window.wordCloudView.fitInView(item)

        def save_image():
            wordCloudDraw.to_file('wc.png')

        rezoom = QAction(self.window.wordCloudView)
        rezoom.setText('Rezoom')
        rezoom.triggered.connect(fit_view)

        save = QAction(self.window.wordCloudView)
        save.setText('Save')
        save.triggered.connect(save_image)

        self.window.wordCloudView.addAction(rezoom)
        self.window.wordCloudView.addAction(save)



        
    def update(self):
        self.window.refCountNum.setText(str(self.window.refListView.count()))


if __name__ == "__main__":


    
    mainWindow = PaperSpider()

    sys.exit(mainWindow.app.exec_())

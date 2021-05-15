from base import Tab
from PySide6.QtCore import Slot

from PySide6.QtGui import QAction, QImage, QPixmap

from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsScene
from PySide6.QtCore import Slot


class WordFreqTab(Tab):

    def __init__(self, app, window, backend):
        super().__init__(app, window, backend)

    def set_interaction_logic(self):

        ####### Word Freq Section #############
        # TODO: right click menu
        # https://blog.csdn.net/qq_39858109/article/details/108778860
        self.window.calcWordFreqButton.clicked.connect(self._on_calculate_word_freq)

    @Slot()
    def _on_calculate_word_freq(self):
        # one reference
        # selected = self.window.refListView.currentIndex().row()
        # refPath = self.refPaths[selected]
        selecteds = self.window.refListView.selectedIndexes()
        selectedRefPaths = []
        for selected in selecteds:
            selectedRefPaths.append(self.app.referenceTab.refPaths[selected.row()])

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

from PySide6.QtCore import Slot


class ScihubTab:

    def __init__(self, app) :
        self.app = app
        self.window = app.window

        self.window.refIdentifierEdit.setPlaceholderText('DOI|PMID|URL')
        self.window.proxyEdit.setPlaceholderText('http://127.0.0.1:8889')


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
        self.backend.set_proxy_using_by_scihub(proxy)

    @Slot()
    def _on_proxy_clear(self):
        self.backend.clear_proxy_using_by_scihub()

    @Slot()
    def _on_download(self):
        refSource = self.window.refIdentifierEdit.text()
        self.backend.download_from_scihub(refSource)
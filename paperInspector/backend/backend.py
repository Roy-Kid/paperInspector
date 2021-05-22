# version: 0.0.1
# data: 2021.04.26
# author: Roy Kid
# contact: lijichen365@126.com


from PySide6.QtCore import QThreadPool
from backend.scihubTab.scihubpy.scihub.scihub import SciHub
from backend.referenceTab.reference import Reference
from backend.scihubTab.scihubWorker import ScihubWorker
from backend.referenceTab.refParseWorker import RefParseWorker
import log

class Backend:

    def __init__(self, app) -> None:
        self.app = app
        self.references = []
        self.sh = SciHub()
        self.threadpool = QThreadPool()

    def addRef(self, refTitle, refPath):
        self.references.append(Reference(refTitle, refPath))

    def removeRef(self, refTitles):
        self.references = [ref for ref in self.references if ref not in refTitles]

    # def update_refs(self, refPaths):

    #     #! TODO: incremental update
    #     for refPath in refPaths:
    #         if refPath not in self.refPaths:
    #             self.refPaths.append(refPath)
    #             pdfperser = PdfParser(refPath)

    #             # ---npl process section---
    #             # e.g. exclude verbose

    #             # ---npl process end---
    #             self.refPDFParsers.append(pdfperser)

    # def drawWordCloud(self):
    #     words = []
    #     for parser in self.refPDFParsers:
    #         words.extend(parser.extract_words())
    #     from collections import Counter

    #     import wordcloud

    #     word_counts = Counter(words)
        
    #     with open('word_counts', 'w', encoding='utf-8') as f:
    #         f.write(str(word_counts))
        
    #     wordCloudDraw = wordcloud.WordCloud()
    #     wordCloudDraw.generate_from_frequencies(word_counts)
    #     return wordCloudDraw  # "WordFreQ.png")

    # def fetch_from_scihub(self, source):
    #     sh = getattr(self, 'scihub', None)
    #     if sh is None:
    #         self.scihub = SciHub()
    #         sh = self.scihub

        # fetch specific article (don't download to disk)
        # this will return a dictionary in the form 
        # {'pdf': PDF_DATA,
        #  'url': SOURCE_URL,
        #  'name': UNIQUE_GENERATED NAME
        # }
    #     return sh.fetch(source)

    def find_avaliable_scihub_urls(self):
    
        log.applog.info('retrieving available urls...')

        execFn = self.sh.get_available_scihub_urls
        self.scihubWorker = ScihubWorker(self, execFn)
        self.scihubWorker.signals.start.connect(lambda x=0: self.app.window.progressBar.setMaximum(x))
        self.scihubWorker.signals.finish.connect(lambda x=100: self.app.window.progressBar.setMaximum(x))
        try:
            self.scihubWorker.run()
            return self.sh.available_base_url_list
        except:
            log.applog.error('check_hostname requires server_hostname, may set proxy first')

        return ''


    def set_proxy_using_by_scihub(self, proxy):
        log.applog.info(f'proxy set {proxy}')
        self.sh.set_proxy(proxy)

    def clear_proxy_using_by_scihub(self):

        log.applog.info(f'proxy clear')
        self.sh.clear_proxy()

    def download_from_scihub(self, source):


        if self.sh.base_url:

            log.applog.info(f'downloading {source}...')
            execFn = self.sh.download
            # test doi: DOI: 10.1063/1.2357935
            self.scihubWorker = ScihubWorker(self, execFn, source)
            self.scihubWorker.signals.start.connect(lambda x=0: self.app.window.progressBar.setMaximum(x))
            self.scihubWorker.signals.finish.connect(lambda x=100: self.app.window.progressBar.setMaximum(x))
            self.scihubWorker.run()
            self.scihubWorker.signals.start.connect(lambda x: self.app.window.progressBar.setMaximum(0))

            self.scihubWorker.signals.finish.connect(lambda x: self.app.window.progressBar.setMaximum(100))
            log.applog.info(f'done.')

        else:
            self.find_avaliable_scihub_urls()

    def parse_doi_arXiv(self, identifier):
        execFn = self.sh.cite
        log.applog.info(f'fetching {identifier}')
        self.scihubWorker = ScihubWorker(self, execFn, identifier)
        
        self.scihubWorker.signals.start.connect(lambda x: self.app.window.progressBar.setMaximum(0))

        self.scihubWorker.signals.finish.connect(lambda x: self.app.window.progressBar.setMaximum(100))

        self.scihubWorker.signals.result.connect(lambda x: self.app.window.metaDataDisplay.setPlainText(str(x)))
        self.scihubWorker.start()
# self.app.window.metaDataDisplay.setPlainText
    def parse_ref(self):

        def refresh_status(i):
            index = self.app.model.index(i, 0)
            index.data = True
            self.app.model.dataChanged.emit(index, index)

        self.refParseWorker = RefParseWorker(self)

        self.refParseWorker.signals.progress.connect(lambda x: self.app.window.progressBar.setValue(x))
        self.refParseWorker.signals.progress.connect(refresh_status)
        self.refParseWorker.signals.finished.connect(lambda x=100: self.app.window.progressBar.setValue(x))

        self.threadpool.start(self.refParseWorker)

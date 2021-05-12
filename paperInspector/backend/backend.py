# version: 0.0.1
# data: 2021.04.26
# author: Roy Kid
# contact: lijichen365@126.com

import os, yaml, sys
from backend.scihubTab.RefParse.refparse.api import RefAPI
from backend.wordfreqTab.parser import PdfParser
from backend.scihubTab.scihubpy.scihub.scihub import SciHub


class Backend:

    def __init__(self) -> None:
        self.refPaths = []
        self.refPDFParsers = []

    def update_refs(self, refPaths):

        #! TODO: incremental update
        for refPath in refPaths:
            if refPath not in self.refPaths:
                self.refPaths.append(refPath)
                pdfperser = PdfParser(refPath)

                # ---npl process section---
                # e.g. exclude verbose

                # ---npl process end---
                self.refPDFParsers.append(pdfperser)

    def drawWordCloud(self):
        words = []
        for parser in self.refPDFParsers:
            words.extend(parser.extract_words())
        from collections import Counter

        import wordcloud

        word_counts = Counter(words)
        
        with open('word_counts', 'w', encoding='utf-8') as f:
            f.write(str(word_counts))
        
        wordCloudDraw = wordcloud.WordCloud()
        wordCloudDraw.generate_from_frequencies(word_counts)
        return wordCloudDraw  # "WordFreQ.png")

    def fetch_from_scihub(self, source):
        sh = getattr(self, 'scihub', None)
        if sh is None:
            self.scihub = SciHub()
            sh = self.scihub

        # fetch specific article (don't download to disk)
        # this will return a dictionary in the form 
        # {'pdf': PDF_DATA,
        #  'url': SOURCE_URL,
        #  'name': UNIQUE_GENERATED NAME
        # }
        return sh.fetch(source)

    def find_avaliable_scihub_urls(self):
        
        sh = getattr(self, 'scihub', None)
        if sh is None:
            self.scihub = SciHub()
            sh = self.scihub

        return sh.available_base_url_list

    def set_proxy_using_by_scihub(self, proxy):
        sh = getattr(self, 'scihub', None)
        if sh is None:
            self.scihub = SciHub()
            sh = self.scihub
        
        sh.set_proxy(proxy)

    def clear_proxy_using_by_scihub(self):
        sh = getattr(self, 'scihub', None)
        if sh is None:
            self.scihub = SciHub()
            sh = self.scihub

        sh.clear_proxy()

    def download_from_scihub(self, source):
        sh = getattr(self, 'scihub', None)
        if sh is None:
            self.scihub = SciHub()
            sh = self.scihub

        sh.download(source)

    def parse_doi_arXiv(self, reference):

        CURPATH = os.path.dirname(os.path.realpath(__file__))

        with open(os.path.join(CURPATH, "scihubTab/RefParse/refparse/config.yaml"), "r") as config:
            FORMAT_CONFIG = yaml.load(config, Loader=yaml.SafeLoader)

        formats = list(FORMAT_CONFIG.keys())

        for ref_format in formats:
            if ref_format not in FORMAT_CONFIG:
                # TODO: add a log
                # cli_logger.error(f"{ref_format} not defined")
                return

        api = RefAPI(reference, FORMAT_CONFIG)
        results = []
        if api.status:
            for ref_format in formats:
                results.append((ref_format, api.render(ref_format)))

        return results


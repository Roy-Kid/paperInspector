# version: 0.0.1
# data: 2021.04.26
# author: Roy Kid
# contact: lijichen365@126.com

# https://github.com/jsvine/pdfplumber
import pdfplumber

class PdfParser:

    template = {
            'UNDEFINED': {
                'bounding_box': (1,2,3,4)
            },
            'JACS': {
                'bounding_box': (1,2,3,4)  #(x0, top, x1, bottom)
            }
        }

    def __init__(self, pdfPath, journal='UNDEFINED') -> None:
        self.pdfPath = pdfPath
        self.pdfname = pdfPath.split('/')[-1]
        self.journal = journal
        self.pdf, self.metadata, self.pages = self._parse(self.pdfname)


    def _parse(self, pdfname):

        # pdf is a pdfplumber.PDF instance
        pdf = pdfplumber.open(pdfname)
            
        # pdf has two properties: metadata..
        metadata = pdf.metadata

        # ...and pages:list contains per page:Page
        pages = pdf.pages

        # TODO: template of the journals
        # e.g. JACS: {
        #   'top': 13mm
        #   'buttom': 13mm} etc. 

        # then use the data of template to crop(clipping) the page
        # how to crop the pages is referred in the methods of pdfplumber.Page class
        
        # pages = [p.crop(self.template[self.journal]['bounding_box'], relative=False) for p in pages]

        return pdf, metadata, pages


    def extract_words(self) -> list:

        """ 提取文中的单词, 以单词出现在文中的位置为准. 返回的是包含大量dict的list, 每一个dict包含单词本身'text', 和跟位置有关的各种是属性

        """

        self.words = []
        for p in self.pages:

            rawSeq = p.extract_words(x_tolerance=3, y_tolerance=3, keep_blank_chars=False, use_text_flow=False, horizontal_ltr=True, vertical_ttb=True, extra_attrs=[])

            for r in rawSeq:
                self.words.append(r['text'])

        return self.words

    def extract_text(self, x_tolerence=3, y_tolerance=3):

        """ 提取文中所有的字母至一个字符串

        Returns:
            [type]: [description]
        """

        text = []
        for p in self.pages:
            text += p.extract_text()
        return text

    def extract_table(self,):
        pass

    def destroy_parser(self):
        self.pdf.close()
        
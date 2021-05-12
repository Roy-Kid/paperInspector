# version: 0.0.1
# data: 2021.04.26
# author: Yunqi Li
# contact: lijichen365@126.com

class NPL:

    def __init__(self) -> None:

        self._originalWords = []
        self._processedWords = []

    @property
    def originalWords(self):
        return self.originalWords

    @originalWords.setter
    def originalWords(self, words):
        self._originalWords = words

    @property
    def processedWords(self):
        return self._processedWords

    def exclude_verbose(self, custom_rule:list):

        self.EXCLUDE_VERBOSE = {'the', 'and', 'for', 'are', 'was', 'were', 'from', 'fig', 'this', 'that', 'high', 'which', 'using', 'with',
                                'such', 'data', 'after', 'under', 'figure', 'have', 'values', 'two', '2015', 'side', 'more', 'these'}
        
        self.EXCLUDE_VERBOSE = self.EXCLUDE_VERBOSE.union(set(custom_rule))

        def exclude_rules(word):

            if word not in self.EXCLUDE_VERBOSE and \
               len(word) < 15:
               return True
            
            else:
                return False

        # TODO: optimize with mask
        words = []
        for word in self.originalWords:
            if exclude_rules(word):
                words.append(words)

        self.processedWords = words
        return self.processedWords

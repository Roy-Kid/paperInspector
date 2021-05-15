# version: 0.0.1
# data: 2021.04.26
# author: Yunqi Li
# contact: lijichen365@126.com

class NPL:

    def __init__(self) -> None:
        self.EXCLUDE_VERBOSE = {'the', 'and', 'for', 'are', 'was', 'were', 'from', 'fig', 'this', 'that', 'high', 'which', 'using', 'with',
                                'such', 'data', 'after', 'under', 'figure', 'have', 'values', 'two', '2015', 'side', 'more', 'these'}
        
    def update_verbose(self, customRule:list):

        self.EXCLUDE_VERBOSE = self.EXCLUDE_VERBOSE.union(set(customRule))

    def exclude_verbose(self, ref):

        ref.exclude_word_mask = [0 if word in self.EXCLUDE_VERBOSE else 1 for word in ref.words]


from itertools import compress

class Reference:

    def __init__(self, title, path):
        self.title = title
        self.path = path
        self.isParsed = False

    def __eq__(self, o: object) -> bool:
        return self.title == o

    def __str__(self) -> str:
        return f'<Reference: {self.title}>'

    __repr__ = __str__

    @property
    def excludedWords(self):
        return list(compress(self.words, self.exclude_word_mask))

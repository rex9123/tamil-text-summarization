from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.util import ngrams
from util.freader import FileReader

class Preprocessor:
  def __init__(self, filePath, ngrams=1):
    self.reader = FileReader(filePath)
    self.ngrams = ngrams
    self.sentences = [ ]
    self.processed = [ ]
    self.paragraphStructure = { }
    self.sCount = 0
    self.pCount = 0

  def parse(self):
    self.reader.read( self.process )
    return self

  def process(self, paragraph):
    for sentence in sent_tokenize(paragraph):
      self.sentences.append( sentence )

      grams = list(ngrams(word_tokenize(sentence), self.ngrams))

      self.processed.append( map(lambda g: " ".join(g), grams) )

      self.paragraphStructure[self.sCount] = self.pCount
      self.sCount = self.sCount + 1

    self.pCount = self.pCount + 1




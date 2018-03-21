import os.path
import math
import operator
import unicodecsv as csv
from textblob import Sentence
from decimal import Decimal


def tf(word, blob):
    return Decimal(blob.words.count(word)) / Decimal(len(blob.words))


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word, bloblist):
    term = Decimal(len(bloblist)) / Decimal((1 + n_containing(word, bloblist)))
    if term == 0:
        return Decimal(0)
    return Decimal(math.log(term))


def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)


def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
    csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
    for row in csv_reader:
        yield [unicode(cell, 'utf-8') for cell in row]


inputPath = os.path.join(os.getcwd(), "1-sentences")
outputPath = os.path.join(os.getcwd(), "2-tf-isf")
listOfFiles = [os.path.join(inputPath, inputTextFile) for inputTextFile in os.listdir(inputPath) if os.path.isfile(os.path.join(inputPath, inputTextFile))]

if not os.path.isdir(outputPath):
    os.mkdir(outputPath)

for inputTextFile in listOfFiles:
    print(inputTextFile)
    with open(inputTextFile, 'r') as content_file:
        csvReader = csv.reader(content_file)
        sentences = [Sentence(sentenceText) for row in csvReader for sentenceText in row]
        for sentence in sentences:
            tfidfCache = {}
            for word in sentence.words:
                string = word.encode("utf-8")
                if string in tfidfCache:
                    continue
                tfidfCache[string] = tfidf(word, sentence, sentences)
            sorted_x = sorted(tfidfCache.items(), key=operator.itemgetter(1))
            print sentence
            print(sorted_x)

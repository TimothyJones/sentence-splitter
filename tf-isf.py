import os.path
import math
import unicodecsv as csv


def tf(word, blob):
    return blob.words.count(word) / len(blob.words)


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word, bloblist):
    return math.log(len(bloblist) / (1 + n_containing(word, bloblist)))


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
        for row in csvReader:
            for sentence in row:
                print("Sentence:" + sentence)

import os.path
import codecs
import re
import unicodecsv as csv
from textblob import TextBlob


inputPath = os.path.join(os.getcwd(), "input")
outputPath = os.path.join(os.getcwd(), "1-sentences")
listOfFiles = [os.path.join(inputPath, inputTextFile) for inputTextFile in os.listdir(inputPath) if os.path.isfile(os.path.join(inputPath, inputTextFile))]

if not os.path.isdir(outputPath):
    os.mkdir(outputPath)

for inputTextFile in listOfFiles:
    print(inputTextFile)
    with codecs.open(inputTextFile, 'r', 'utf-8', 'ignore') as content_file:
        text = TextBlob(content_file.read())
        sentences = [re.sub('\s+', ' ', str(s)) for s in text.sentences]
        with open(os.path.join(outputPath, os.path.basename(inputTextFile)), 'wb') as outputCsvFile:
            writer = csv.writer(outputCsvFile, encoding='utf-8')
            writer.writerow(sentences)

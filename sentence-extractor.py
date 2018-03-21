import os.path
import codecs
from textblob import TextBlob


inputPath = os.path.join(os.getcwd(), "input")
listOfFiles = [os.path.join(inputPath, f) for f in os.listdir(inputPath) if os.path.isfile(os.path.join(inputPath, f))]


for f in listOfFiles:
    print(f)
    with codecs.open(f, 'r', 'utf-8') as content_file:
        text = TextBlob(content_file.read())
        print(text.sentences)

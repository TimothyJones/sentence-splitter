import os.path
import math
import operator
import unicodecsv as csv
from textblob import Sentence
from nltk.corpus import stopwords
import sklearn.metrics
import scipy.sparse

from decimal import Decimal


def tf(word, blob):
    return Decimal(blob.words.count(word)) / Decimal(len(blob.words))


def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)


def idf(word, bloblist):
    term = Decimal(len(bloblist)) / Decimal(n_containing(word, bloblist))
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

stopWords = set(stopwords.words('english'))

if not os.path.isdir(outputPath):
    os.mkdir(outputPath)

nextWordId = 1
wordIds = {}


def get_word_id(word_string):
    global nextWordId
    if word_string not in wordIds:
        wordIds[word_string] = nextWordId
        nextWordId += 1
    return wordIds[word_string]


def print_sentence(idx):
    global sentence_text_dict
    print "Sentence %d: %s " % (idx, sentence_text_dict[idx])
    print sentence_text_dict[idx].sentiment


num_sentences = 0

sm = scipy.sparse.dok_matrix((83, 650))

sentence_text_dict = {}

for inputTextFile in listOfFiles:
    print(inputTextFile)
    with open(inputTextFile, 'r') as content_file:
        csvReader = csv.reader(content_file)
        sentences = [Sentence(sentenceText) for row in csvReader for sentenceText in row]
        for sentence in sentences:
            tfidfCache = {}
            sentence_text_dict[num_sentences] = sentence
            for word in sentence.words:
                string = word.encode("utf-8")
                get_word_id(string)
                if string in tfidfCache or string in stopWords:
                    continue
                tfidfCache[string] = tfidf(word, sentence, sentences)
            sorted_x = sorted(tfidfCache.items(), key=operator.itemgetter(1), reverse=True)
            print num_sentences , sentence
            for wordString in tfidfCache:
                sm[num_sentences, get_word_id(wordString)] = tfidfCache[wordString]
            num_sentences += 1

sim = sklearn.metrics.pairwise.cosine_similarity(sm)

for i in range(len(sim)):
    maxIdx = -1
    maxScore = 0
    for j in range(len(sim[i])):
        if i != j and sim[i][j] > maxScore:
            maxScore = sim[i][j]
            maxIdx = j
    if maxIdx == -1:
        print "No match for sentence %d" % maxIdx
    else:
        print "Best match for sentence %d is sentence %d, with score %f"  %(i, maxIdx, maxScore)
        print_sentence(i)
        print_sentence(maxIdx)
    print
    print

print(sim[82,81])
print num_sentences


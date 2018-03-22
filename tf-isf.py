import os.path
import math
import operator
import csv
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
    print("Sentence {0}: {1} ".format(idx, sentence_text_dict[idx]))
    print(sentence_text_dict[idx].sentiment)


num_sentences = 0
num_documents = 0

sentence_text_dict = {}

all_sentences = []
sentence_to_docid = {}

# Read the data and count words / sentences
for inputTextFile in listOfFiles:
    print(inputTextFile)
    with open(inputTextFile, 'r', encoding='utf-8') as content_file:
        csvReader = csv.reader(content_file)
        sentences = [Sentence(sentenceText) for row in csvReader for sentenceText in row]
        all_sentences += sentences
        for sentence in sentences:
            sentence_text_dict[num_sentences] = sentence
            sentence_to_docid[num_sentences] = num_documents
            num_sentences += 1
            for word in sentence.words:
                string = word.encode("utf-8")
                get_word_id(string)
        num_documents += 1


print(all_sentences)
# Generate tf.idf scores and fill in the sparse matrix
tfidfMatrix = scipy.sparse.dok_matrix((num_sentences, nextWordId))
for sentence_id in sentence_text_dict:
    sentence = sentence_text_dict[sentence_id]
    tfidfCache = {}
    for word in sentence.words:
        string = word.encode("utf-8")
        if string in tfidfCache or string in stopWords:
            continue
        tfidfCache[string] = tfidf(word, sentence, all_sentences)
        sorted_x = sorted(tfidfCache.items(), key=operator.itemgetter(1), reverse=True)
        for wordString in tfidfCache:
            tfidfMatrix[sentence_id, get_word_id(wordString)] = tfidfCache[wordString]


sets = []

sim = sklearn.metrics.pairwise.cosine_similarity(tfidfMatrix)
for i in range(len(sim)):
    maxIdx = -1
    maxScore = 0
    for j in range(len(sim[i])):
        if i != j and sim[i][j] > maxScore:
            maxScore = sim[i][j]
            maxIdx = j
    if maxIdx == -1:
        print("No match for sentence {0}".format(i))
        print()
        print()
    else:
        print("Best match for sentence {0} is sentence {1}, with score {2}".format(i, maxIdx, maxScore))
        print_sentence(i)
        print_sentence(maxIdx)
        print()
        print()

        added = False
        for s in sets:
            if i in s or maxIdx in s:
                s.add(i)
                s.add(maxIdx)
                added = True
                break
        if not added:
            sets.append({i, maxIdx})

finalSets = set()

for s in sets:
    finalSet = s.copy()
    for other in sets:
        if not finalSet.isdisjoint(other):
            finalSet = finalSet.union(other)

    finalSets.add(frozenset(finalSet))


summaries = []

for s in finalSets:
    minId = -1
    minSubjectivity = 2
    docs_that_support = set()
    for id in s:
        if minSubjectivity > sentence_text_dict[id].sentiment.subjectivity and len(sentence_text_dict[id].words) > 4:
            minSubjectivity = sentence_text_dict[id].sentiment.subjectivity
            minId = id
        docs_that_support.add(sentence_to_docid[id])

    if minId == -1:
        continue

    summaries.append((len(docs_that_support), s,minId))

sorted_summaries = sorted(summaries, key=lambda x: x[0], reverse=True)

for t in sorted_summaries:
    s = t[1]
    print("{0} complaints (with {1} sentences) support sentence {2}: {3}".format(t[0],len(s),t[2],sentence_text_dict[t[2]]))
    for id in s:
        if id != minId:
            print("    {0}".format(sentence_text_dict[id]))
    print()
    print()


print(sim[82,81])
print(num_sentences, nextWordId)
print(sets)
print(finalSets)

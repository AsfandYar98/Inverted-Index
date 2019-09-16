import sys
import os
import io
import re
import operator
import nltk
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from collections import OrderedDict

if len(sys.argv) > 1:
    path_to_corpus = sys.argv[1]
    corpus_folder = os.path.join(os.getcwd(), path_to_corpus)
else:
    print("ERROR! Please enter the name of a directory containing the corpus documents.")
    exit()

if not os.path.exists(corpus_folder):
    print("ERROR '" + corpus_folder + "' does not exist or it is an invalid directory.")
    exit()

tokenizer = RegexpTokenizer(r'[a-zA-Z0-9]*[a-zA-Z][a-zA-Z0-9]*')
stemmer = PorterStemmer()
path_to_stopList = "stoplist.txt"
stopList_file = os.path.join(os.getcwd(), path_to_stopList)
stopWords = open(stopList_file).read()

open('docids.txt', 'w').close()
open('termids.txt', 'w').close()
open('term_index.txt', 'w').close()

termList = {}
index = {}
docID = 0
termID = 0
termFreq = 0
docFreq = 0

l = len(os.listdir(path_to_corpus))
with open("docids.txt", 'a', encoding='utf-8', errors='ignore') as map_doc, open("termids.txt", 'a', encoding='utf-8',
                                                                                 errors='ignore') as term_doc, open(
    "term_index.txt", 'a', encoding='utf-8', errors='ignore') as inverted_index:
    for filename in os.listdir(path_to_corpus):
        tmp = os.path.basename(filename)
        docTitle = tmp
        docID = docID + 1

        print("%.2f" % round(((docID / l) * 100), 2) + r"%\t" + docTitle + "\n");
        map_doc.write(str(docID) + "\t" + docTitle + "\r\n")

        readfile = open(path_to_corpus + r"//" + tmp, encoding='utf-8', errors='ignore').read()

        soup = BeautifulSoup(readfile, 'html.parser')
        if soup.html is None:
            text = ''
        else:
            soup = soup.html

            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip()
                      for line in lines for phrase in line.split(" "))
            text = ' '.join(chunk for chunk in chunks if chunk)

        del readfile

        tokens = tokenizer.tokenize(text)
        tokens = [token.lower() for token in tokens]
        tokens = [stemmer.stem(i) for i in tokens if i not in stopWords]

        for j in range(0, len(tokens)):
            if tokens[j] not in termList:
                termID = termID + 1
                termList[tokens[j]] = termID
                index[termID] = [1, 0, (docID, j)]
                term_doc.write(str(termList[tokens[j]]) + "\t" + tokens[j] + "\r\n")
            else:
                index[termList[tokens[j]]].append((docID, j))
                index[termList[tokens[j]]][0] = index[termList[tokens[j]]][0] + 1

print(index)

for key in index:
    tempDoc = 0
    tempPos = 0
    newTempDoc = 0
    newTempPos =0
    for i in range(len(index[key])):
        if i == 0 or i  == 1:
            continue
        elif i ==2:
            tempDoc = index[key][2][0]
            tempPos = index[key][2][1]
            index[key][1] = index[key][1] + 1
        else:
            if tempDoc == index[key][i][0]:
                newTempDoc = index[key][i][0]
                newTempPos = index[key][i][1]

                tuple =(newTempDoc - tempDoc, newTempPos - tempPos)
                index[key][i] = tuple

                tempDoc = newTempDoc
                tempPos = newTempPos

            elif tempDoc != index[key][i][0]:
                index[key][1] = index[key][1] + 1

                newTempDoc = index[key][i][0]
                newTempPos = index[key][i][1]

                tuple = (newTempDoc - tempDoc, index[key][i][1])
                index[key][i] = tuple

                tempDoc = newTempDoc
                tempPos = newTempPos


with open("term_index.txt", 'w', encoding='utf8') as termIndex:
    for key in index:
        termIndex.write("\n")
        termIndex.write(str(key) + "\t")

        for i in range(len(index[key])):
            if i==0:
                termIndex.write(str(index[key][0]) + "\t")
                termIndex.write(str(index[key][1]) + "\t")
                continue
            elif i==1:
                continue
            else:
                termIndex.write(str(index[key][i][0]) + "," + str(index[key][i][1]) + "\t")

del index
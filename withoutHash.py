import sys
import os
from nltk.tokenize import RegexpTokenizer
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer


def takeSecond(elem):
    return elem[1]


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

termList = []
index = []
docID = 0
termID = 0

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
                termList.insert(termID, tokens[j])
                index.append([docID, termID, j])
                term_doc.write(str(termID) + "\t" + tokens[j] + "\r\n")
            else:
                point = termList.index(tokens[j]) + 1
                index.append((docID, point, j))

index.sort(key=takeSecond)

listIndex = [[] for i in range(len(termList)+1)]

for i in range(len(index)):
    tuple = (index[i][0], index[i][2])
    listIndex[index[i][1]].append(tuple)

termfreq= [0 for term in range(len(listIndex)+1)]
docfreq = []
docfreq = [0 for doc in range(len(listIndex)+1)]


for key in range(len(listIndex)):

    tempDoc = 0
    tempPos = 0
    newTempDoc = 0
    newTempPos = 0


    if key == 0:
        continue
    else:
        for i in range(len(listIndex[key])):
            if i == 0:
                tempDoc = listIndex[key][0][0]
                tempPos = listIndex[key][0][1]
                docfreq[key] = 1
            else:
                if tempDoc == listIndex[key][i][0]:
                    newTempDoc = listIndex[key][i][0]
                    newTempPos = listIndex[key][i][1]

                    tuple =(newTempDoc - tempDoc, newTempPos - tempPos)
                    listIndex[key][i] = tuple

                    tempDoc = newTempDoc
                    tempPos = newTempPos

                elif tempDoc != listIndex[key][i][0]:
                    docfreq[key] = docfreq[key] + 1

                    newTempDoc = listIndex[key][i][0]
                    newTempPos = listIndex[key][i][1]

                    tuple = (newTempDoc - tempDoc, listIndex[key][i][1])
                    listIndex[key][i] = tuple

                    tempDoc = newTempDoc
                    tempPos = newTempPos

for key in range(len(listIndex)):

    if key == 0:
        continue
    else:
        termfreq[key] = len(listIndex[key])

with open("term_index.txt", 'w', encoding='utf8') as termIndex:
    for key in range(1, len(listIndex)):
        termIndex.write(str(key) + "\t")
        termIndex.write(str(termfreq[key]) + "\t")
        termIndex.write(str(docfreq[key]) + "\t")

        for i in range(len(listIndex[key])):
                termIndex.write(str(listIndex[key][i][0]) + "," + str(listIndex[key][i][1]) + "\t")

        termIndex.write("\n")
del listIndex
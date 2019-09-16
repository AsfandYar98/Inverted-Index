import os
import sys
from nltk.stem import PorterStemmer

if sys.argv[1] == '--term':

    stemmer = PorterStemmer()
    termName = stemmer.stem(sys.argv[2])

    term = ""
    with open("termids.txt", "r", encoding="utf8") as termIDs:
        for line in termIDs:
            if termName in line:
                datas = line.split()
                if termName == datas[1]:
                    term = datas[0]

    del termIDs
    if term == "":
        print("Term was not found in the corpus.\n")
    else:

        with open("term_index.txt", "r") as termIndex:
            for line in termIndex:
                if term in line:
                    datas = line.split()
                    if term == datas[0]:
                        print("Listing for term:\t" + termName + "\n")
                        print("TERMID:\t" + term + "\n")
                        print("Number of documents containing term:\t" + datas[2] + "\n")
                        print("Term frequency in corpus:\t" + datas[1] + "\n")
                        break;

else:
    print("ERROR! Please enter the query in correct format.")
    exit()

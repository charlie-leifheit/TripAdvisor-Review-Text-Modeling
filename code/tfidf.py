from __future__ import division
import csv

"""
This file uses TF-IDF to score all the words in the reviews and
sort them. 
"""

selectedPos = ["VERB"]

wordBag = []
with open('data/review_title_words-clean-park-names.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    line = 0
    for row in csv_reader:
        if (line == 0) : 
            line += 1
            continue
        park, year, word, count, pos = row[0], row[1], row[2], row[3], row[4]
        if park.lower().find(word) >= 0: continue
        if pos not in selectedPos: continue
        word += (","+pos)
        wordBag.append((park, word, count))
        line += 1

with open('data/review_body_words-clean-park-names.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    line = 0
    for row in csv_reader:
        if (line == 0) : 
            line += 1
            continue
        park, year, word, count, pos = row[0], row[1], row[2], row[3], row[4]
        if park.lower().find(word) >= 0: continue
        # if pos not in selectedPos: continue
        word += (","+pos)
        wordBag.append((park, word, count))
        line += 1

wordBagByPark = {}
for (park, word, count) in wordBag:
    if park not in wordBagByPark:
        wordBagByPark[park] = {}
    if word not in wordBagByPark[park]:
        wordBagByPark[park][word] = 0
    wordBagByPark[park][word] += int(count)

parks = sorted(wordBagByPark.keys())

tfidfByPark = {}
for park in parks:
    tfidf = []

    sumCount = 0
    for w in wordBagByPark[park].keys():
        sumCount += wordBagByPark[park][w]

    for w in wordBagByPark[park].keys():
        count = wordBagByPark[park][w]
        tf = count / sumCount

        numDocs = 0
        for p in parks:
            if w in wordBagByPark[p]:
                numDocs += 1
        idf = len(parks) / numDocs

        score = tf * idf
        tfidf.append([score, w])

    tfidf.sort()
    tfidf.reverse()
    tfidfByPark[park] = tfidf

data = []
data.append(["park","word","pos","tfidf"])
for park in parks:
    tfidf = tfidfByPark[park]
    for [s, w] in tfidf[0:25]:
        splits = w.split(",")
        word, pos = splits[0], splits[1]
        data.append([park, word, pos, str(s)])

with open('output/top25-everything-tfidf-by-park.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(data)






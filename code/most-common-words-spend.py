import csv

"""
This file opens the open refine consolidated table of visitor spending between 2012 and 2018
and creates a csv file of the top 25 words of a particular part of speech. 
"""

# selectedPos = ["ADJ", "ADV"]
# selectedPos = ["NOUN", "INTJ", "X"]
# selectedPos = ["VERB"]

bagofwords = {}
parks = {}
spending = {}

with open('data/2012-2018-national-park-spending-table.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0: 
            line_count += 1
            continue
        line_count += 1
        park,year,total_visitors,visitor_spending,average_spend = row[0], row[1], row[2], row[3], row[4]
        if (park not in spending):
            spending[park] = {}
        spend = visitor_spending[1:]
        spend = spend.replace(",","")
        try:
            spending[park][year] = [float(spend), average_spend]
        except Exception as e:
            spending[park][year] = [0.0, average_spend]

with open('data/review_title_words-clean-park-names.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0: 
            line_count += 1
            continue
        line_count += 1
        park, year, word, count, pos = row[0], row[1], row[2], row[3], row[4]
        
        # if pos not in selectedPos: continue
        if park.lower().find(word) >= 0: continue
        
        word = word + "," + pos

        if (park not in parks):
            parks[park] = {}
        if year not in parks[park]:
            parks[park][year] = {}
        if (word not in parks[park][year]):
            parks[park][year][word] = 0
        parks[park][year][word] += int(count)

for p in parks.keys():
    for y in parks[p].keys():
        for w in parks[p][y].keys():
            if w not in bagofwords:
                bagofwords[w] = 0
            bagofwords[w] += parks[p][y][w]

wordOrder = sorted(bagofwords.items(), key=lambda kv: kv[1])
wordOrder.reverse()
wordOrder = wordOrder[:25]

topWords = []
for (wordpos, count) in wordOrder:
    splits = wordpos.split(",")
    word, pos = splits[0], splits[1]
    topWords.append(word)

data = []
data.append(["park", "year"] + topWords + ["spending", "average_spend"])
for p in sorted(parks.keys()):
    for y in range(2012, 2019):
        if str(y) not in parks[p]: continue
        counts = []
        err = 0
        for i in range(len(wordOrder)):
            try:
                c = parks[p][str(y)][wordOrder[i][0]]
            except Exception as e:
                c = str(0)
                err += 1
            counts.append(c)
        if err < 20:
            data.append([p, str(y)] + counts + [spending[p][str(y)][0], spending[p][str(y)][1][1:]])

with open('output/park-top25-all-spend.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(data)
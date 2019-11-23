import csv

"""
This file drops the extra columns in the spending table 
and only retains park name, year, and visitor spending. 
"""

spending = {}

with open('data/2012-2018-national-park-spending-table.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0: 
            line_count += 1
            continue
        line_count += 1
        park,year,total_visitors,visitor_spending = row[0], row[1], row[2], row[3]
        if (park not in spending):
            spending[park] = {}
        spend = visitor_spending[1:]
        spend = spend.replace(",","")
        try:
            spending[park][year] = float(spend)
        except Exception as e:
            spending[park][year] = 0.0

data = []
data.append(["park"] + range(2012,2019) + ["2019"])
for p in sorted(spending.keys()):
    yearlyspend = []
    for y in range(2012, 2019):
        yearlyspend.append(spending[p][str(y)])
    data.append([p] + yearlyspend)

with open('output/park-spend-by-year.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(data)
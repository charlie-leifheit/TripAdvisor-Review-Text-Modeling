import csv
import numpy as np
from sklearn.linear_model import LinearRegression

"""
This file runs a simple regression model using existing spending
from 2012 to 2018 and predicts the spending for 2019 and 2020. 
"""

method = LinearRegression()
x = np.array([2012,2013,2014,2015,2016,2017,2018]).reshape((-1, 1))
x2 = np.array([2019,2020]).reshape((-1, 1))
data =[]
data.append(["park"] + range(2012, 2019) + ["predicted 2019", "predicted 2020"])

with open('../data/park-spend-by-year.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line = 0
    for row in csv_reader:
        if (line == 0) : 
            line += 1
            continue
        park = row[0]
        yarray = []
        for i in range(1, 8):
            yarray.append(float(row[i]))
        y = np.array(yarray)

        model = method.fit(x, y)
        y_pred = model.predict(x2)
        data.append([park] + yarray + [round(y_pred[0], 2), round(y_pred[1], 2)])

outputData = []
outputData.append(["park", "year", "spending"])
for row in data[1:]:
    p = row[0]
    for y in range(2021-2012):
        outputData.append([p, 2012+y, row[1+y]])
print len(outputData)

with open('../model/park-spending-by-year-prediction-simple-regression.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(outputData)

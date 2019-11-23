import csv

"""
This file combines the file that includes ratings for each park 
and the file with park name, year, and visitor spend. 
"""

spending = {}
rating = {}

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
            spending[park][year] = [0.0, 0.0]

with open('data/user_ratings_table-clean-park-names.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0: 
            line_count += 1
            continue
        line_count += 1
        park, year, user_rating, rating_count, vote_count = row[0], row[1], row[2], row[3], row[4]
        if not (2012 <= int(year) <= 2018): continue
        if (park not in rating):
            rating[park] = {}
        if (year not in rating[park]):
            rating[park][year] = {}
        if (user_rating not in rating[park][year]):
            rating[park][year][user_rating] = {}
        rating[park][year][user_rating] = [rating_count, vote_count]

data = []
data.append(["park", "year", "rating_count_1", "rating_count_1",
                             "rating_count_2", "rating_count_2",
                             "rating_count_3", "rating_count_3",
                             "rating_count_4", "rating_count_4",
                             "rating_count_5", "rating_count_5",
                             "visitor_spend", "average_spend"])

for park in sorted(rating.keys()):
    for year in range(2012, 2019):
        year = str(year)
        rating_data = []
        if year not in rating[park]:
            rating_data = [0 for i in range(10)]
        else:
            for user_rating in range(1, 6):
                user_rating = str(user_rating)
                if user_rating not in rating[park][year]:
                    rating_data += [0, 0]
                else:
                    rating_data += rating[park][year][user_rating]
        data.append([park, year] + rating_data + spending[park][year])

with open('output/park-rating-spend.csv', 'w') as writeFile:
    writer = csv.writer(writeFile)
    writer.writerows(data)
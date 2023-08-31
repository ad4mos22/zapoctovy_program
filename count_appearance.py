import csv
from collections import Counter

input_file = 'input.csv'
output_file = 'output.csv'

input_file_info = []
with open(input_file, 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        input_file_info.extend(row)

movie_terms = []
with open('A_complete_data.csv', 'r') as file:
    reader = csv.DictReader(file)
    for row in reader:
        terms = row['term']
        movie_terms.extend(terms)

#count the occurrences of each term
term_counts = Counter(movie_terms)

#sort terms based on count and alphabetically
sorted_terms = sorted(term_counts.items(), key=lambda x: (-x[1], x[0]))

#write sorted genres to the X_genres.csv file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',')
    writer.writerow(['term', 'count'])
    writer.writerows(sorted_terms)

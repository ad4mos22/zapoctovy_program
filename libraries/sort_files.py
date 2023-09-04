import csv

input_file_path = "input.csv"
output_file_path = "output.csv"
term_name = 'term'

file_info = {}
with open(input_file_path, 'r') as file:
    reader = csv.DictReader(file, delimiter=',')
    for row in reader:
        term, count, idf = row[term_name], row['database frequency'], row['idf']
        file_info[term] = count, idf

sorted_data = sorted(file_info.items(), key=lambda x: (int(x[1][0]), x[0]), reverse=True)

with open(output_file_path, 'w', newline='') as file:
    fieldnames = [term, 'database frequency', 'idf']
    writer = csv.DictWriter(file, fieldnames=fieldnames, delimiter=',')
    writer.writeheader()
    for term, (count, idf) in sorted_data:
        writer.writerow({term_name: term, 'database frequency': count, 'idf': idf})

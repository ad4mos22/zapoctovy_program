import numpy as np
import csv

open_file = 'input.csv'
output_file = 'output.csv'
term_name = 'term'

def idf_calculation():
    file_info = {}

    with open(open_file, 'r', newline='', encoding='utf-8') as input_file:
        reader = csv.DictReader(input_file, delimiter=',')

        for row in reader:
            term, count = row[term_name], row["database frequency"]
            file_info[term] = count

    with open(output_file, 'w', newline='', encoding='utf-8') as output_file:
        writer = csv.writer(output_file, delimiter=',')
        writer.writerow([term_name, 'database frequency', 'idf'])  # Header

        for term, count in file_info.items():
            output_line = [term, count, f"{np.log(4660/int(count)):.4f}"]
            writer.writerow(output_line)

    print("done")

idf_calculation()
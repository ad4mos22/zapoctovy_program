import csv
import numpy as np

#read CSV file and parse vectors
normalized_vectors = []

with open('movie_vectors.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        #convert movie_id to integer
        movie_id = int(row["movie_id"])
        vector_str = row["vector"]

        #parse vector string and convert to floats
        vector = np.array([float(x) for x in vector_str[1:-1].split(',')])

        #calculate magnitude and normalize vector
        magnitude = np.linalg.norm(vector)
        normalized_vector = vector / magnitude

        normalized_vectors.append((movie_id, normalized_vector))

#save normalized vectors to a new CSV file
with open('normalized_vectors.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['movie_id', 'normalized_vector'])
    for movie_id, normalized_vector in normalized_vectors:
        #write movie_id and normalized vector as values, not strings
        writer.writerow([movie_id, *normalized_vector])

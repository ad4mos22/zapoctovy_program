import csv
import numpy as np


file_info = {}

#read the data from the csv file
with open("A_data.csv", "r") as file:
    reader = csv.DictReader(file, delimiter=";")
    
    for row in reader:
        movie_id, title, year, imdb, duration, director, actor, genres, keywords = row["ID"], row["Title"], row["Year"], row["IMDb"], row["Duration"], row["Director"], row["Actor"], row["Genre"], row["Keywords"]
        file_info[movie_id] = genres.split("|"), keywords.split("|"), actor, director

vector_info = []

#read the terms and their idf from the csv file
with open("vector_info.csv", "r") as vector_file:
    reader = csv.DictReader(vector_file, delimiter=",")
    for row in reader:
        term, df, idf = row["term"], row["database frequency"], row["idf"]
        vector_info.append([term, idf])

#write the vectors for each movie to a csv file
with open("movie_vectors.csv", "w") as output_file:
    writer = csv.writer(output_file, delimiter=";")
    writer.writerow(["movie_id", "vector"])

    #for each term in the vector_info, check if it is in the movie's genres, keywords, actor or director
    #if it is, add the idf to the vector, else add 0
    for movie_id, (genres, keywords, actor, director) in file_info.items():
        vector = []
        for term, idf in vector_info:
            if term in genres or term in keywords or term == actor or term == director:
                vector.append(float(idf))
            else:
                vector.append(float(0))

        writer.writerow([movie_id, vector])
import csv
import numpy as np
import random


def handle_feedback(movie_vectors=list, uservector=np.array, feedback=bool, movie_id=int):
    #feedback represents whether the user liked the movie or not
    
    #initialize movie vector
    movievector = np.zeros((1399,), dtype=float)
    
    #find the movie vector of the movie that the user just watched
    for row in movie_vectors:
        if int(row["movie_id"]) == movie_id:
            movievector = np.array(list(map(float, row['normalized_vector'].split(','))))
            break

    #update user vector to be the sum of the user vector and the movie vector
    if feedback:    
        uservector = (uservector + movievector)/2
    
    #update user vector to be the difference of the user vector and the movie vector
    else:           
        uservector = (uservector - movievector)/2

    #normalize the user vector   
    normalized_user_vector = uservector / np.linalg.norm(uservector)

    return normalized_user_vector

def cosine_similarity(vector_a, vector_b):
    #calculate cosine similarity between two vectors
    
    dot_product = np.dot(vector_a, vector_b)
    magnitude_a = np.linalg.norm(vector_a)
    magnitude_b = np.linalg.norm(vector_b)
    
    #check for division by zero
    if magnitude_a == 0 or magnitude_b == 0:
        return 0
    else:
        similarity = dot_product / (magnitude_a * magnitude_b)
    
    return similarity

def get_recommendation(uservector=None, recommended_movies=None):
    #get the best recommendation for the user
    similarity_score = {}

    with open("normalized_vectors.csv", "r") as normalized_vectors_file:
        reader = csv.DictReader(normalized_vectors_file, delimiter=";")

        for row in reader:
            movie_id = int(row["movie_id"])
            normalized_vector = np.array(list(map(float, row['normalized_vector'].split(','))))

            similarity = cosine_similarity(uservector, normalized_vector)
            similarity_score[movie_id] = similarity
    
    #remove movies that have already been recommended
    similarity_score = {movie_id: similarity for movie_id, similarity in similarity_score.items() if movie_id not in recommended_movies}
    
    #loop until a movie that has not been recommended is found
    while True:
        best_recommendation = int(max(similarity_score, key=similarity_score.get, default=0))

        if best_recommendation not in recommended_movies:
            break
    
    #add the best recommendation to the list of recommended movies
    already_recommended(best_recommendation, recommended_movies)
    
    #return the movie id of the best recommendation
    return best_recommendation                      

def add_to_watchlist(movie_id=int, watchlist=list):
    #add a movie to the watchlist
    watchlist.append(movie_id)
    
    return None
    
def already_recommended(movie_id=int, recommended_movies=list):
    #add a movie to the list of movies that have already been recommended
    recommended_movies.append(movie_id)
    
    return None

def return_watchlist(watchlist=list):
    #return the watchlist
    return watchlist

def get_random_movies(recommended_movies=list):
    #to build up the users vector, star by recommending 10 random movies
    random_movies = []

    #generate 10 random movie ids
    for i in range(10):
        random_movies.append(random.randint(1, 4660))

        #make sure that the movie ids are unique               
        while random_movies[i] in random_movies[:i]:
            random_movies[i] = random.randint(1, 4660)

    #return the list of random movie ids
    return random_movies

def give_recommendations_list(uservector=np.array, recommended_movies=list):
    #give the user a list of 10 recommendations at the end of the program
    recommendations_list = []

    #get 10 recommendations
    for _ in range(10):

        recommendation = get_recommendation(uservector, recommended_movies)
        recommendations_list.append(recommendation)

        #add the recommendation to the list of already recommended movies
        recommended_movies.append(recommendation)  
    
    #return the list of recommendations
    return recommendations_list

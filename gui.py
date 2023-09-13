import tkinter as tk
from tkinter import messagebox
import csv
import numpy as np
from collections import deque
import backend as bk


def load_movie_data():
    """ 
    This function loads movie data from a csv file.

    Returns:
        movie_data (list): a list of dictionaries containing movie data
    """
    movie_data = []

    # open csv file and read data into a list
    with open('main_data/A_complete_data.csv', 'r') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            movie_data.append(row)

    return movie_data


def load_movie_vectors():
    """
    This function loads movie vectors from a csv file.

    Returns:
        movie_vectors (list): a list of dictionaries containing movie vectors
    """
    movie_vectors = []

    with open("main_data/normalized_vectors.csv", "r") as normalized_vectors_file:
        reader = csv.DictReader(normalized_vectors_file, delimiter=";")

        for row in reader:
            movie_vectors.append(row)

    # return a list of movie vectors
    return movie_vectors


class MovieRecommendationApp:
    """ 
    This class creates a GUI for the movie recommendation program.
    The GUI shows a movie title and information, and three buttons: "Like", "Dislike" and "End Program".

    The "Like" button shows the next movie, and adds the movie to the user's watchlist if the user wants to.
    The "Dislike" button shows the next movie, and does not add the movie to the user's watchlist.

    The program ends when the user clicks the "End Program" button.

    Variables:
    root: the root window
    movie_data: a list of dictionaries containing movie data
    current_movie_id: the id of the movie that is currently being shown
    already_recommended: a list of movie ids that have already been recommended
    watchlist: a list of movie ids that the user has added to their watchlist
    movie_queue: a queue of movie ids that are to be recommended
    user_vector: a vector that represents the user's preferences
    feedback: a boolean that represents the user's feedback

    """

    def __init__(self, root):
        """
        The constructor for the MovieRecommendationApp class.

        Parameters:
            root (tk.Tk): the root window
        """
        self.root = root
        self.root.title("Movie Recommendation Program")

        self.movie_data = load_movie_data()
        self.movie_vectors = load_movie_vectors()

        self.movie_title_label = tk.Label(
            root, text="", font=("Helvetica", 18))
        self.movie_title_label.pack(pady=10)

        self.movie_info_label = tk.Label(root, text="", font=("Helvetica", 12))
        self.movie_info_label.pack(pady=5)

        # create buttons
        self.like_button = tk.Button(
            root, text="Like", command=self.like_movie)
        self.like_button.pack(side="left", padx=10)

        self.dislike_button = tk.Button(
            root, text="Dislike", command=self.dislike_movie)
        self.dislike_button.pack(side="right", padx=10)

        self.end_button = tk.Button(
            root, text="End Program", command=self.end_program)
        self.end_button.pack(pady=20)

        # initialize variables
        self.current_movie_id = 0
        self.already_recommended = []
        self.watchlist = []
        self.movie_queue = deque()
        self.user_vector = np.zeros((1399,), dtype=float)
        self.feedback = True

        self.start_program()

    def start_program(self):
        """ 
        This function starts the program.
        It gets 10 random movie recommendations and adds them to the queue, so that user's profile can be created.
        """
        self.movie_list = bk.get_random_movies(self.already_recommended)
        self.movie_queue.extend(self.movie_list)
        self.show_movie(self.movie_queue)

    def show_movie(self, queue=deque):
        """
        This function shows a movie from the queue.
        It shows the movie title with brief information.

        Parameters:
            queue (deque): a queue of movie ids that are to be recommended
        """

        # show a first movie from the queue
        self.current_movie_id = queue.popleft()

        # check if the movie id is valid
        if self.current_movie_id <= 4660:
            # show the movie title and information, substract 1 from the movie id because the list is zero-indexed and the movie ids start at 1
            movie = self.movie_data[self.current_movie_id - 1]
            self.movie_title_label.config(text=movie['Title'])
            # convert keywords to a comma-separated string
            keywords = ', '.join(movie['Keywords'].split('|'))
            self.movie_info_label.config(
                text=f"Year: {movie['Year']} | IMDb: {movie['IMDb']} | Duration: {movie['Duration']} min\nGenres: {movie['Genre']}\nDirector: {movie['Director']}\nLeading actor: {movie['Actor']}\nPlot keywords: {keywords}")

        else:
            self.movie_title_label.config(text="No more movies.")
            self.movie_info_label.config(text="")
            self.end_program()

    def like_movie(self):
        """ 
        This function is called when the user clicks the "Like" button.
        It updates the user's feedback, adds the movie to the watchlist if the user wants to, and shows the next movie.
        """
        # update the feedback variable
        self.feedback = True
        movie = self.movie_data[self.current_movie_id-1]

        # update the user vector, so that the recommendation algorithm can learn from the user's feedback
        user_vector = self.user_vector
        self.user_vector = bk.handle_feedback(self.movie_vectors,
                                              user_vector,
                                              self.feedback,
                                              self.current_movie_id)

        # ask the user if they want to add the movie to their watchlist
        response = messagebox.askyesno(
            "Add to Watchlist", f"Do you want to add '{movie['Title']}' to your watchlist?")

        if response:
            bk.add_to_watchlist(self.current_movie_id, self.watchlist)
            pass

        # show the next movie, if there is one to be shown
        if self.movie_queue:
            self.show_movie(self.movie_queue)

        # if there are no more movies to be shown, recommend a new movie
        else:
            recommended_movie = bk.get_recommendation(
                self.user_vector, self.already_recommended)
            self.movie_queue.append(recommended_movie)
            self.show_movie(self.movie_queue)

    def dislike_movie(self):
        """
        This function is called when the user clicks the "Dislike" button.
        It updates the user's feedback, and shows the next movie.
        """

        # update the feedback variable, show the next movie
        self.feedback = False

        # update the user vector, so that the recommendation algorithm can learn from the user's feedback
        user_vector = self.user_vector
        self.user_vector = bk.handle_feedback(
            self.movie_vectors, user_vector, self.feedback, self.current_movie_id)

        # do not add the movie to the watchlist, or ask anything else

        # show the next movie, if there is one to be shown
        if self.movie_queue:
            self.show_movie(self.movie_queue)

        # if there are no more movies to be shown, recommend a new movie
        else:
            recommended_movie = bk.get_recommendation(
                self.user_vector, self.already_recommended)
            self.movie_queue.append(recommended_movie)
            self.show_movie(self.movie_queue)

    def display_recommendations(self):
        """ 
        This function displays 10 recommended movies based on the user's preferences. 
        """

        recommended_movies = bk.give_recommendations_list(
            self.user_vector, self.already_recommended)
        recommended_titles = [self.movie_data[movie_id - 1]
                              ['Title'] for movie_id in recommended_movies]

        recommended_text = "\n".join(recommended_titles)
        messagebox.showinfo("Recommendations",
                            f"Recommended movies:\n{recommended_text}")

    def end_program(self):
        """ 
        This function is called when the user clicks the "End Program" button.
        It hides the buttons, shows the user's watchlist and recommended movies, and closes the program.
        """

        # hide the buttons
        self.like_button.pack_forget()
        self.dislike_button.pack_forget()
        self.end_button.pack_forget()

        # get the user's watchlist
        watchlist = bk.return_watchlist()

        # get recommended movies for the user
        recommended_movies = bk.give_recommendations_list(
            self.user_vector, self.already_recommended)
        recommended_titles = [self.movie_data[movie_id - 1]
                              ['Title'] for movie_id in recommended_movies]

        # check if there are any movies in the watchlist
        if watchlist:
            watchlist_text = "\n".join(
                [self.movie_data[movie_id - 1]['Title'] for movie_id in self.watchlist])
        else:
            watchlist_text = "Your watchlist is empty."

        if recommended_titles:
            recommended_text = "\n".join(recommended_titles)
        else:
            recommended_text = "No more recommendations."

        # show the watchlist and recommended movies in a messagebox
        messagebox.showinfo(
            "Program Ended", f"Your watchlist:\n{watchlist_text}\n\nRecommended movies:\n{recommended_text}")

        # close the program
        self.root.destroy()

    def run(self):
        """ 
         This function runs the program.
        """
        self.root.mainloop()

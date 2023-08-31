from gui import MovieRecommendationApp
import tkinter as tk

#main file to run the program
if __name__ == "__main__":
    root = tk.Tk()  
    app = MovieRecommendationApp(root)
    app.run()

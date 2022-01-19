from flask import Flask, render_template, request, redirect, flash
from models import MovieManager


manager = MovieManager('https://www.imdb.com/chart/top/')
manager.preprocess()
manager.review_penalizer()
manager.oscar_calculator()

all_movies = manager.get_list()

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',methods=['GET'],items=all_movies)

if __name__ == "__main__":
    app.run(debug=False)
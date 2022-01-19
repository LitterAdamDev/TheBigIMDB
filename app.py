from flask import Flask, render_template, request, redirect, flash
from models import MovieManager

app = Flask(__name__)

@app.route("/",methods=['GET'])
def index():
    manager = MovieManager('https://www.imdb.com/chart/top/')
    manager.preprocess()
    manager.review_penalizer()
    manager.oscar_calculator()
    all_movies = manager.get_list()
    all_movies.sort(key=lambda x: x._rating_value, reverse=True)

    return render_template('index.html',items=all_movies)

if __name__ == "__main__":
    app.run(debug=True)
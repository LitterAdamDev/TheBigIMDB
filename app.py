from flask import Flask, render_template, send_file, session
from models import MovieManager
from datetime import timedelta
import os
import csv

app = Flask(__name__)
app.secret_key = "dzfJyr6ZcyGjRA7DozpPGEQjGcvDrL4P"
app.permanent_session_lifetime = timedelta(hours=6)

manager = MovieManager("https://www.imdb.com/chart/top/")


@app.route("/",methods=["GET","POST"])
def index():    
    if "movie_list" not in session:
        manager.preprocess()
        manager.review_penalizer()
        manager.oscar_calculator()
        movie_list = manager.get_list()
        jsonfied_list = [movie.__dict__ for movie in movie_list]
        session.permanent = True
        session["movie_list"] = jsonfied_list
    return render_template("index.html",items=session["movie_list"] if "movie_list" in session else [])

@app.route("/download", methods=["GET","POST"])
def download():
    os.makedirs("outputs/", exist_ok=True)
    with open("outputs/ratings.csv", "w", encoding="utf-16", newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter="\t")
        csv_writer.writerow(["Place", "Title", "Rating [adjusted]", "Rating [original]", "Oscar Calculator", "Review Penalizer"])
        list_to_return = []
        if session["movie_list"]:
            list_to_return = session["movie_list"]
        else:
            list_to_return = manager.get_list()

        for idx, movie in enumerate(list_to_return,start=1):
            csv_writer.writerow([idx, movie["title"], movie["rating_value"], movie["original_rating_value"], "+"+str(movie["bonus_value"]), "-"+str(movie["minus_value"])])
    
    return send_file(
        "outputs/ratings.csv",
        mimetype="Content-Type: text/csv; charset=Shift_JIS",
        attachment_filename="ratings.csv",
        as_attachment=True,
    )
    
if __name__ == "__main__":
    app.run(debug=True)
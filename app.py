from flask import Flask, render_template, send_file
from models import MovieManager
import os
import csv

app = Flask(__name__)
app.secret_key = "dzfJyr6ZcyGjRA7DozpPGEQjGcvDrL4P"

manager = MovieManager("https://www.imdb.com/chart/top/",20)

#Index
@app.route("/",methods=["GET"])
def index():  
    #Scraping, preprocessing the movies with adjustments  
    manager.preprocess()
    manager.review_penalizer()
    manager.oscar_calculator()
    return render_template("index.html",items=manager.get_list())

#Export
@app.route("/download", methods=["GET","POST"])
def download():
    #Generating a CSV file for export
    os.makedirs("outputs/", exist_ok=True)
    with open("outputs/ratings.csv", "w", encoding="utf-16", newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter="\t")
        csv_writer.writerow(["Place", "Title", "Rating [adjusted]", "Rating [original]", "Oscar Calculator", "Review Penalizer"])
        list_to_return = manager.get_list()
        for idx, movie in enumerate(list_to_return,start=1):
            csv_writer.writerow([idx, movie.title, movie.rating_value, movie.original_rating_value, "+" + str(movie.bonus_value), "-" + str(movie.minus_value)])

    #Exports the finished file    
    return send_file(
        "outputs/ratings.csv",
        mimetype="Content-Type: text/csv; charset=Shift_JIS",
        download_name="ratings.csv",
        as_attachment=True,
    )
    
if __name__ == "__main__":
    app.run(debug=True)
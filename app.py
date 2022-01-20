from flask import Flask, jsonify, render_template, send_file, session
from models import MovieManager
from time import time
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "dzfJyr6ZcyGjRA7DozpPGEQjGcvDrL4P"
app.permanent_session_lifetime = timedelta(hours=5)

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
    manager.generate_csv()
    return send_file(
        "outputs/ratings.csv",
        mimetype="Content-Type: text/csv; charset=Shift_JIS",
        attachment_filename="ratings.csv",
        as_attachment=True,
    )
    
if __name__ == "__main__":
    app.run(debug=True)
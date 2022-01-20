from flask import Flask, render_template, request, redirect, flash, send_file, Response
from models import MovieManager

app = Flask(__name__)
manager = MovieManager('https://www.imdb.com/chart/top/')

@app.route("/",methods=['GET','POST'])
def index():
    manager.preprocess()
    manager.review_penalizer()
    manager.oscar_calculator()

    return render_template('index.html',items=manager.get_list())

@app.route("/download", methods=['GET','POST'])
def download():
    manager.generate_csv()
    return send_file(
        'outputs/ratings.csv',
        mimetype='Content-Type: text/csv; charset=Shift_JIS',
        attachment_filename='ratings.csv',
        as_attachment=True,
    )
    
if __name__ == "__main__":
    app.run(debug=True)
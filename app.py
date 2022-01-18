from flask import Flask, render_template, request, redirect, flash

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',methods=['GET'])


if __name__ == "__main__":
    app.run(debug=True) #Set it false before hosting
from flask import Flask, render_template, request, redirect, flash
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen

url= 'https://www.imdb.com/chart/top/'

# opens the connection and downloads html page from url
client = urlopen(url)
# parses html into a soup data structure to traverse html
# as if it were a json data type.
page_soup = soup(client.read(), 'lxml')
client.close()
# finds each product from the store page
containers = page_soup.findAll('tr') #"td",{'class' : 'posterColumn'}

all_movies = []

for container in containers[1:21]:
    rk = container.find('span',{'name' : 'rk'}).attrs['data-value']
    ir = container.find('span',{'name' : 'ir'}).attrs['data-value']
    nv = container.find('span',{'name' : 'nv'}).attrs['data-value']
    all_movies.append({
        'rating' : rk,
        'counter' : ir
    })


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html',methods=['GET'],items=all_movies)


if __name__ == "__main__":
    app.run(debug=True) #Set it false before hosting
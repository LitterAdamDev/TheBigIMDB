from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from math import floor
import concurrent.futures

class Movie():
    def __init__(self, place, rating_value, rating_counter, oscars, title):
        self.place = place
        self.rating_value = rating_value
        self.original_rating_value = rating_value
        self.rating_counter = rating_counter
        self.oscars = oscars
        self.title = title
        self.bonus_value = 0
        self.minus_value = 0


class MovieManager():
    def __init__(self, url, limit):
        self.url = url
        self.list = []
        self.highest_counter = 0
        self.limit = limit
        
    def get_list(self):
        self.list.sort(key=lambda x: x.rating_value, reverse=True)
        return self.list
    
    def open_sub_container(self, container):
        oscars = 0
        href = container.find("a").attrs["href"]
        sub_client = urlopen("".join(["https://www.imdb.com/",href]))
        sub_page_soup = soup(sub_client.read(), "lxml")
        sub_client.close()
        
        section = sub_page_soup.find("div",{"class" : "Awards__Wrapper-sc-152rtbv-0 davyDx base"})
        text = section.find("a",{"class" : "ipc-metadata-list-item__label ipc-metadata-list-item__label--link"}).text.split()
        if text[0] == "Won":
            oscars = int(text[1])
        
        rating_counter = container.find("span",{"name" : "nv"}).attrs["data-value"]
        
        if int(rating_counter) > int(self.highest_counter):
            self.highest_counter = int(rating_counter)
        
        self.list.append(
            Movie(
                place=container.find("span",{"name" : "rk"}).attrs["data-value"],
                rating_value=round(float(container.find("span",{"name" : "ir"}).attrs["data-value"]),1),
                rating_counter= int(rating_counter),
                oscars=oscars,
                title=container.find("td",{"class" : "titleColumn"}).a.text
            )
        )
        
    def preprocess(self):
        self.list = []
        client = urlopen(self.url)
        page_soup = soup(client.read(), "lxml")
        client.close()
        
        main_container = page_soup.find("tbody",{"class" : "lister-list"})
        sub_containers = main_container.find_all("tr",limit=self.limit)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.limit) as executor:
            executor.map(self.open_sub_container,sub_containers)
        
        
    
    def review_penalizer(self):
        for movie in self.list:
            if movie.rating_counter < self.highest_counter:
                movie.minus_value = round(floor((self.highest_counter - movie.rating_counter)/100000) * 0.1,1)
                movie.rating_value = movie.rating_value - floor((self.highest_counter - movie.rating_counter)/100000) * 0.1

    
    def oscar_calculator(self):
        for movie in self.list:
            points = 0     
            
            if movie.oscars >=10:
                points = 1.5
            elif movie.oscars >= 6:
                points = 1
            elif movie.oscars >= 3:
                points = 0.5 
            elif movie.oscars > 0:
                points = 0.3
            
            movie.bonus_value = points
            movie.rating_value = round(max(min(movie.rating_value + points,10),0),1)
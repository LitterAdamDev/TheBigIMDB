from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from math import floor

class Movie():
    def __init__(self, place, rating_value, rating_counter, oscars, title):
        self._place = place
        self._rating_value = rating_value
        self._rating_counter = rating_counter
        self._oscars = oscars
        self._title = title


class MovieManager():
    def __init__(self,url):
        self._url = url
        self._list = []
        self._highest_counter = 0
        
    def get_list(self):
        return self._list
        
    def preprocess(self):
        client = urlopen(self._url)
        page_soup = soup(client.read(), 'lxml')
        client.close()
        
        main_container = page_soup.find('tbody',{'class' : 'lister-list'})
        sub_containers = main_container.find_all('tr',limit=5)
        for container in sub_containers:
            
            oscars = 0
            href = container.find('a').attrs['href']
            sub_client = urlopen(''.join(['https://www.imdb.com/',href]))
            sub_page_soup = soup(sub_client.read(), 'lxml')
            sub_client.close()
            
            section = sub_page_soup.find('div',{'class' : 'Awards__Wrapper-sc-152rtbv-0 davyDx base'})
            text = section.find('a',{'class' : 'ipc-metadata-list-item__label ipc-metadata-list-item__label--link'}).text.split()
            if text[0] == 'Won':
                oscars = int(text[1])
            
            rating_counter = container.find('span',{'name' : 'nv'}).attrs['data-value']
            
            if int(rating_counter) > (self._highest_counter):
                self._highest_counter = int(rating_counter)
            
            self._list.append(
                Movie(
                    place=container.find('span',{'name' : 'rk'}).attrs['data-value'],
                    rating_value=float(container.find('span',{'name' : 'ir'}).attrs['data-value']),
                    rating_counter= int(rating_counter),
                    oscars=oscars,
                    title=container.find('td',{'class' : 'titleColumn'}).a.text
                )
            )
    
    def review_penalizer(self):
        for movie in self._list:
            if movie._rating_counter < self._highest_counter:
                movie._rating_value = movie._rating_value - floor((self._highest_counter - movie._rating_counter)/100000) * 0.1
    
    def oscar_calculator(self):
        for movie in self._list:
            points = 0     
            
            if movie._oscars >=10:
                points = 1.5
            elif movie._oscars >= 6:
                points = 1
            elif movie._oscars >= 3:
                points = 0.5 
            elif movie._oscars > 0:
                points = 0.3
              
            movie._rating_value = movie._rating_value + points
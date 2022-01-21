from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
from urllib.error import HTTPError
from math import floor
import concurrent.futures

class Movie():
    """Stores the scraped, and additional properties of a specific movie for further purposes.

    Arguments:
    title -- the title of the movie
    place -- the place of the movie in the rank list. 
    rating_value -- the achieved rating
    rating_counter -- the number of reviews submitted by the people
    oscars -- the number of Oscars the film has earned
    
    Additional properties:
    bonus_value -- calculated deduction by the review_penalizer function
    minus_value -- calculated addition by the oscar_calculated function
    """
    def __init__(self, title, place, rating_value, rating_counter, oscars):
        self.place = int(place)
        self.rating_value = float(rating_value)
        self.original_rating_value = float(rating_value)
        self.rating_counter = int(floor(rating_counter))
        self.oscars = int(oscars)
        self.title = title
        self.bonus_value = 0.0
        self.minus_value = 0.0


class MovieManager():
    """Scrapes, stores and adjust data of a specified amount of movies.

    Arguments:
        url -- the url of the rank list for the scraping function
        limit -- the number of movies to be scraped

    Additional properties:
        movie_storage -- list of Movie objects to store the scraped data
        highest_counter -- the number of reviews at the most reviewed movie in the scraped data
    """
    def __init__(self, url, limit):
        self.url = url
        self.movie_storage = []
        self.highest_counter = 0
        self.limit = limit
        
    def get_list(self):
        """Sorts and returns the movie_storage based on the adjusted ratings.

        Returns:
            sorted list of Movie objects
        """
        self.movie_storage.sort(key=lambda x: x.rating_value, reverse=True)
        return self.movie_storage
    
    def open_sub_container(self, container):
        """Finds specified values in raw scraped data and stores them.(optional solution for multiprocessing)

        Args:
            container -- raw scraped data for further processing
        Raises:
            HTTPError: if the provided url is wrong for some reason.
        """

        oscars = 0
        #Finding the required href argument value to scrape more data about the current movie
        href = container.find("a").attrs["href"]

        try:
            sub_client = urlopen("".join(["https://www.imdb.com/",href]))
            sub_page_soup = soup(sub_client.read(), "lxml")
            sub_client.close()
        except HTTPError as http_error:
            print(http_error)

        #Getting the number of Oscars if any
        section = sub_page_soup.find("div",{"class" : "Awards__Wrapper-sc-152rtbv-0 davyDx base"})
        text = section.find("a",{"class" : "ipc-metadata-list-item__label ipc-metadata-list-item__label--link"}).text.split()
        if text[0] == "Won":
            oscars = int(text[1])
        
        #Update the highest_counter property if necessary
        rating_counter = container.find("span",{"name" : "nv"}).attrs["data-value"]
        if int(rating_counter) > int(self.highest_counter):
            self.highest_counter = int(rating_counter)
        
        self.movie_storage.append(
            Movie(
                place=container.find("span",{"name" : "rk"}).attrs["data-value"],
                rating_value=round(float(container.find("span",{"name" : "ir"}).attrs["data-value"]),1),
                rating_counter= int(rating_counter),
                oscars=oscars,
                title=container.find("td",{"class" : "titleColumn"}).a.text
            )
        )
        
    def preprocess(self):
        """Scrapes and preprocess the raw text data.(via multiprocessing)

        Raises:
            HTTPError: if the provided url is wrong for some reason.
        """

        try:
            client = urlopen(self.url)
            page_soup = soup(client.read(), "lxml")
            client.close()
        except HTTPError as http_error:
            print(http_error)
        
        main_container = page_soup.find("tbody",{"class" : "lister-list"})
        sub_containers = main_container.find_all("tr",limit=self.limit)
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.limit) as executor:
            executor.map(self.open_sub_container,sub_containers)
        
        
    
    def review_penalizer(self):
        """Penalize those movies where the number of reviews is low.

        Implementation: 
            -1 * ([Maximum number of reviews] - [Current number of reviews])/100000 * 0.1
        """

        for movie in self.movie_storage:
            if movie.rating_counter < self.highest_counter:
                movie.minus_value = round(floor((self.highest_counter - movie.rating_counter)/100000) * 0.1,1)
                movie.rating_value = movie.rating_value - floor((self.highest_counter - movie.rating_counter)/100000) * 0.1

    
    def oscar_calculator(self):
        """Rewards movies with more Oscars
        """
        for movie in self.movie_storage:
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
            #The value of the rating must be between 0.0 and 10.0
            #The number of decimal places is optional
            movie.rating_value = round(max(min(movie.rating_value + points,10),0),1)
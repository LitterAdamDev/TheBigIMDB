import unittest
from app import app
from models import Movie, MovieManager

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        #Setting up a temponary "testing enviorment" with dummy data
        self.ctx = app.app_context()
        self.ctx.push()
        self.client = app.test_client()
        self.manager = MovieManager("https://www.imdb.com/chart/top/",20)
        self.manager.movie_storage = [Movie('First Movie',1,5.0,1000000,5), Movie('Second Movie',2,6.0,100000,0,), Movie('Third Movie',3,9.9,2000000,8)]
        self.manager.highest_counter = 2000000
    
    def tearDown(self):
        self.ctx.pop()
    
    def test_home_route(self):
        #Testing the home route and the number of scraped movies
        res = self.client.get('/', content_type='html/text')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'The Big IMDB quest', res.data)
        self.assertIn(b'<th scope="row">20</th>', res.data)
    
    def test_download_route(self):
        #Testing the export action and the result file contained by the response
        res = self.client.post('/download', content_type='text/csv',follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.headers['Content-Disposition'],'attachment; filename=ratings.csv')
        
    def test_review_penalizer(self):
        #Testing the review_penalizer function with dummy data
        self.manager.review_penalizer()
        result = self.manager.get_list()
        self.assertEqual(len(result),3)
        self.assertEqual([result[0].rating_value,result[1].rating_value,result[2].rating_value],[9.9,4.1,4.0])
    
    def test_oscar_calculator(self):
        #Testing the oscar_calculator function with dummy data
        self.manager.oscar_calculator()
        result = self.manager.get_list()
        self.assertEqual(len(result),3)
        self.assertEqual([result[0].rating_value,result[1].rating_value,result[2].rating_value],[10,6.0,5.5])

if __name__ == "__main__":
    unittest.main()
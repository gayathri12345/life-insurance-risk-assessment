from app import app
import unittest
from urllib import request


class TestHelloAPI(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_one(self):
        response=self.app.get('/')
        self.assertEqual(response.status_code,200)
        
    def test_two(self):
        response=self.app.get('/')
        self.assertTrue(b'LIFE INSURANCE RISK ASSESSMENT OF CUSTOMERS' in response.data)
       
    def test_three(self):
        response=self.app.get('/')
        self.assertTrue(b'Predict the risk of customers' in response.data)
       

if __name__=='__main__':
    unittest.main(verbosity=1)
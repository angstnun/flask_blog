import unittest
from selenium import webdriver
from flaskr import create_app


class AppTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app({
            "TESTING": True
        })
        self.client = self.app.test_client()

    def tearDown(self):
        pass

    def test_CheckIfRootReturns200(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main(verbosity=2)

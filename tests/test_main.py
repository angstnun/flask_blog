import unittest
from selenium import webdriver

class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)
            
    def test_radiohead(self):
        result = 2 + 2
        self.assertEqual(result, 4, "Radiohead logic doesn't work here")
        
    def test_shouldDisplayHomePage(self):
        browser = webdriver.Chrome()
        browser.get('http://localhost:5000')
        isFlaskr = browser.title.upper().find("FLASKR") > -1
        self.assertTrue(isFlaskr)

if __name__ == '__main__':
    unittest.main(verbosity=2)
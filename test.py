import unittest
from app import app

class APITestCase(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_get_word(self):
        response = self.app.get('/')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn('word', data)
        self.assertEqual(data['word'], 'NewWord')
        
        

    def test_update_word(self):
        with app.test_client() as client:
            # Authenticate as admin
            client.post('/admin', data={'username': 'admin', 'password': 'root'})

            # Update the word
            response = client.post('/admin', data={'word': 'NewWord'})
            self.assertEqual(response.status_code, 200)

            # Fetch the updated word
            response = self.app.get('/')
            data = response.get_json()
            self.assertEqual(response.status_code, 200)
            self.assertIn('word', data)
            self.assertEqual(data['word'], 'NewWord')

if __name__ == '__main__':
    unittest.main()

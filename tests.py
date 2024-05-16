import unittest
from flask_testing import TestCase
from codebreaker import app  # Asegúrate de importar tu app de Flask correctamente

class TestCodebreakerAPI(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.client = app.test_client()

    def test_guess_correct_input(self):
        response = self.client.post('/guess', json={'guess': '1234'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('exact', response.json)
        self.assertIn('near', response.json)

    def test_guess_invalid_input(self):
        response = self.client.post('/guess', json={'guess': 'abc'})
        self.assertEqual(response.status_code, 400)

    def test_set_code_correct(self):
        response = self.client.post('/set_code', json={'new_code': '9876'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Secret code updated successfully', response.json['message'])

    def test_set_code_invalid_input(self):
        response = self.client.post('/set_code', json={'new_code': 'abc'})
        self.assertEqual(response.status_code, 400)

    def test_guess_after_code_set(self):
        self.client.post('/set_code', json={'new_code': '0000'})
        response = self.client.post('/guess', json={'guess': '0000'})
        self.assertEqual(response.json, {'exact': 4, 'near': 0})

if __name__ == '__main__':
    unittest.main()
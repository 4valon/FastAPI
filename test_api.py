import unittest
from fastapi.testclient import TestClient
#from api_michal import app
from csv_to_json import app as blazej_api

# Setup the TestClient
client = TestClient(blazej_api)

class TestCSVToJsonEndpoint(unittest.TestCase):
    def test_normal_csv(self):
        data = "name,age,location\nAlice,24,Boston\nBob,19,Seattle"
        files = {'file': ('test.csv', data, 'text/csv')}
        response = client.post("/csv_to_json", files=files)
        self.assertEqual(response.status_code, 200)
        expected_json = {
            'name': ['Alice', 'Bob'], 
            'age': ['24', '19'],
            'location': ['Boston', 'Seattle']
        }
        self.assertEqual(response.json(), expected_json)

    def test_empty_csv(self):
        data = ""
        files = {'file': ('empty.csv', data, 'text/csv')}
        response = client.post("/csv_to_json", files=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    def test_csv_with_headers_only(self):
        data = "name,age"
        files = {'file': ('headers_only.csv', data, 'text/csv')}
        response = client.post("/csv_to_json", files=files)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {})

    def test_csv_with_extra_spaces(self):
        data = "name , age \n Alice , 24 \n Bob , 19 "
        files = {'file': ('extra_spaces.csv', data, 'text/csv')}
        response = client.post("/csv_to_json", files=files)
        expected_json = {'name ': [' Alice ', ' Bob '], ' age ': [' 24 ', ' 19 ']}
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), expected_json)

    def test_csv_with_missing_values(self):
        data = "name,age\nAlice,24\nBob,"
        files = {'file': ('missing_values.csv', data, 'text/csv')}
        response = client.post("/csv_to_json", files=files)
        self.assertEqual(response.status_code, 200)
        expected_json = {'name': ['Alice', 'Bob'], 'age': ['24', '']}
        self.assertEqual(response.json(), expected_json)

    def test_csv_with_special_characters(self):
        data = "name,age\nAlice,24\nBob@,#19\nÇarl,30"
        files = {'file': ('special_chars.csv', data, 'text/csv')}
        response = client.post("/csv_to_json", files=files)
        self.assertEqual(response.status_code, 200)
        expected_json = {'name': ['Alice', 'Bob@', 'Çarl'], 'age': ['24', '#19', '30']}
        self.assertEqual(response.json(), expected_json)

if __name__ == '__main__':
    unittest.main()

import os
import unittest
import requests
import time

class FlaskrTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        url = 'http://127.0.0.1:5000/v1/tasks/remove'
        response = requests.get(url)

    '''
    Examples:

    def test_0_connect_db(self):
        url = 'http://127.0.0.1:5000/v1/tasks'
        response = requests.get(url)
        assert response.status_code == 200

    def test_1_remove_all(self):
        url = 'http://127.0.0.1:5000/v1/tasks/remove'
        response = requests.get(url)
        assert response.status_code == 200

    def test_2_insert_in_db(self):
        headers = {"Content-Type": "application/json"}
        url = 'http://127.0.0.1:5000/v1/tasks'

        data = {"title": "Test Task 1", "is_completed": "true"}
        response = requests.post(url, json=data, headers=headers)

        data = {"title": "Test Task 2", "is_completed": "false"}
        response = requests.post(url, json=data, headers=headers)

        response = requests.get(url)
        tasks = response.json()['tasks']
        assert response.status_code==200
    '''


    @classmethod
    def tearDownClass(cls):
        pass

if __name__ == '__main__':
    unittest.main()
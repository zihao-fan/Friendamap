import requests
import json

endpoint_url = 'http://localhost:5000/v1'
headers = {
	'Content-Type': 'application/json'
}

def post_task(title, is_completed=False):
	url = endpoint_url + '/tasks'
	data = {
		'title': title,
		'is_completed': is_completed
	}
	resp = requests.post(url, data=json.dumps(data), headers=headers)
	return (resp.status_code, resp.json())

input = {
	'tasks': [
    	{'title': "Test Task 1", 'is_completed': True},
     	{'title': "Test Task 2", 'is_completed': False},
      	{'title': "Test Task 3", 'is_completed': True}
	]
}

def post_tasks(input):
	url = endpoint_url + '/tasks'

	resp = requests.post(url, data=json.dumps(input), headers=headers)
	print(resp)
	return (resp.status_code, resp.json())

def get_post(id):
	url = endpoint_url + '/tasks/{}'.format(id)

	resp = requests.get(url, headers=headers)
	return (resp.status_code, resp.json())

def get_posts():
	url = endpoint_url + '/tasks'
	resp = requests.get(url, headers=headers)
	return (resp.status_code, resp.json())

def delete_post(id):
	url = endpoint_url + '/tasks/{}'.format(id)

	resp = requests.delete(url, headers=headers)
	return (resp.status_code, None)

def delete_posts():
	input = {
		'tasks': [
	      {'id': 1},
	      {'id': 2},
	      {'id': 3}		
		]
	}
	url = endpoint_url + '/tasks'
	resp = requests.delete(url, data=json.dumps(input), headers=headers)
	return (resp.status_code, None)


def edit_post(id, new_title, new_is_completed):
	url = endpoint_url + '/tasks/{}'.format(id)

	data = {
		'title': new_title,
		'is_completed': new_is_completed
	}


	resp = requests.put(url, data=json.dumps(data), headers=headers)

	if resp.status_code == 404:
		return (resp.status_code, resp.json())

	return (resp.status_code, None)


"""
initial data
"""

post_task('Test Task 1', True)
post_task('Test Task 2')
post_task('Test Task 3', True)

